# src/routes/audit.py
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from crewai import Crew, Task, Process
from src.agents import audit_agent

audit_bp = Blueprint('audit', __name__)

UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@audit_bp.route('/audit/upload', methods=['POST'])
def upload_ledger():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Kick off the audit agent
        try:
            audit_task = Task(
                description=f"""
                A new ledger file has been uploaded at '{filepath}'.
                Use the 'Ledger Audit Tool' to analyze it. 
                Based on the tool's output, write a detailed executive summary for the business owner.
                
                CRITICAL INSTRUCTION: You MUST explicitly list the exact integer amounts (e.g., "$250,000") 
                and descriptions provided by the tool for any high-value transactions or anomalies found. 
                Do not just say "there are high value transactions"—show the user the exact item name, date, 
                and the exact financial value causing the anomaly.
                
                Format the final response nicely in Markdown with bullet points for easy reading.
                """,
                expected_output="A well-formatted Markdown report outlining the financial risks and summary of the ledger.",
                agent=audit_agent
            )

            audit_crew = Crew(
                agents=[audit_agent],
                tasks=[audit_task],
                process=Process.sequential,
                verbose=True
            )

            result = str(audit_crew.kickoff())

            return jsonify({
                "message": "Audit completed",
                "filename": filename,
                "report": result
            }), 200

        except Exception as e:
            return jsonify({"error": f"Failed to run audit analysis: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type. Only Excel or CSV allowed."}), 400
