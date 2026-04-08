# src/agents.py
from crewai import Agent
from src.llm_config import llm
from src.tools import inventory_analysis_tool

# --- The Analyst Agent ---
stock_analyst_agent = Agent(
    role="Inventory Analyst",
    goal="""Analyze the current inventory status based on the latest Tally ERP data exports. 
    Identify all out-of-stock and low-stock items accurately.""",
    backstory="""You are a meticulous Inventory Analyst with a knack for numbers. 
    You are an expert at using data analysis tools to uncover critical inventory insights 
    and ensuring the business never runs out of essential stock.""",
    tools=[inventory_analysis_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# --- The Reporting Agent ---
report_creator_agent = Agent(
    role="Business Reporter",
    goal="""Create a clear, concise, and actionable summary of the inventory analysis findings. 
    The summary should be easy for a business owner to understand.""",
    backstory="""You are a Business Reporter who specializes in creating reports for executives. 
    You know how to present data in a way that is straightforward and highlights the most 
    important information, enabling quick decision-making.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# --- The Comparison Agent ---
comparison_analyst = Agent(
    role="Inventory Comparison Analyst",
    goal="""Compare two inventory analysis snapshots and provide a clear, insightful narrative 
    about what changed, whether the situation improved or worsened, and what the business 
    owner should pay attention to.""",
    backstory="""You are an experienced Inventory Comparison Analyst who tracks inventory 
    health over time. You excel at spotting trends, identifying improvements or deterioration 
    in stock levels, and communicating these changes in plain business language. You always 
    highlight the most important changes first and provide actionable context.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

from src.query_tool import get_database_schema, execute_sql_query

# --- The Data Query Agent ---
data_analyst_agent = Agent(
    role="Inventory Data Analyst",
    goal="""Answer natural language queries about the user's inventory by translating them 
    into SQL, executing them against the database, and providing a plain-English response.""",
    backstory="""You are a Data Analyst specialized in inventory. You know how to take a loose 
    business question like 'Which items are critical in the latest run?', look up the database 
    schema, write an accurate SQL query, execute it, and interpret the results back to the user clearly.""",
    tools=[get_database_schema, execute_sql_query],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

from src.forecast_tool import forecast_item_tool

# --- The Trend Forecasting Agent ---
forecast_agent = Agent(
    role="Inventory Demand Forecaster",
    goal="""Analyze historical stock data using linear regression to predict when items will run out of stock.
    Provide data-backed predictions for inventory burn rates.""",
    backstory="""You are a Data Scientist focusing on supply chain forecasting. You use scikit-learn models 
    to map out inventory depletion trends and alert managers to items that are quietly burning towards zero 
    before they actually run out.""",
    tools=[forecast_item_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

from src.email_tool import send_email_alert

# --- The Smart Reorder Alert Agent ---
reorder_agent = Agent(
    role="Purchasing Manager",
    goal="""Review the latest critical stock items and pro-actively generate reorder alerts using the 
    send_email_alert tool. Notify the business owner or supplier of what needs immediate restocking.""",
    backstory="""You are a Purchasing Manager responsible for supply chain continuity. 
    You monitor stock levels and when items hit critical lows, you immediately draft and send out 
    reorder requests via email to ensure operations don't halt.""",
    tools=[send_email_alert],
    llm=llm,
    verbose=True,
    allow_delegation=False
)

from src.audit_tool import analyze_ledger_tool

# --- The Ledger Audit Agent ---
audit_agent = Agent(
    role="Financial Compliance Auditor",
    goal="""Analyze financial ledgers to identify discrepancies, high-value risk transactions, 
    and unusual patterns. Summarize the financial risk for the business owner.""",
    backstory="""You are a strict and meticulous Financial Auditor. You excel at taking raw ledger data 
    and turning it into an executive risk summary, highlighting anything that looks suspicious or requires 
    further human review.""",
    tools=[analyze_ledger_tool],
    llm=llm,
    verbose=True,
    allow_delegation=False
)
