import frappe

def create_or_update_property_setters(configs: list[dict]):
    """
    Create / Update Property Setter records from config
    Patch-safe, production-safe, config-driven
    """

    for config in configs:
        required = ["doc_type", "property", "property_type", "value"]
        for key in required:
            if key not in config:
                frappe.throw(f"Missing required key: {key}")

        try:
            name = frappe.db.exists("Property Setter", {**config})

            if name:
                # Update existing (PATCH SAFE)
                doc = frappe.get_doc("Property Setter", name)
                for key, value in config.items():
                    if key not in ("doctype"):
                        setattr(doc, key, value)

                doc.save(ignore_permissions=True)

            else:
                # Create new
                doc = frappe.get_doc({
                    "doctype": "Property Setter",
                    **config
                })
                doc.insert(ignore_permissions=True)

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Property Setter Setup Failed"
            )
            raise

    frappe.db.commit()
    print("Property Setters migrated successfully")
