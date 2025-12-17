# Expense Tracker MCP Server

A simple expense tracking server built with FastMCP. Helps you keep track of your spending through natural conversations with AI assistants like Claude.

## What it does

This server lets you:
- Add expenses with date, amount, category, and notes
- List expenses within a date range
- Get spending summaries by category
- View predefined expense categories

All your expense data is stored locally in a SQLite database.

## Quick Start

**Install dependencies:**
```bash
pip install fastmcp aiosqlite
```

**Run the server:**
```bash
python main.py
```

The server starts on `http://0.0.0.0:8000` by default.

## Using with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "expenses": {
      "command": "python",
      "args": ["/full/path/to/expense_tracker_mcp_server/main.py"]
    }
  }
}
```

Then you can chat with Claude like:
- "Add a $45 expense for groceries today"
- "Show me all my expenses from last week"
- "How much did I spend on food this month?"

## Available Tools

### add_expense
Adds a new expense to your tracker.

```python
add_expense(
    date="2024-12-17",      # Format: YYYY-MM-DD
    amount=45.50,            # Any number
    category="Food & Dining",
    subcategory="Groceries", # Optional
    note="Weekly shopping"   # Optional
)
```

### list_expenses
Shows expenses between two dates.

```python
list_expenses(
    start_date="2024-12-01",
    end_date="2024-12-17"
)
```

### summarize
Groups expenses by category and shows totals.

```python
summarize(
    start_date="2024-12-01",
    end_date="2024-12-17",
    category="Food & Dining"  # Optional filter
)
```

## Default Categories

The server includes these categories out of the box:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Travel
- Education
- Business
- Other

You can customize categories by creating a `categories.json` file in the project directory.

## How it works

Expenses are stored in `expenses.db` (SQLite) in your system's temp directory. The database is created automatically when you first run the server. On Windows, this is usually `C:\Users\YourName\AppData\Local\Temp\expenses.db`.

The server uses async operations so it can handle multiple requests efficiently.

## Troubleshooting

**"Database is in read-only mode"**
The temp directory might not be writable. Try running with elevated permissions or check the `DB_PATH` in the code.

**Can't connect to server**
Make sure port 8000 isn't already in use. You can change the port in `main.py` if needed.

**Claude can't see the tools**
Double-check the path in your `claude_desktop_config.json` is absolute and points to `main.py`.

## Built with

- [FastMCP](https://github.com/jlowin/fastmcp) - Makes building MCP servers easy
- [aiosqlite](https://github.com/omnilib/aiosqlite) - Async SQLite wrapper
- SQLite - Local database storage

## License

MIT