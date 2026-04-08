# src/tools.py
import os
import glob
import pandas as pd
from datetime import datetime
from crewai.tools import tool


def run_inventory_analysis():
    """
    Core analysis logic. Returns structured data dict.
    Used by both the CrewAI tool and the API directly.
    """
    data_folder = 'data'
    reports_folder = 'reports'

    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    stock_files = glob.glob(os.path.join(data_folder, 'Stock_Summary_*.xlsx'))
    if not stock_files:
        return {
            "status": "error",
            "message": "Could not find any 'Stock_Summary_*.xlsx' file in the 'data' folder."
        }

    latest_stock_file = max(stock_files, key=os.path.getmtime)
    df_stock = pd.read_excel(latest_stock_file)

    df_stock['Closing Balance'] = pd.to_numeric(
        df_stock['Closing Balance'].astype(str).str.replace(r'\s*[A-Za-z.]*$', '', regex=True),
        errors='coerce'
    )
    df_stock['Closing Balance'].fillna(0, inplace=True)

    out_of_stock = df_stock[df_stock['Closing Balance'] == 0].copy()
    low_stock = df_stock[(df_stock['Closing Balance'] > 0) & (df_stock['Closing Balance'] < 5)].copy()
    critical_stock = df_stock[df_stock['Closing Balance'] < 0].copy()

    today_str = datetime.now().strftime("%Y-%m-%d")
    report_filename = f"Inventory_Report_{today_str}.xlsx"
    report_filepath = os.path.join(reports_folder, report_filename)

    with pd.ExcelWriter(report_filepath, engine='openpyxl') as writer:
        out_of_stock[['Name', 'Closing Balance']].to_excel(
            writer, sheet_name='Out of Stock Items', index=False)
        low_stock[['Name', 'Closing Balance']].to_excel(
            writer, sheet_name='Low Stock Items', index=False)
        critical_stock[['Name', 'Closing Balance']].to_excel(
            writer, sheet_name='Critical Stock Items', index=False)

    # Build structured result
    result = {
        "status": "success",
        "message": f"Successfully created the inventory report: {report_filepath}",
        "filename": report_filename,
        "filepath": report_filepath,
        "total_items": len(df_stock),
        "summary_stats": {
            "out_of_stock_count": len(out_of_stock),
            "low_stock_count": len(low_stock),
            "critical_count": len(critical_stock),
            "total_items": len(df_stock),
            "healthy_count": len(df_stock) - len(out_of_stock) - len(low_stock) - len(critical_stock)
        },
        "items": {
            "out_of_stock": out_of_stock[['Name', 'Closing Balance']].to_dict('records'),
            "low_stock": low_stock[['Name', 'Closing Balance']].to_dict('records'),
            "critical": critical_stock[['Name', 'Closing Balance']].to_dict('records')
        }
    }

    return result


@tool("Inventory Analysis Tool")
def inventory_analysis_tool() -> str:
    """
    Analyzes the most recent stock data from an Excel file in the 'data' folder.
    It identifies out-of-stock and low-stock items, then generates and saves
    a new Excel report in the 'reports' folder.
    """
    try:
        result = run_inventory_analysis()
        return result.get("message", "Analysis completed.")
    except Exception as e:
        return f"An error occurred during inventory analysis: {str(e)}"