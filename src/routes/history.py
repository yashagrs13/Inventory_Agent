# src/routes/history.py
import json
from flask import Blueprint, request, jsonify
from crewai import Crew, Task, Process
from src.db import get_runs, get_run, get_comparison
from src.agents import comparison_analyst

history_bp = Blueprint('history', __name__)


@history_bp.route('/history')
def list_history():
    """Get all past analysis runs."""
    runs = get_runs()
    return jsonify({"runs": runs})


@history_bp.route('/compare')
def compare_runs():
    """Compare two analysis runs side-by-side with AI narrative."""
    run1_id = request.args.get('run1', type=int)
    run2_id = request.args.get('run2', type=int)

    if not run1_id or not run2_id:
        return jsonify({"error": "Please provide run1 and run2 query parameters"}), 400

    comparison = get_comparison(run1_id, run2_id)

    if not comparison:
        return jsonify({"error": "One or both runs not found"}), 404

    # Generate AI narrative comparing the two runs
    try:
        run1 = comparison['run1']
        run2 = comparison['run2']
        delta = comparison['delta']

        comparison_data = f"""
        Run 1 (ID: {run1['id']}, Date: {run1['timestamp']}, File: {run1['input_filename']}):
        - Total Items: {run1['total_items']}
        - Out of Stock: {run1['out_of_stock_count']}
        - Low Stock: {run1['low_stock_count']}
        - Critical (Negative): {run1['critical_count']}

        Run 2 (ID: {run2['id']}, Date: {run2['timestamp']}, File: {run2['input_filename']}):
        - Total Items: {run2['total_items']}
        - Out of Stock: {run2['out_of_stock_count']}
        - Low Stock: {run2['low_stock_count']}
        - Critical (Negative): {run2['critical_count']}

        Changes (Run 1 → Run 2):
        - Out of Stock: {'+' if delta['out_of_stock'] > 0 else ''}{delta['out_of_stock']}
        - Low Stock: {'+' if delta['low_stock'] > 0 else ''}{delta['low_stock']}
        - Critical: {'+' if delta['critical'] > 0 else ''}{delta['critical']}
        - Total Items: {'+' if delta['total_items'] > 0 else ''}{delta['total_items']}
        """

        comparison_task = Task(
            description=f"""
            Compare these two inventory analysis snapshots and write a 2-3 paragraph 
            narrative summary for the business owner:

            {comparison_data}

            Your narrative should:
            1. State whether inventory health improved or worsened overall
            2. Highlight the most significant changes
            3. Provide brief, actionable recommendations
            
            Keep it concise and business-friendly. Do NOT use technical jargon.
            """,
            expected_output="A 2-3 paragraph business narrative comparing the two inventory snapshots.",
            agent=comparison_analyst
        )

        comparison_crew = Crew(
            agents=[comparison_analyst],
            tasks=[comparison_task],
            process=Process.sequential,
            verbose=True
        )

        narrative = str(comparison_crew.kickoff())
        comparison['narrative'] = narrative

    except Exception as e:
        # If AI narrative fails, still return the data without it
        comparison['narrative'] = None
        comparison['narrative_error'] = str(e)

    return jsonify(comparison)
