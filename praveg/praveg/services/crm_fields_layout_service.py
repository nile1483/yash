import frappe
import json
from .utils_service import load_json
import os

BASE_DIR = os.path.dirname(__file__)
BASE_FILE_PATH = os.path.join(BASE_DIR, ".." , "setup" , "data")

def create_default_fields_layout():
    crm_lead_default_layout()
    crm_deal_default_layout()
    
    frappe.db.commit()
    print("CRM Fields Layout migrated Successfully")
    
def crm_lead_default_layout():
    quick_entry_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_quick_entry_layout.json"))
    data_fields_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_data_fields_layout.json"))
    side_panel_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_side_panel_layout.json"))
    
    create_or_update_crm_fields_layout("CRM Lead", "Quick Entry", quick_entry_layout)
    create_or_update_crm_fields_layout("CRM Lead", "Data Fields", data_fields_layout)
    create_or_update_crm_fields_layout("CRM Lead", "Side Panel", side_panel_layout)
    
def crm_deal_default_layout():
    quick_entry_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_quick_entry_layout.json"))
    data_fields_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_data_fields_layout.json"))
    side_panel_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_side_panel_layout.json"))
    
    create_or_update_crm_fields_layout("CRM Deal", "Quick Entry", quick_entry_layout)
    create_or_update_crm_fields_layout("CRM Deal", "Data Fields", data_fields_layout)
    create_or_update_crm_fields_layout("CRM Deal", "Side Panel", side_panel_layout)
    
def create_or_update_crm_fields_layout(dt=str, type=str, layout=dict):
    if type != "Side Panel":
        remove_fields = set(layout.get("remove_fields", []))
        tabs = []

        field_layout = frappe.db.exists(
            "CRM Fields Layout",
            {
                "dt": dt,
                "type": type
            })

        if field_layout:
            doc = frappe.get_doc("CRM Fields Layout", field_layout)

            if doc and doc.layout:
                tabs = json.loads(doc.layout)

            has_tabs = False
            if isinstance(tabs, list) and len(tabs) > 0 and isinstance(tabs[0], dict):
                has_tabs = any("sections" in tab for tab in tabs)

            if not has_tabs:
                tabs = [{"name": "first_tab", "sections": tabs}]

            if remove_fields:
                for tab in tabs:
                    for section in tab.get("sections", []):
                        for column in section.get("columns", []):
                            original_fields = column.get("fields", [])
            
                            # keep only fields NOT in remove_fields
                            filtered_fields = [
                                f for f in original_fields if f not in remove_fields
                            ]
            
                            if len(original_fields) != len(filtered_fields):
                                removed = set(original_fields) - set(filtered_fields)
                                # print(f"Removed fields | Doctype: {dt} | layout: {removed} | Type: {type}")
                                # print(f"Removed fields from layout: {removed}")
            
                            column["fields"] = filtered_fields

            meta_fields = frappe.get_meta(dt).fields
            meta_fieldnames = {mf.fieldname for mf in meta_fields}

            for section in layout.get("sections", []):
                for column in section.get("columns", []):
                    fields = column.get("fields", [])

                    # filter instead of removing while iterating
                    allowed_fields = []
                    for field in fields:
                        if field in meta_fieldnames:
                            allowed_fields.append(field)
                        else:
                            # print(f"Removed invalid field: {field}")
                            pass

                    column["fields"] = allowed_fields

            # Skip adding sections with duplicate names
            # existing_section_names = {s.get("name") for s in tabs[0]["sections"]}  
            # for section in layout.get("sections", []):
            #     if section.get("name") not in existing_section_names:
            #         tabs[0]["sections"].append(section)

            existing_sections = {
                s.get("name"): idx
                for idx, s in enumerate(tabs[0]["sections"])
            }

            for section in layout.get("sections", []):
                sec_name = section.get("name")

                if sec_name in existing_sections:
                    # ✅ Override entire section
                    tabs[0]["sections"][existing_sections[sec_name]] = section
                    # print(f"Overridden section: {sec_name} | Doctype: {dt} | Type: {type}")
                else:
                    # ✅ Add new section
                    tabs[0]["sections"].append(section)
                    # print(f"Added new section: {sec_name} | Doctype: {dt} | Type: {type}")

            doc.layout = json.dumps(tabs)
            doc.save()
        else:
            doc = frappe.new_doc("CRM Fields Layout")
            doc.dt = dt
            doc.type = type
            doc.layout = json.dumps([{"name": "first_tab", "sections": layout.get("sections", [])}])
            doc.save()
    else:
        remove_fields = set(layout.get("remove_fields", []))
        new_sections = layout.get("sections", [])
    
        field_layout = frappe.db.exists(
            "CRM Fields Layout",
            {
                "dt": dt,
                "type": type
            }
        )
    
        meta_fields = frappe.get_meta(dt).fields
        meta_fieldnames = {mf.fieldname for mf in meta_fields}
    
        # Clean incoming sections (validate + remove_fields)
        for section in new_sections:
            for column in section.get("columns", []):
                original_fields = column.get("fields", [])
    
                valid_fields = [
                    f for f in original_fields
                    if f in meta_fieldnames and f not in remove_fields
                ]
    
                column["fields"] = valid_fields
    
        if field_layout:
            doc = frappe.get_doc("CRM Fields Layout", field_layout)
    
            db_layout = json.loads(doc.layout) if doc.layout else []
    
            # Remove fields from existing DB layout
            if remove_fields:
                for section in db_layout:
                    for column in section.get("columns", []):
                        column["fields"] = [
                            f for f in column.get("fields", [])
                            if f not in remove_fields
                        ]
    
            # existing_section_names = {s.get("name") for s in db_layout}
            # # Append only new sections
            # for section in new_sections:
            #     if section.get("name") not in existing_section_names:
            #         db_layout.append(section)

            existing_sections = {
                s.get("name"): idx
                for idx, s in enumerate(db_layout)
            }

            for section in new_sections:
                sec_name = section.get("name")
            
                if sec_name in existing_sections:
                    # ✅ Override entire section
                    db_layout[existing_sections[sec_name]] = section
                    # print(f"Overridden section: {sec_name} | Doctype: {dt} | Type: {type}")
                else:
                    # ✅ Add new section
                    db_layout.append(section)
                    # print(f"Added new section: {sec_name} | Doctype: {dt} | Type: {type}")
    
            # ✅ Store ONLY array of sections
            doc.layout = json.dumps(db_layout)
            doc.save()
    
        else:
            # Create new doc
            doc = frappe.new_doc("CRM Fields Layout")
            doc.dt = dt
            doc.type = type
    
            # ✅ Store ONLY sections array
            doc.layout = json.dumps(new_sections)
            doc.save()


def override_default_fields_layout():
    crm_lead_override_default_layout()
    crm_deal_override_default_layout()

    frappe.db.commit()
    print("CRM Fields Layout overridden Successfully")

def crm_lead_override_default_layout():
    quick_entry_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_quick_entry_layout.json"))
    data_fields_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_data_fields_layout.json"))
    side_panel_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_side_panel_layout.json"))

    override_crm_fields_layout(
        dt="CRM Lead",
        type="Quick Entry", 
        layout=quick_entry_layout
    )

    override_crm_fields_layout(
        dt="CRM Lead",
        type="Data Fields", 
        layout=data_fields_layout
    )

    override_crm_fields_layout(
        dt="CRM Lead",
        type="Side Panel", 
        layout=side_panel_layout
    )
    
def crm_deal_override_default_layout():
    quick_entry_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_quick_entry_layout.json"))
    data_fields_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_data_fields_layout.json"))
    side_panel_layout = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_side_panel_layout.json"))

    override_crm_fields_layout(
        dt="CRM Deal", 
        type="Quick Entry", 
        layout=quick_entry_layout
    )

    override_crm_fields_layout(
        dt="CRM Deal", 
        type="Data Fields", 
        layout=data_fields_layout
    )
    
    override_crm_fields_layout(
        dt="CRM Deal", 
        type="Side Panel", 
        layout=side_panel_layout
    )

def override_crm_fields_layout(dt=str, type=str, layout=list[dict]):
    field_layout = frappe.db.exists(
        "CRM Fields Layout",
        {
            "dt": dt,
            "type": type
        })

    if field_layout:
        doc = frappe.get_doc("CRM Fields Layout", field_layout)
        doc.layout = json.dumps(layout)
        doc.save()
    else:
        doc = frappe.new_doc("CRM Fields Layout")
        doc.dt = dt
        doc.type = type
        doc.layout = json.dumps(layout)
        doc.save()