"""
expense_tools.py
-----------------
Tools for employee-specific expense queries and for submitting a new
expense claim (action tool).
"""

import os
from datetime import date
from .data_loader import get_expense_records_df, DATA_DIR, reload_all
from .employee_tools import get_employee_info

VALID_CATEGORIES = [
    "Travel", "Client Meal", "Accommodation", "Internet Reimbursement",
    "Office Supplies", "Training/Certification", "Mobile Bill", "Cab/Local Conveyance",
]
VALID_STATUSES = ["Approved", "Pending", "Rejected", "Reimbursed"]


def get_expense_status(employee_id: str, status: str = None) -> list:
    """
    Return expense records for an employee, optionally filtered by status.

    Args:
        employee_id: e.g. "EMP014"
        status: optional filter — one of "Approved", "Pending", "Rejected",
                "Reimbursed". If omitted, returns all records.

    Returns:
        List of expense record dicts (empty list if none match), or a
        single-item list [{"error": "..."}] if the employee doesn't exist
        or status is invalid.

    Example:
        >>> get_expense_status("EMP014", status="Pending")
        [{"expense_id": "EXP0031", "category": "Travel", "amount": 4500, ...}]
    """
    employee = get_employee_info(employee_id)
    if "error" in employee:
        return [employee]
    if status is not None and status not in VALID_STATUSES:
        return [{"error": f"Invalid status '{status}'. Must be one of {VALID_STATUSES}."}]

    df = get_expense_records_df()
    result = df[df["employee_id"].str.upper() == str(employee_id).upper()]
    if status is not None:
        result = result[result["status"] == status]
    return result.to_dict(orient="records")


def get_expense_summary(employee_id: str) -> dict:
    """
    Return a quick aggregate summary of an employee's expenses by status.

    Args:
        employee_id: e.g. "EMP014"

    Returns:
        dict with total claimed amount and counts per status, or
        {"error": "..."} if the employee doesn't exist.

    Example:
        >>> get_expense_summary("EMP014")
        {
            "employee_id": "EMP014",
            "total_claims": 5,
            "total_amount": 18500,
            "by_status": {"Approved": 2, "Pending": 1, "Rejected": 1, "Reimbursed": 1}
        }
    """
    employee = get_employee_info(employee_id)
    if "error" in employee:
        return employee

    df = get_expense_records_df()
    result = df[df["employee_id"].str.upper() == str(employee_id).upper()]
    if result.empty:
        return {
            "employee_id": employee_id,
            "total_claims": 0,
            "total_amount": 0,
            "by_status": {},
        }
    return {
        "employee_id": employee_id,
        "total_claims": int(len(result)),
        "total_amount": float(result["amount"].sum()),
        "by_status": result["status"].value_counts().to_dict(),
    }


def submit_expense(employee_id: str, category: str, amount: float, description: str = "") -> dict:
    """
    Submit a new expense claim. Writes a new row to expense_records.csv
    with status "Pending" and today's date. This is an ACTION tool.

    Args:
        employee_id: e.g. "EMP014"
        category: one of VALID_CATEGORIES (e.g. "Travel", "Client Meal")
        amount: claim amount in INR (positive number)
        description: optional free-text description

    Returns:
        dict with the created expense record, or {"error": "..."} if
        employee_id/category/amount is invalid.

    Example:
        >>> submit_expense("EMP014", "Travel", 3200, "Client visit - Mumbai")
        {
            "success": True,
            "expense_id": "EXP0091",
            "status": "Pending",
            "message": "Expense claim EXP0091 submitted for approval."
        }
    """
    employee = get_employee_info(employee_id)
    if "error" in employee:
        return employee
    if category not in VALID_CATEGORIES:
        return {"error": f"Invalid category '{category}'. Must be one of {VALID_CATEGORIES}."}
    if not isinstance(amount, (int, float)) or amount <= 0:
        return {"error": "amount must be a positive number."}

    df = get_expense_records_df()
    next_num = len(df) + 1
    expense_id = f"EXP{next_num:04d}"
    today = date.today().isoformat()

    new_row = {
        "expense_id": expense_id,
        "employee_id": employee_id,
        "category": category,
        "amount": amount,
        "currency": "INR",
        "expense_date": today,
        "submitted_date": today,
        "status": "Pending",
        "description": description or f"{category} expense",
        "approver_id": employee.get("manager_id", ""),
    }
    df.loc[len(df)] = new_row

    df.to_csv(os.path.join(DATA_DIR, "expense_records.csv"), index=False)
    reload_all()

    return {
        "success": True,
        "expense_id": expense_id,
        "status": "Pending",
        "message": f"Expense claim {expense_id} submitted for approval.",
    }
