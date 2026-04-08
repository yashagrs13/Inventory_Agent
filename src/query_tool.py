# src/query_tool.py
import sqlite3
from typing import List, Any
from crewai.tools import tool
from src.db import DB_PATH

@tool("Get Database Schema")
def get_database_schema() -> str:
    """
    Returns the schema of the inventory database. 
    Use this first to understand the tables and columns available before writing SQL queries.
    """
    schema = """
    Table: analysis_runs
    - id (INTEGER PRIMARY KEY)
    - timestamp (TEXT)
    - input_filename (TEXT)
    - status (TEXT)
    - out_of_stock_count (INTEGER)
    - low_stock_count (INTEGER)
    - critical_count (INTEGER)
    - total_items (INTEGER)

    Table: analysis_items (Contains individual item details for each run)
    - id (INTEGER PRIMARY KEY)
    - run_id (INTEGER) - Foreign key to analysis_runs.id
    - item_name (TEXT)
    - closing_balance (REAL)
    - category (TEXT) - e.g., 'out_of_stock', 'low_stock', 'critical'
    """
    return schema

@tool("Execute SQL Query")
def execute_sql_query(query: str) -> str:
    """
    Executes a read-only SQL query on the inventory database and returns the results.
    Input must be a valid SQL SELECT statement.
    Example: 'SELECT count(*) FROM analysis_items WHERE category = "out_of_stock"'
    """
    if "insert" in query.lower() or "update" in query.lower() or "delete" in query.lower() or "drop" in query.lower():
        return "Error: Only read-only (SELECT) queries are allowed."
        
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            return "No results found for this query."
            
        # Convert to list of dicts string representation
        results = [dict(row) for row in rows]
        
        # Limit output length to prevent token overflow if too many rows
        if len(results) > 50:
            return str(results[:50]) + f"\n... (and {len(results) - 50} more rows. Try to refine your query to limit results)"
            
        return str(results)
    except Exception as e:
        return f"SQL Error: {str(e)}"
    finally:
        if 'conn' in locals():
            conn.close()
