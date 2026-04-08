# src/audit_tool.py
import pandas as pd
from crewai.tools import tool

def perform_ledger_audit(filepath: str) -> dict:
    """
    Reads an Excel ledger file, looks for unusual transactions, 
    and returns a structured risk report.
    """
    try:
        df = pd.read_excel(filepath)
        
        # Clean basic column names if they exist, or attempt to find Debit/Credit
        cols = [c.lower() for c in df.columns]
        
        # We assume standard Tally Ledger columns might contain keywords: 
        # debit, credit, amount, particulars, date
        debit_col = next((c for c in df.columns if 'debit' in c.lower()), None)
        credit_col = next((c for c in df.columns if 'credit' in c.lower()), None)
        particulars_col = next((c for c in df.columns if 'particular' in c.lower() or 'name' in c.lower() or 'description' in c.lower()), None)
        date_col = next((c for c in df.columns if 'date' in c.lower()), None)

        if not debit_col and not credit_col:
            # Fallback for generic amount column
            amount_col = next((c for c in df.columns if 'amount' in c.lower() or 'value' in c.lower()), None)
            if not amount_col:
                return {
                    "status": "error",
                    "message": "Could not identify standard financial columns (Debit, Credit, or Amount) in the uploaded file."
                }
            df['Debit'] = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
            debit_col = 'Debit'
            credit_col = None
        else:
            if debit_col:
                df[debit_col] = pd.to_numeric(df[debit_col], errors='coerce').fillna(0)
            if credit_col:
                df[credit_col] = pd.to_numeric(df[credit_col], errors='coerce').fillna(0)

        # Basic Risk Rule 1: High Value Transactions
        threshold = 100000  # Assume 1 lakh as high threshold for demo purposes
        high_value_tx = []
        
        if debit_col:
            high_debits = df[df[debit_col] > threshold]
            for _, row in high_debits.iterrows():
                desc = row[particulars_col] if particulars_col else "Unknown"
                dt = row[date_col] if date_col else "Unknown"
                high_value_tx.append({"Type": "High Debit", "Date": str(dt), "Description": str(desc), "Amount": float(row[debit_col])})

        if credit_col:
            high_credits = df[df[credit_col] > threshold]
            for _, row in high_credits.iterrows():
                desc = row[particulars_col] if particulars_col else "Unknown"
                dt = row[date_col] if date_col else "Unknown"
                high_value_tx.append({"Type": "High Credit", "Date": str(dt), "Description": str(desc), "Amount": float(row[credit_col])})

        # Calculate totals
        total_debits = df[debit_col].sum() if debit_col else 0
        total_credits = df[credit_col].sum() if credit_col else 0
        total_transactions = len(df)

        # Discrepancy heuristic: Suspicious round numbers or missing particulars
        suspicious = []
        if particulars_col:
            missing_desc = df[df[particulars_col].isnull() | (df[particulars_col] == '')]
            if not missing_desc.empty:
                suspicious.append(f"Found {len(missing_desc)} transactions with missing descriptions.")

        result = {
            "status": "success",
            "total_transactions": total_transactions,
            "total_debits": float(total_debits),
            "total_credits": float(total_credits),
            "high_value_transactions": high_value_tx,
            "suspicious_patterns": suspicious,
            "message": f"Audit complete. Processed {total_transactions} records."
        }
        
        return result
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error parsing ledger file: {str(e)}"
        }

@tool("Ledger Audit Tool")
def analyze_ledger_tool(filepath: str) -> str:
    """
    Parses a financial ledger Excel file (from the given filepath) to calculate 
    totals, identify high-value/risky transactions, and spot missing data.
    """
    res = perform_ledger_audit(filepath)
    if res.get("status") == "error":
        return res["message"]
        
    summary = f"Total Transactions: {res['total_transactions']}\n"
    summary += f"Total Debits: {res['total_debits']}\n"
    summary += f"Total Credits: {res['total_credits']}\n\n"
    
    if res['high_value_transactions']:
        summary += f"High Value Transactions Detected ({len(res['high_value_transactions'])}):\n"
        for idx, tx in enumerate(res['high_value_transactions'][:10]): # Cap at 10 for LLM context
            summary += f"- {tx['Date']}: {tx['Type']} of {tx['Amount']} for '{tx['Description']}'\n"
    else:
        summary += "No extremely high value transactions detected.\n"
        
    if res['suspicious_patterns']:
        summary += "\nSuspicious Patterns:\n"
        for p in res['suspicious_patterns']:
            summary += f"- {p}\n"
            
    summary += "\nUse this data to write an audit risk summary."
    return summary
