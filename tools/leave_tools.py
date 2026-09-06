"""
leave_tools.py
--------------
Tools for employee-specific leave balance queries and for applying leave
(a simple "action" tool, demonstrating that the agent can not just fetch
data but also initiate a routine task).
"""

import os
import pandas as pd
from .data_loader import get_leave_balance_df, DATA_DIR, reload_all
from .employee_tools import get_employee_info

VALID_LEAVE_TYPES = {
    "casual": "casual_leave",
    "earned": "earned_leave",
    "sick": "sick_leave",
}


def get_leave_balance(employee_id: str) -> dict:
    """
    Return an employee's leave balance for the current leave year.

    Args:
        employee_id: e.g. "EMP014"

    Returns:
        dict with casual/earned/sick leave totals, used, and remaining,
        or {"error": "..."} if the employee has no leave record.

    Example:
        >>> get_leave_balance("EMP014")
        {
            "employee_id": "EMP014",
            "leave_year": 2026,
            "casual_leave": {"total": 12, "used": 4, "remaining": 8},
            "earned_leave": {"total": 15, "used": 3, "remaining": 12},
            "sick_leave": {"total": 10, "used": 2, "remaining": 8},
            "wfh_days_used_this_month": 3
        }
    """
    df = get_leave_balance_df()
    row = df[df["employee_id"].str.upper() == str(employee_id).upper()]
    if row.empty:
        return {"error": f"No leave record found for employee ID '{employee_id}'."}
    r = row.iloc[0]
    return {
        "employee_id": r["employee_id"],
        "leave_year": int(r["leave_year"]),
        "casual_leave": {
            "total": int(r["casual_leave_total"]),
            "used": int(r["casual_leave_used"]),
            "remaining": int(r["casual_leave_remaining"]),
        },
        "earned_leave": {
            "total": int(r["earned_leave_total"]),
            "used": int(r["earned_leave_used"]),
            "remaining": int(r["earned_leave_remaining"]),
        },
        "sick_leave": {
            "total": int(r["sick_leave_total"]),
            "used": int(r["sick_leave_used"]),
            "remaining": int(r["sick_leave_remaining"]),
        },
        "wfh_days_used_this_month": int(r["wfh_days_used_this_month"]),
    }


def apply_leave(employee_id: str, leave_type: str, days: int) -> dict:
    """
    Apply for leave: validates balance and, if sufficient, deducts the
    requested days and writes the update back to leave_balance.csv.

    This is an ACTION tool (it changes data), unlike get_leave_balance
    which is read-only. The agent should confirm details with the user
    before calling this.

    Args:
        employee_id: e.g. "EMP014"
        leave_type: one of "casual", "earned", "sick"
        days: number of days to apply for (positive integer)

    Returns:
        dict with the outcome and updated balance, or {"error": "..."}
        if the employee/leave_type is invalid or balance is insufficient.

    Example:
        >>> apply_leave("EMP014", "casual", 2)
        {
            "success": True,
            "message": "Applied 2 casual leave day(s) for EMP014.",
            "updated_balance": {"total": 12, "used": 6, "remaining": 6}
        }
    """
    if leave_type not in VALID_LEAVE_TYPES:
        return {"error": f"Invalid leave_type '{leave_type}'. Must be one of {list(VALID_LEAVE_TYPES)}."}
    if not isinstance(days, int) or days <= 0:
        return {"error": "days must be a positive integer."}

    employee = get_employee_info(employee_id)
    if "error" in employee:
        return employee

    df = get_leave_balance_df()
    mask = df["employee_id"].str.upper() == str(employee_id).upper()
    if not mask.any():
        return {"error": f"No leave record found for employee ID '{employee_id}'."}

    prefix = VALID_LEAVE_TYPES[leave_type]
    remaining_col = f"{prefix}_remaining"
    used_col = f"{prefix}_used"
    total_col = f"{prefix}_total"

    idx = df[mask].index[0]
    remaining = df.at[idx, remaining_col]
    if days > remaining:
        return {
            "error": (
                f"Insufficient {leave_type} leave balance for {employee_id}: "
                f"requested {days}, only {int(remaining)} remaining."
            )
        }

    df.at[idx, used_col] = int(df.at[idx, used_col]) + days
    df.at[idx, remaining_col] = int(df.at[idx, remaining_col]) - days

    # Persist back to CSV (this is the "database write" for the demo)
    df.to_csv(os.path.join(DATA_DIR, "leave_balance.csv"), index=False)
    reload_all()  # clear cache so subsequent reads see the update

    return {
        "success": True,
        "message": f"Applied {days} {leave_type} leave day(s) for {employee_id}.",
        "updated_balance": {
            "total": int(df.at[idx, total_col]),
            "used": int(df.at[idx, used_col]),
            "remaining": int(df.at[idx, remaining_col]),
        },
    }
