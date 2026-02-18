import frappe

def create_doctypes(configs: list[dict]):
    """
    Create multiple doctypes safely from config
    """
    for config in configs:
        doctype_name = config.get("name")

        if not doctype_name:
            frappe.throw("Doctype name is required")

        if frappe.db.exists("DocType", doctype_name):
            continue  # already exists → patch-safe

        doc = frappe.get_doc({
            "doctype": "DocType",
            "custom": 1,
            **config
        })

        doc.insert(ignore_permissions=True)

    frappe.db.commit()
    print("Doctypes migrated successfully")