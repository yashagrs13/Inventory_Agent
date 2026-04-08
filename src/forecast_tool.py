# src/forecast_tool.py
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from crewai.tools import tool
from src.db import get_item_history

def generate_forecast_data(item_name: str):
    """
    Core function to generate linear regression forecast for an item.
    Returns both the metrics and the data points for charting.
    """
    history = get_item_history(item_name)
    
    if len(history) < 2:
        return {"error": "Not enough historical data (minimum 2 data points required)."}
        
    # Convert timestamps to days since first record
    try:
        first_date = datetime.fromisoformat(history[0]['timestamp'])
        
        X = []
        Y = []
        chart_data = []
        
        for record in history:
            current_date = datetime.fromisoformat(record['timestamp'])
            days = (current_date - first_date).days
            balance = float(record['closing_balance'])
            
            X.append([days])
            Y.append(balance)
            
            chart_data.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "actual": balance,
                "predicted": None # Will fill later
            })
            
        X = np.array(X)
        Y = np.array(Y)
        
        # Fit Linear Regression Model
        model = LinearRegression()
        model.fit(X, Y)
        
        coef = model.coef_[0]
        intercept = model.intercept_
        
        if coef >= 0:
            trend = "stable or increasing"
            days_to_zero = -1
        else:
            trend = "decreasing"
            # Solve for 0 = coef * days + intercept -> days = -intercept / coef
            days_to_zero = int(-intercept / coef)
            
        # Add predictions for past data points to show the trend line
        predictions = model.predict(X)
        for i, pred in enumerate(predictions):
            chart_data[i]["predicted"] = round(float(pred), 2)
            
        # Forecast future points (e.g., next 30 days or until 0)
        future_points = []
        if trend == "decreasing" and days_to_zero > X[-1][0]:
            # Generate points until it hits zero
            future_days_list = list(range(X[-1][0] + 1, min(days_to_zero + 1, X[-1][0] + 31)))
        else:
            # Generate next 14 days
            future_days_list = list(range(X[-1][0] + 1, X[-1][0] + 15))
            
        for future_day in future_days_list:
            pred_amount = max(0, model.predict([[future_day]])[0])
            future_date = first_date + timedelta(days=future_day)
            
            future_points.append({
                "date": future_date.strftime("%Y-%m-%d"),
                "actual": None,
                "predicted": round(float(pred_amount), 2)
            })
            
        chart_data.extend(future_points)
        
        depletion_date = (first_date + timedelta(days=days_to_zero)).strftime("%Y-%m-%d") if days_to_zero > 0 else "N/A"
        
        return {
            "item_name": item_name,
            "trend": trend,
            "burn_rate_per_day": round(float(abs(coef)), 2) if coef < 0 else 0,
            "days_until_depletion": days_to_zero - X[-1][0] if days_to_zero > X[-1][0] else -1,
            "estimated_depletion_date": depletion_date,
            "data_points": chart_data
        }
        
    except Exception as e:
        return {"error": f"Forecasting failed: {str(e)}"}

@tool("Forecast Item Stock")
def forecast_item_tool(item_name: str) -> str:
    """
    Uses Linear Regression (scikit-learn) on historical data to predict when an item will run out of stock.
    Input MUST be the exact 'item_name'. 
    It returns the trend, daily burn rate, and estimated out-of-stock date.
    """
    result = generate_forecast_data(item_name)
    if "error" in result:
        return result["error"]
        
    if result["trend"] == "decreasing":
        msg = (f"Trend: Decreasing. "
               f"Burning ~{result['burn_rate_per_day']} units/day. "
               f"Estimated to run out in {result['days_until_depletion']} days (around {result['estimated_depletion_date']}).")
    else:
        msg = "Trend: Stable or Increasing. No immediate risk of depletion."
        
    return msg
