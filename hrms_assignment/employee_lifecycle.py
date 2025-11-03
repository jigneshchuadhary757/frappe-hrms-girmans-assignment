import frappe
from frappe.model.document import Document
import base64
from frappe.utils.pdf import get_pdf

def update_employee_status(doc, method):

    # When employee is confirmed
    if doc.workflow_state == "Confirmed" and doc.status != "Active":
        doc.status = "Active"
        frappe.msgprint("✅ Employee has been confirmed and status updated to Active.")

    # When employee exits (was confirmed and active before)
    elif doc.workflow_state == "Exit" and doc.status == "Active":
        doc.status = "Left"
        frappe.msgprint("⚠️ Employee has exited. Experience Letter will be generated.")

        # Enqueue experience letter generation
        frappe.enqueue(generate_experience_letter, employee_name=doc.name)
        frappe.msgprint("📄 Experience Letter generation task has been queued.")


@frappe.whitelist()
def generate_experience_letter(employee_name):
    try:
        doc = frappe.get_doc("Employee", employee_name)

        html = f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6; font-size: 14px;">
            <h3 style="text-align:center;">Experience Letter</h3>
            <p>Date: {frappe.utils.nowdate()}</p>
            <p>To Whom It May Concern,</p>

            <p>This is to certify that <b>{doc.employee_name}</b> worked at our organization from 
            <b>{doc.date_of_joining}</b> to <b>{doc.relieving_date or "Present"}</b> 
            as a <b>{doc.designation or "Employee"}</b>.</p>

            <p>During their tenure, their performance was satisfactory and they were a valuable member of our team.</p>

            <p>We wish them all the best in their future endeavors.</p>

            <p style="margin-top:40px;">HR Manager<br><b>{frappe.defaults.get_global_default('company') or 'Company Name'}</b></p>
        </div>
        """

        # Generate PDF from HTML
        pdf_content = get_pdf(html)

        # Encode PDF content to base64
        encoded_pdf = base64.b64encode(pdf_content).decode()

        #  Create a File document
        file_doc = frappe.get_doc({
            "doctype": "File",
            "file_name": f"Experience_Letter_{doc.name}.pdf",
            "attached_to_doctype": "Employee",
            "attached_to_name": doc.name,
            "is_private": 1,
            "content": encoded_pdf,
            "decode": True  
        })
        file_doc.insert(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(f"Experience letter generated for {employee_name}")
        frappe.msgprint(f"📄 Experience Letter has been generated and attached for Employee {employee_name}.")

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), f"Error generating Experience Letter for {employee_name}")
