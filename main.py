import sqlite3
import os
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP(name="Expense Tracker MCP")

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL,
            category TEXT,
            note TEXT,
            date TEXT
        )
    """
    )
    conn.commit()
    conn.close()


def run_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch:
        rows = cursor.fetchall()
        conn.close()
        return rows
    conn.commit()
    conn.close()


@mcp.tool
def add_expense(amount: float, category: str, note: str = ""):
    """Add a new expense entry into SQLite database."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    run_query(
        "INSERT INTO expenses (amount, category, note, date) VALUES (?, ?, ?, ?)",
        (amount, category, note, date_str),
    )
    return "Expense added successfully."


@mcp.tool
def list_expenses():
    """Return all expenses stored in the database."""
    rows = run_query("SELECT * FROM expenses", fetch=True)
    return [
        {"id": r[0], "amount": r[1], "category": r[2], "note": r[3], "date": r[4]}
        for r in rows
    ]


@mcp.tool
def total_expenses():
    """Return the total amount spent."""
    rows = run_query("SELECT SUM(amount) FROM expenses", fetch=True)
    total = rows[0][0] if rows[0][0] is not None else 0
    return {"total_spent": total}


@mcp.tool
def filter_by_category(category: str):
    """Return all expenses matching a category."""
    rows = run_query(
        "SELECT * FROM expenses WHERE LOWER(category) = LOWER(?)",
        (category,),
        fetch=True,
    )
    return [
        {"id": r[0], "amount": r[1], "category": r[2], "note": r[3], "date": r[4]}
        for r in rows
    ]


@mcp.tool
def filter_by_date(date: str):
    """
    Return expenses from a given date.
    Format: YYYY-MM-DD
    """
    rows = run_query(
        "SELECT * FROM expenses WHERE date LIKE ?", (f"{date}%",), fetch=True
    )
    return [
        {"id": r[0], "amount": r[1], "category": r[2], "note": r[3], "date": r[4]}
        for r in rows
    ]


if __name__ == "__main__":
    init_db()
    mcp.run()
