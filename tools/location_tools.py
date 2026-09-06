"""
location_tools.py
------------------
Tools for office location lookups — either directly by location_id, or
by resolving an employee's own office location.
"""

from .data_loader import get_office_locations_df
from .employee_tools import get_employee_info


def get_office_location(location_id: str) -> dict:
    """
    Return details for a specific office location.

    Args:
        location_id: e.g. "L012"

    Returns:
        dict with city, address, facilities, seating capacity, etc.,
        or {"error": "..."} if not found.

    Example:
        >>> get_office_location("L012")
        {"location_id": "L012", "city": "Bengaluru", "floor": "Floor 2", ...}
    """
    df = get_office_locations_df()
    row = df[df["location_id"].str.upper() == str(location_id).upper()]
    if row.empty:
        return {"error": f"Office location ID '{location_id}' not found."}
    return row.iloc[0].to_dict()


def get_employee_office(employee_id: str) -> dict:
    """
    Return the office location details for a given employee (resolves the
    employee's location_id, then looks it up).

    Args:
        employee_id: e.g. "EMP014"

    Returns:
        dict with the employee's office details, or {"error": "..."} if
        the employee or their location can't be found.

    Example:
        >>> get_employee_office("EMP014")
        {"location_id": "L012", "city": "Bengaluru", "floor": "Floor 2",
         "address": "204, MG Road, Bengaluru", "facilities": "Cafeteria, Parking, Gym", ...}
    """
    employee = get_employee_info(employee_id)
    if "error" in employee:
        return employee
    return get_office_location(employee["location_id"])


def list_locations_by_city(city: str) -> list:
    """
    Return all office locations (floors/buildings) in a given city.

    Args:
        city: e.g. "Chennai"

    Returns:
        List of location dicts in that city (empty list if none found).

    Example:
        >>> list_locations_by_city("Chennai")
        [{"location_id": "L001", "city": "Chennai", "floor": "Floor 1", ...}, ...]
    """
    df = get_office_locations_df()
    result = df[df["city"].str.lower() == city.lower()]
    return result.to_dict(orient="records")
