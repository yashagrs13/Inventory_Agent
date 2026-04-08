# main.py
import os
from dotenv import load_dotenv
from crewai import Crew, Process
from src.agents import stock_analyst_agent, report_creator_agent
from src.tasks import analysis_task, reporting_task

# Load environment variables from .env file
load_dotenv()

# --- Assemble the Crew ---
inventory_crew = Crew(
    agents=[stock_analyst_agent, report_creator_agent],
    tasks=[analysis_task, reporting_task],
    process=Process.sequential,
    verbose=True
)

# --- Kick off the process ---
if __name__ == "__main__":
    print("Starting the Inventory Analysis Crew...")
    
    # Before running, make sure the 'data' and 'reports' folders exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('reports', exist_ok=True)
    
    print("\nReminder: Please ensure your latest Tally exports are in the 'data' folder.")
    print("Example filenames: 'Stock_Summary_2025-09-21.xlsx'\n")
    
    result = inventory_crew.kickoff()
    
    print("\n--------------------------------------------------")
    print("Inventory Analysis Crew finished its work.")
    print("Final Report Summary:")
    print(result)
    print("--------------------------------------------------")