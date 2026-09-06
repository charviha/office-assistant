"""
it_asset_tools.py
------------------
Tools for employee-specific IT asset queries (laptops, monitors, phones,
etc. issued to an employee).
"""

from .data_loader import get_it_assets_df
from .employee_tools import get_employee_info

VALID_STATUSES = ["Assigned", "Under Repair", "Returned"]


def get_it_assets(employee_id: str, status: str = None) -> list:
    """
    Return IT assets issued to an employee, optionally filtered by status.

    Args:
        employee_id: e.g. "EMP014"
        status: optional filter — one of "Assigned", "Under Repair", "Returned".
                If omitted, returns all assets ever issued to the employee.

    Returns:
        List of asset dicts (empty list if none), or a single-item list
        [{"error": "..."}] if the employee doesn't exist or status is invalid.

    Example:
        >>> get_it_assets("EMP014")
        [
            {"asset_id": "AST0027", "asset_type": "Laptop", "brand_model": "Dell Latitude 5440",
             "serial_number": "SN-ABCD-12345678", "issued_date": "2023-04-10",
             "status": "Assigned", "warranty_expiry": "2026-04-10"}
        ]
    """
    employee = get_employee_info(employee_id)
    if "error" in employee:
        return [employee]
    if status is not None and status not in VALID_STATUSES:
        return [{"error": f"Invalid status '{status}'. Must be one of {VALID_STATUSES}."}]

    df = get_it_assets_df()
    result = df[df["employee_id"].str.upper() == str(employee_id).upper()]
    if status is not None:
        result = result[result["status"] == status]
    return result.to_dict(orient="records")
