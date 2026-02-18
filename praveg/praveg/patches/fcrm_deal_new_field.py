from praveg.services.custom_fields_service import create_or_update_custom_fields
def execute():
    
    custom_fields = [
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Hotel Property",
            "fieldname": "custom_hotel_property",
            "fieldtype": "Link",
            "options": "CRM Hotel Property",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Check In",
            "fieldname": "custom_check_in",
            "fieldtype": "Date",
            "default": "Today",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Check Out",
            "fieldname": "custom_check_out",
            "fieldtype": "Date",
            "default": "Today",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "No of Persons",
            "fieldname": "custom_no_of_persons",
            "fieldtype": "Int",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Adult",
            "fieldname": "custom_adult",
            "fieldtype": "Select",
            "options": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Child (0-17)",
            "fieldname": "custom_child",
            "fieldtype": "Select",
            "options": "0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10",
            "default": "0",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "1st Child Age",
            "fieldname": "custom_child_age_1",
            "fieldtype": "Select",
            "options": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17",
            "depends_on": "eval: doc.custom_child > 0 && doc.custom_child < 11",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "2nd Child Age",
            "fieldname": "custom_child_age_2",
            "fieldtype": "Select",
            "options": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17",
            "depends_on": "eval: doc.custom_child > 1 && doc.custom_child < 11",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "3rd Child Age",
            "fieldname": "custom_child_age_3",
            "fieldtype": "Select",
            "options": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17",
            "depends_on": "eval: doc.custom_child > 2 && doc.custom_child < 11",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "4th Child Age",
            "fieldname": "custom_child_age_4",
            "fieldtype": "Select",
            "options": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17",
            "depends_on": "eval: doc.custom_child > 3 && doc.custom_child < 11",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Room Category",
            "fieldname": "custom_room_category",
            "fieldtype": "Link",
            "options": "CRM Room Category",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "No of Rooms",
            "fieldname": "custom_no_of_rooms",
            "fieldtype": "Int",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Meal Plans",
            "fieldname": "custom_meal_plans",
            "fieldtype": "Link",
            "options": "CRM Meal Plan",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Rates",
            "fieldname": "custom_rates",
            "fieldtype": "Float",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "City",
            "fieldname": "custom_city",
            "fieldtype": "Data",
            # "options": "City",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "State",
            "fieldname": "custom_state",
            "fieldtype": "Data",
            # "options": "State",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Country",
            "fieldname": "custom_country",
            "fieldtype": "Data",
            # "options": "Country",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Pincode",
            "fieldname": "custom_pincode",
            "fieldtype": "Data",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "Remarks",
            "fieldname": "custom_remarks",
            "fieldtype": "Text",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Deal",
            "label": "User Type",
            "fieldname": "custom_user_type",
            "fieldtype": "Select",
            "options": "Individual\nCorporate\nAgent",
            "module": "Praveg",
            "is_system_generated": 1
        }
    ]

    create_or_update_custom_fields(custom_fields)
