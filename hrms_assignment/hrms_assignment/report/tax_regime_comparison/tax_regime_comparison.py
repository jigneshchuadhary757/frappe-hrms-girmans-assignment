# Copyright (c) 2025, Jignesh Chaudhary and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
    columns, data = get_columns(), []
    
    employees = frappe.get_all(
        "Employee",
        fields=["name", "employee_name", "custom_tax_regime_preference"]
    )

    for emp in employees:
        old_tax = get_tax_deduction(emp.name, "Old Regime Structure")
        new_tax = get_tax_deduction(emp.name, "New Regime Structure")

        data.append([
            emp.name,
            emp.employee_name,
            emp.custom_tax_regime_preference or "Not Set",
            old_tax,
            new_tax,
            "Old" if old_tax < new_tax else "New" if new_tax < old_tax else "Same"
        ])

    return columns, data


def get_columns():
    return [
        {"label": "Employee ID", "fieldname": "employee", "fieldtype": "Link", "options": "Employee", "width": 150},
        {"label": "Employee Name", "fieldname": "employee_name", "fieldtype": "Data", "width": 180},
        {"label": "Selected Regime", "fieldname": "custom_tax_regime_preference", "fieldtype": "Data", "width": 130},
        {"label": "Old Regime Tax (₹)", "fieldname": "old_tax", "fieldtype": "Currency", "width": 150},
        {"label": "New Regime Tax (₹)", "fieldname": "new_tax", "fieldtype": "Currency", "width": 150},
        {"label": "Better Option", "fieldname": "better_option", "fieldtype": "Data", "width": 120},
    ]


def get_tax_deduction(employee, structure_name):
    """Fetch total deduction for the given employee and salary structure."""
    total_deduction = 0

    salary_slip = frappe.db.get_value(
        "Salary Slip",
        {"employee": employee, "salary_structure": structure_name},
        "name"
    )

    if salary_slip:
        deductions = frappe.db.get_all(
            "Salary Detail",
            filters={"parent": salary_slip, "parentfield": "deductions"},
            fields=["amount"]
        )
        total_deduction = sum([d.amount for d in deductions])

    return total_deduction
