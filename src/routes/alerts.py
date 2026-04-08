# src/routes/alerts.py
from flask import Blueprint, request, jsonify
from crewai import Crew, Task, Process
from src.agents import reorder_agent
from src.db import get_run

alerts_bp = Blueprint('alerts', __name__)

@alerts_bp.route('/alerts/send', methods=['POST'])
def send_alert():
    """Trigger the reorder_agent to generate and send an alert email based on a run's data."""
    data = request.json
    run_id = data.get('run_id')
    to_email = data.get('to_email')

    if not run_id or not to_email:
        return jsonify({"error": "Missing run_id or to_email"}), 400

    run_data = get_run(run_id)
    if not run_data:
        return jsonify({"error": "Run not found"}), 404

    # Extract critical and out of stock items
    critical_items = run_data['items'].get('critical', [])
    out_of_stock_items = run_data['items'].get('out_of_stock', [])
    low_stock_items = run_data['items'].get('low_stock', [])

    if not critical_items and not out_of_stock_items:
        return jsonify({"message": "No critical or out of stock items to alert about."}), 200

    items_to_alert = critical_items + out_of_stock_items

    # Prepare data for the agent
    items_list_str = "\n".join([f"- {item['Name']} (Current Balance: {item['Closing Balance']})" for item in items_to_alert])

    try:
        alert_task = Task(
            description=f"""
            Review the following items that are critically low or out of stock.
            
            Target recipient email: {to_email}
            
            Items requiring immediate reorder action:
            {items_list_str}
            
            Action: 
            Use the 'Send Email Alert' tool to send a professional reorder request email to the 
            supplier or business owner at '{to_email}'. 
            The email subject should be urgent but professional. 
            The body should clearly list the items needing restocking and request prompt action.
            """,
            expected_output="Confirmation of whether the email was successfully sent using the tool.",
            agent=reorder_agent
        )

        alert_crew = Crew(
            agents=[reorder_agent],
            tasks=[alert_task],
            process=Process.sequential,
            verbose=True
        )

        result = str(alert_crew.kickoff())

        return jsonify({
            "message": "Alert process completed",
            "agent_result": result
        })

    except Exception as e:
        return jsonify({"error": f"Failed to run alert agent: {str(e)}"}), 500
