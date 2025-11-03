import frappe
from frappe.utils import flt

def apply_tax_exemptions(doc, method=None):
    """
    Reduce taxable income using Employee Investment Declaration.
    This should be called on Salary Slip before submission (via hook or custom script).
    """

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

    # Calculate taxable income (cannot go below 0)
    taxable_income = max(gross - exemption, 0)
    doc.taxable_amount = taxable_income

    # Net pay remains gross minus all deductions
    doc.net_pay = gross - deductions

    frappe.msgprint(
        f"Applied Tax Exemption: ₹{exemption:,.2f}\n"
        f"Taxable Income after Exemption: ₹{taxable_income:,.2f}"
    )
