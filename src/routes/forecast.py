# src/routes/forecast.py
from flask import Blueprint, request, jsonify
from src.forecast_tool import generate_forecast_data
from src.db import get_run

forecast_bp = Blueprint('forecast', __name__)

@forecast_bp.route('/forecast', methods=['GET'])
def get_forecast():
    """Endpoint for the dashboard to get forecast data for a specific item."""
    item_name = request.args.get('item_name')
    if not item_name:
        return jsonify({"error": "Missing item_name parameter"}), 400

    result = generate_forecast_data(item_name)
    if "error" in result:
        return jsonify(result), 400

    return jsonify(result), 200

@forecast_bp.route('/forecast/top', methods=['GET'])
def get_top_forecasts():
    """Get forecast data for the top critical items from a specific run."""
    run_id = request.args.get('run_id', type=int)
    if not run_id:
        return jsonify({"error": "Missing run_id parameter"}), 400

    run_data = get_run(run_id)
    if not run_data:
        return jsonify({"error": "Run not found"}), 404

    # We want to forecast items that are low stock (since out of stock is already depleted, 
    # and healthy might not need immediate attention).
    items_to_forecast = run_data['items'].get('low_stock', [])
    
    # Take up to 3 items to avoid long processing times in this demo
    items_to_forecast = items_to_forecast[:3]

    forecasts = []
    for item in items_to_forecast:
        forecast_result = generate_forecast_data(item['Name'])
        if "error" not in forecast_result:
            forecasts.append(forecast_result)

    return jsonify({"forecasts": forecasts}), 200
