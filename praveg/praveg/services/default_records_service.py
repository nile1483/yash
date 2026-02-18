import frappe

# def load_default_records_from_folder(folder_path):
#     for file in os.listdir(folder_path):
#         if file.endswith(".json"):
#             data = load_json(os.path.join(folder_path, file))
#             insert_records(data)

def create_default_records(data: list[dict]):
    for item in data:
        doctype = item.get("doctype")
        records = item.get("records", [])

        for record in records:
            if not frappe.db.exists(doctype, record):
                doc = frappe.get_doc({
                    "doctype": doctype,
                    **record
                })
                doc.insert(ignore_permissions=True)

    frappe.db.commit()
    print("Default records created successfully.")
