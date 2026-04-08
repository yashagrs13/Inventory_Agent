# src/routes/results.py
from flask import Blueprint, jsonify, send_from_directory
from src.db import get_run
import os

results_bp = Blueprint('results', __name__)

REPORTS_FOLDER = 'reports'


@results_bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(REPORTS_FOLDER, filename, as_attachment=True)


@results_bp.route('/results/<int:run_id>')
def get_results(run_id):
    """Get full analysis results for the dashboard."""
    run = get_run(run_id)

    if not run:
        return jsonify({"error": "Analysis run not found"}), 404

    return jsonify({
        "id": run['id'],
        "timestamp": run['timestamp'],
        "input_filename": run['input_filename'],
        "report_filename": run['report_filename'],
        "status": run['status'],
        "agent_output": run['agent_output'],
        "summary_stats": {
            "out_of_stock_count": run['out_of_stock_count'],
            "low_stock_count": run['low_stock_count'],
            "critical_count": run['critical_count'],
            "total_items": run['total_items'],
            "healthy_count": run['total_items'] - run['out_of_stock_count'] - run['low_stock_count'] - run['critical_count']
        },
        "items": run.get('items', {}),
        "download_url": f"/download/{run['report_filename']}" if run['report_filename'] else None
    })
