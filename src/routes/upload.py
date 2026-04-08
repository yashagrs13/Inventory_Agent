# src/routes/upload.py
import json
import threading
from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from crewai import Crew, Process
from src.agents import stock_analyst_agent, report_creator_agent
from src.tasks import analysis_task, reporting_task
from src.tools import run_inventory_analysis
from src.db import save_run
from src.stream_capture import CrewOutputCapture

upload_bp = Blueprint('upload', __name__)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_uploaded_file(file):
    """Save uploaded file and return the new filename and path."""
    filename = secure_filename(file.filename)
    today_str = datetime.now().strftime("%Y-%m-%d")
    new_filename = f"Stock_Summary_{today_str}.xlsx"
    filepath = os.path.join('data', new_filename)
    file.save(filepath)
    return new_filename, filepath


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Standard (non-streaming) upload endpoint."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        try:
            new_filename, filepath = _save_uploaded_file(file)

            # Run CrewAI analysis
            inventory_crew = Crew(
                agents=[stock_analyst_agent, report_creator_agent],
                tasks=[analysis_task, reporting_task],
                process=Process.sequential,
                verbose=True
            )

            crew_result = inventory_crew.kickoff()

            # Run the structured analysis to get data for DB / dashboard
            analysis_result = run_inventory_analysis()

            if analysis_result['status'] == 'success':
                run_id = save_run(
                    input_filename=new_filename,
                    report_filename=analysis_result['filename'],
                    status='success',
                    agent_output=str(crew_result),
                    summary_data=analysis_result['summary_stats'],
                    items_data=analysis_result['items']
                )

                return jsonify({
                    "message": "Report generated successfully",
                    "run_id": run_id,
                    "download_url": f"/download/{analysis_result['filename']}",
                    "filename": analysis_result['filename']
                })
            else:
                return jsonify({"error": analysis_result.get('message', 'Analysis failed')}), 500

        except Exception as e:
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type. Please upload .xlsx or .xls files"}), 400


@upload_bp.route('/upload-stream', methods=['POST'])
def upload_stream():
    """SSE streaming upload endpoint — streams agent thoughts in real-time."""
    if 'file' not in request.files:
        return Response(
            f"data: {json.dumps({'type': 'error', 'content': 'No file uploaded'})}\n\n",
            mimetype='text/event-stream'
        )

    file = request.files['file']

    if file.filename == '' or not allowed_file(file.filename):
        return Response(
            f"data: {json.dumps({'type': 'error', 'content': 'Invalid file'})}\n\n",
            mimetype='text/event-stream'
        )

    new_filename, filepath = _save_uploaded_file(file)

    def generate():
        capture = CrewOutputCapture()
        result_holder = {'crew_result': None, 'error': None, 'done': False}

        def run_crew():
            try:
                capture.start_capture()

                inventory_crew = Crew(
                    agents=[stock_analyst_agent, report_creator_agent],
                    tasks=[analysis_task, reporting_task],
                    process=Process.sequential,
                    verbose=True
                )

                result_holder['crew_result'] = inventory_crew.kickoff()

            except Exception as e:
                result_holder['error'] = str(e)
            finally:
                capture.stop_capture()
                result_holder['done'] = True

        # Start crew in background thread
        crew_thread = threading.Thread(target=run_crew, daemon=True)
        crew_thread.start()

        # Stream events
        yield f"data: {json.dumps({'type': 'status', 'content': 'Analysis started...', 'timestamp': datetime.now().isoformat()})}\n\n"

        while not result_holder['done']:
            events = capture.drain_events()
            if events:
                for event in events:
                    yield f"data: {json.dumps(event)}\n\n"
            else:
                # Keepalive
                import time
                time.sleep(0.3)
                yield f"data: {json.dumps({'type': 'keepalive', 'timestamp': datetime.now().isoformat()})}\n\n"

        # Drain remaining events
        events = capture.drain_events()
        for event in events:
            yield f"data: {json.dumps(event)}\n\n"

        # Run structured analysis and save to DB
        if result_holder['error']:
            yield f"data: {json.dumps({'type': 'error', 'content': result_holder['error'], 'timestamp': datetime.now().isoformat()})}\n\n"
        else:
            try:
                analysis_result = run_inventory_analysis()

                if analysis_result['status'] == 'success':
                    run_id = save_run(
                        input_filename=new_filename,
                        report_filename=analysis_result['filename'],
                        status='success',
                        agent_output=str(result_holder['crew_result']),
                        summary_data=analysis_result['summary_stats'],
                        items_data=analysis_result['items']
                    )

                    report_name = analysis_result['filename']
                    complete_data = {
                        'type': 'complete',
                        'run_id': run_id,
                        'download_url': f'/download/{report_name}',
                        'filename': report_name,
                        'timestamp': datetime.now().isoformat()
                    }
                    yield f"data: {json.dumps(complete_data)}\n\n"
                else:
                    error_data = {
                        'type': 'error',
                        'content': analysis_result.get('message', 'Analysis failed'),
                        'timestamp': datetime.now().isoformat()
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"

            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'content': str(e), 'timestamp': datetime.now().isoformat()})}\n\n"

    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
        'Connection': 'keep-alive'
    })
