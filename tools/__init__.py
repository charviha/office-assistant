"""
tools package
-------------
Employee-specific data tools for the TechNova Office Assistant.

Person 3 (Agent/Orchestration) should import everything needed from here:

    from tools import (
        get_employee_info, search_employee_by_name, get_manager_info,
        get_leave_balance, apply_leave,
        get_expense_status, get_expense_summary, submit_expense,
        get_it_assets,
        get_office_location, get_employee_office, list_locations_by_city,
    )

All read tools return either:
  - a dict (single-record lookups), or
  - a list of dicts (multi-record lookups)
On failure, they return {"error": "<reason>"} (or [{"error": "..."}] for
list-returning tools) instead of raising an exception, so the agent can
safely pass the result straight to the LLM as a tool result.

Action tools (apply_leave, submit_expense) write back to the CSVs and
return {"success": True, ...} on success or {"error": "..."} on failure.
"""

from .employee_tools import get_employee_info, search_employee_by_name, get_manager_info
from .leave_tools import get_leave_balance, apply_leave
from .expense_tools import get_expense_status, get_expense_summary, submit_expense
from .it_asset_tools import get_it_assets
from .location_tools import get_office_location, get_employee_office, list_locations_by_city

__all__ = [
    "get_employee_info",
    "search_employee_by_name",
    "get_manager_info",
    "get_leave_balance",
    "apply_leave",
    "get_expense_status",
    "get_expense_summary",
    "submit_expense",
    "get_it_assets",
    "get_office_location",
    "get_employee_office",
    "list_locations_by_city",
]
