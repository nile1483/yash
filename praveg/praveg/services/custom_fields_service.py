import frappe

def create_or_update_custom_fields(custom_fields: list[dict]):
    """
    Create or update Custom Fields
    """

    for cf in custom_fields:
        try:
            # Validate minimum required keys
            if not cf.get("dt") or not cf.get("fieldname"):
                frappe.log_error(
                    title="Invalid Custom Field Definition",
                    message=str(cf)
                )
                continue

            name = frappe.db.exists(
                "Custom Field",
                {"dt": cf["dt"], "fieldname": cf["fieldname"]}
            )

            if name:
                doc = frappe.get_doc("Custom Field", name)

                # Update only changed values (idempotent)
                updated = False
                for key, value in cf.items():
                    if key == "doctype":
                        continue

                    if doc.get(key) != value:
                        doc.set(key, value)
                        updated = True

                if updated:
                    doc.flags.ignore_permissions = True
                    doc.save(ignore_permissions=True)
                    # print(
                    #     f"Updated Custom Field: {cf['dt']} → {cf['fieldname']}"
                    # )
                else:
                    pass
                    # frappe.logger().debug(
                    #     f"No changes for Custom Field: {cf['dt']} → {cf['fieldname']}"
                    # )

            else:
                doc = frappe.get_doc(cf)
                doc.insert(ignore_permissions=True)

                # print(
                #     f"Created Custom Field: {cf['dt']} → {cf['fieldname']}"
                # )

        except Exception:
            frappe.log_error(
                title=f"Custom Field Migration Failed: {cf.get('fieldname')}",
                message=frappe.get_traceback()
            )

    # Commit once for performance and safety
    frappe.db.commit()
    print("Custom Fields Migration Completed Successfully")