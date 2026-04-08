# src/db.py
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'inventory.db')


def get_connection():
    """Get a database connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            input_filename TEXT NOT NULL,
            report_filename TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            agent_output TEXT,
            summary_json TEXT,
            out_of_stock_count INTEGER DEFAULT 0,
            low_stock_count INTEGER DEFAULT 0,
            critical_count INTEGER DEFAULT 0,
            total_items INTEGER DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            closing_balance REAL NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY (run_id) REFERENCES analysis_runs(id)
        )
    ''')

    conn.commit()
    conn.close()


def save_run(input_filename, report_filename, status, agent_output,
             summary_data, items_data):
    """
    Save a complete analysis run to the database.
    
    Args:
        input_filename: Name of the uploaded file
        report_filename: Name of the generated report
        status: 'success' or 'error'
        agent_output: Raw agent text output
        summary_data: Dict with counts (out_of_stock_count, low_stock_count, etc.)
        items_data: Dict with lists of items {out_of_stock: [...], low_stock: [...], critical: [...]}
    
    Returns:
        The run_id of the newly created run
    """
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()

    cursor.execute('''
        INSERT INTO analysis_runs 
            (timestamp, input_filename, report_filename, status, agent_output,
             summary_json, out_of_stock_count, low_stock_count, critical_count, total_items)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        input_filename,
        report_filename,
        status,
        agent_output,
        json.dumps(summary_data),
        summary_data.get('out_of_stock_count', 0),
        summary_data.get('low_stock_count', 0),
        summary_data.get('critical_count', 0),
        summary_data.get('total_items', 0)
    ))

    run_id = cursor.lastrowid

    # Save individual items for history/forecasting queries
    all_items = []
    for category, items in items_data.items():
        for item in items:
            all_items.append((
                run_id,
                item.get('Name', 'Unknown'),
                item.get('Closing Balance', 0),
                category
            ))

    if all_items:
        cursor.executemany('''
            INSERT INTO analysis_items (run_id, item_name, closing_balance, category)
            VALUES (?, ?, ?, ?)
        ''', all_items)

    conn.commit()
    conn.close()
    return run_id


def get_runs():
    """Get all analysis runs, most recent first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, timestamp, input_filename, report_filename, status,
               out_of_stock_count, low_stock_count, critical_count, total_items
        FROM analysis_runs
        ORDER BY timestamp DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_run(run_id):
    """Get a single run with full data including items."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM analysis_runs WHERE id = ?', (run_id,))
    run = cursor.fetchone()
    if not run:
        conn.close()
        return None

    run_dict = dict(run)
    if run_dict.get('summary_json'):
        run_dict['summary'] = json.loads(run_dict['summary_json'])

    # Get items grouped by category
    cursor.execute('''
        SELECT item_name, closing_balance, category 
        FROM analysis_items WHERE run_id = ?
    ''', (run_id,))
    items = cursor.fetchall()

    run_dict['items'] = {
        'out_of_stock': [],
        'low_stock': [],
        'critical': []
    }
    for item in items:
        item_dict = {'Name': item['item_name'], 'Closing Balance': item['closing_balance']}
        category = item['category']
        if category in run_dict['items']:
            run_dict['items'][category].append(item_dict)

    conn.close()
    return run_dict


def get_comparison(run_id_1, run_id_2):
    """Get two runs for side-by-side comparison."""
    run1 = get_run(run_id_1)
    run2 = get_run(run_id_2)

    if not run1 or not run2:
        return None

    delta = {
        'out_of_stock': run2['out_of_stock_count'] - run1['out_of_stock_count'],
        'low_stock': run2['low_stock_count'] - run1['low_stock_count'],
        'critical': run2['critical_count'] - run1['critical_count'],
        'total_items': run2['total_items'] - run1['total_items']
    }

    return {'run1': run1, 'run2': run2, 'delta': delta}


def get_item_history(item_name):
    """
    Get historical closing balances for a specific item across all runs.
    Used by the forecasting feature.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ar.timestamp, ai.closing_balance
        FROM analysis_items ai
        JOIN analysis_runs ar ON ai.run_id = ar.id
        WHERE ai.item_name = ? AND ar.status = 'success'
        ORDER BY ar.timestamp ASC
    ''', (item_name,))
    rows = cursor.fetchall()
    conn.close()
    return [{'timestamp': row['timestamp'], 'closing_balance': row['closing_balance']} for row in rows]
