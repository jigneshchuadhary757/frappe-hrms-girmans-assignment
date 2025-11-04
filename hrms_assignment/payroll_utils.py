import frappe
from frappe.utils import flt

def apply_tax_exemptions(doc, method=None):
    if not getattr(doc, "employee", None):
        return

    # Fetch the total investment declaration for the employee
    inv = frappe.db.get_value(
        "Employee Investment Declaration",
        {"employee": doc.employee},
        ["total_investment"],
        as_dict=True
    )

    exemption = flt(inv.total_investment) if inv else 0
    gross = flt(doc.gross_pay or sum(flt(e.amount) for e in (doc.earnings or [])))
    deductions = flt(doc.total_deduction or 0)

    taxable_income = max(gross - exemption, 0)
    doc.taxable_amount = taxable_income

    doc.net_pay = gross - deductions

    frappe.msgprint(
        f"Applied Tax Exemption: ₹{exemption:,.2f}\n"
        f"Taxable Income after Exemption: ₹{taxable_income:,.2f}"
    )


def assign_salary_structure_based_on_regime(doc, method):
    if not doc.employees:
        frappe.msgprint("No employees found in this Payroll Entry.")
        return

    regime_to_structure = {
        "Old Regime Structure": "Old Regime Structure",
        "New Regime Structure": "New Regime Structure"
    }

    for row in doc.employees:
        if not row.employee:
            continue

        emp = frappe.get_doc("Employee", row.employee)
        regime = emp.get("custom_tax_regime_preference")  # ✅ Use custom fieldname here

        if not regime:
            frappe.msgprint(f"Tax Regime Preference not set for {emp.employee_name} ({emp.name}).")
            continue

        structure_name = regime_to_structure.get(regime)

        if not structure_name:
            frappe.msgprint(f"No salary structure mapping found for regime '{regime}'.")
            continue

        is_active = frappe.db.exists("Salary Structure", {"name": structure_name, "is_active": 1})
        if is_active:
            row.salary_structure = structure_name
        else:
            frappe.msgprint(
                f"No active Salary Structure found for regime '{regime}' "
                f"for Employee {emp.employee_name} ({emp.name})."
            )
