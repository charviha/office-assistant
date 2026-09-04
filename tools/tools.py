import csv
from pathlib import Path

from rag.retriever import retrieve


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_DIR = BASE_DIR / "data" / "database"


def search_policy(query):
    """
    Search company policy documents using the RAG system.
    """

    results = retrieve(query, top_k=3)

    if not results:
        return "No relevant policy information was found."

    response = []

    for result in results:
        response.append(
            f"Source: {result['source']}\n"
            f"Page: {result['page']}\n"
            f"{result['text']}"
        )

    return "\n\n-----------------------------\n\n".join(response)


def get_employee_info(employee_id):
    """
    Retrieve employee information from employees.csv.
    """

    file_path = DATABASE_DIR / "employees.csv"

    if not file_path.exists():
        return "Employee database was not found."

    with open(file_path, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            if row.get("employee_id") == str(employee_id):
                return row

    return f"No employee found with ID {employee_id}."


def get_leave_balance(employee_id):
    """
    Retrieve leave balance from leave_balance.csv.
    """

    file_path = DATABASE_DIR / "leave_balance.csv"

    if not file_path.exists():
        return "Leave balance database was not found."

    with open(file_path, "r", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for row in reader:

            if row.get("employee_id") == str(employee_id):
                return row

    return f"No leave information found for employee {employee_id}."
