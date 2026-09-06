"""
employee_tools.py
------------------
Tools for looking up basic employee information. These are usually called
first by the agent to validate an employee_id before calling the more
specific tools (leave, expenses, IT assets).
"""

from .data_loader import get_employees_df


def get_employee_info(employee_id: str) -> dict:
    """
    Return basic profile information for a single employee.

    Args:
        employee_id: e.g. "EMP014"

    Returns:
        dict with employee fields, or {"error": "..."} if not found.

    Example:
        >>> get_employee_info("EMP014")
        {
            "employee_id": "EMP014",
            "name": "Riya Kapoor",
            "email": "riya.kapoor@technova.com",
            "department": "Engineering",
            "designation": "Tech Lead",
            "location_id": "L012",
            "manager_id": "EMP009",
            "date_of_joining": "2021-03-15",
            "employment_type": "Full-Time",
            "status": "Active"
        }
    """
    df = get_employees_df()
    row = df[df["employee_id"].str.upper() == str(employee_id).upper()]
    if row.empty:
        return {"error": f"Employee ID '{employee_id}' not found."}
    return row.iloc[0].to_dict()


def search_employee_by_name(name: str) -> list:
    """
    Find employees whose name contains the given text (case-insensitive).
    Useful when a user says "what's Riya's leave balance" instead of an ID.

    Args:
        name: full or partial name, e.g. "Riya"

    Returns:
        List of matching employee dicts (each with employee_id, name,
        department, designation). Empty list if no match.

    Example:
        >>> search_employee_by_name("Riya")
        [{"employee_id": "EMP014", "name": "Riya Kapoor", "department": "Engineering", "designation": "Tech Lead"}]
    """
    df = get_employees_df()
    matches = df[df["name"].str.contains(name, case=False, na=False)]
    cols = ["employee_id", "name", "department", "designation"]
    return matches[cols].to_dict(orient="records")


def get_manager_info(employee_id: str) -> dict:
    """
    Return the profile of an employee's manager.

    Args:
        employee_id: e.g. "EMP014"

    Returns:
        dict with the manager's profile, or {"error": "..."} if the
        employee or manager cannot be found / employee has no manager.

    Example:
        >>> get_manager_info("EMP014")
        {"employee_id": "EMP009", "name": "Aditya Rao", "designation": "Engineering Manager", ...}
    """
    employee = get_employee_info(employee_id)
    if "error" in employee:
        return employee
    manager_id = employee.get("manager_id")
    if not manager_id or (isinstance(manager_id, float)):
        return {"error": f"Employee '{employee_id}' has no manager on record."}
    return get_employee_info(manager_id)
