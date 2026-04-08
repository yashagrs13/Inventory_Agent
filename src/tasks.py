# src/tasks.py
from crewai import Task
from src.agents import stock_analyst_agent, report_creator_agent

# --- The Analysis Task ---
# This task instructs the analyst agent to use its tool.
analysis_task = Task(
    description="""
    Use the Inventory Analysis and Reporting Tool to process the latest Tally data. 
    The tool is located in the 'data' directory. The final report should be saved in the 'reports' directory.
    Your final answer MUST be the success or error message returned by the tool.
    """,
    expected_output="A confirmation message indicating that the Excel report has been successfully created, including the filename.",
    agent=stock_analyst_agent
)

# --- The Reporting Task ---
# This task takes the result from the analysis and summarizes it.
reporting_task = Task(
    description="""
    Review the confirmation message from the inventory analysis. 
    Based on this message, write a brief, one-paragraph summary for the business owner. 
    If the report was created successfully, state this clearly and mention the filename. 
    If there was an error, clearly state the error message.
    """,
    expected_output="A concise paragraph summarizing the outcome of the inventory analysis.",
    agent=report_creator_agent,
    context=[analysis_task]  # This makes it dependent on the first task
)