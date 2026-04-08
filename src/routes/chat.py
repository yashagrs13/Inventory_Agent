# src/routes/chat.py
from flask import Blueprint, request, jsonify
from crewai import Crew, Task, Process
from src.agents import data_analyst_agent

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/query', methods=['POST'])
def query_data():
    """Natural language query endpoint for Chat with Data feature."""
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_query = data['message']

    try:
        query_task = Task(
            description=f"""
            The user wants to know the following about their inventory database:
            "{user_query}"
            
            Use the 'Get Database Schema' tool to understand the database structure.
            Then use the 'Execute SQL Query' tool to fetch the necessary information.
            Finally, provide a clear, business-friendly answer based on the data you retrieved.
            If the query fails or returns no data, explain that nicely. 
            Do NOT show the raw SQL to the user unless they ask for it.
            """,
            expected_output="A clear, plain English answer to the user's query based on the database data.",
            agent=data_analyst_agent
        )

        chat_crew = Crew(
            agents=[data_analyst_agent],
            tasks=[query_task],
            process=Process.sequential,
            verbose=True
        )

        response = str(chat_crew.kickoff())

        return jsonify({
            "response": response
        })

    except Exception as e:
        return jsonify({"error": f"Error processing query: {str(e)}"}), 500
