from praveg.services.doctype_service import create_doctypes
from praveg.services.custom_fields_service import create_or_update_custom_fields
from praveg.services.property_setter_service import create_or_update_property_setters
def execute():
    
    DOCTYPES = [
        {
            "name": "CRM Hotel Property",
            "module": "Praveg",
            "autoname": "field:hotel_property_name",
            "custom": 0,
            "fields": [
                {
                    "label": "Name",
                    "fieldname": "hotel_property_name",
                    "fieldtype": "Data",
                    "reqd": 1
                },
                {
                    "label": "Address",
                    "fieldname": "address",
                    "fieldtype": "Text",
                    "reqd": 0
                },
                {
                    "label": "Toll Free Number",
                    "fieldname": "toll_free_number",
                    "fieldtype": "Data",
                    "reqd": 0
                },
                {
                    "label": "Email",
                    "fieldname": "email",
                    "fieldtype": "Data",
                    "reqd": 0
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ]
        },
        {
            "name": "CRM Room Category",
            "module": "Praveg",
            "autoname": "field:room_category_name",
            "custom": 0,
            "fields": [
                {
                    "label": "Name",
                    "fieldname": "room_category_name",
                    "fieldtype": "Data",
                    "reqd": 1
                },
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ]
        },
        {
            "name": "CRM Meal Plan",
            "module": "Praveg",
            "autoname": "field:meal_plan_name",
            "custom": 0,
            "fields": [
                {
                    "label": "Name",
                    "fieldname": "meal_plan_name",
                    "fieldtype": "Data",
                    "reqd": 1
                }
            ],
            "permissions": [
                {
                    "role": "System Manager",
                    "read": 1,
                    "write": 1,
                    "create": 1,
                    "delete": 1
                }
            ]
        }
    ]

    custom_fields = [
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Hotel Property",
            "fieldname": "custom_hotel_property",
            "fieldtype": "Link",
            "options": "CRM Hotel Property",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Check In",
            "fieldname": "custom_check_in",
            "fieldtype": "Date",
            "default": "Today",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Check Out",
            "fieldname": "custom_check_out",
            "fieldtype": "Date",
            "default": "Today",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "No of Persons",
            "fieldname": "custom_no_of_persons",
            "fieldtype": "Int",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Adult",
            "fieldname": "custom_adult",
            "fieldtype": "Select",
            "options": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
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
            "dt": "CRM Lead",
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
            "dt": "CRM Lead",
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
            "dt": "CRM Lead",
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
            "dt": "CRM Lead",
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
            "dt": "CRM Lead",
            "label": "Room Category",
            "fieldname": "custom_room_category",
            "fieldtype": "Link",
            "options": "CRM Room Category",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "No of Rooms",
            "fieldname": "custom_no_of_rooms",
            "fieldtype": "Int",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Meal Plans",
            "fieldname": "custom_meal_plans",
            "fieldtype": "Link",
            "options": "CRM Meal Plan",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Rates",
            "fieldname": "custom_rates",
            "fieldtype": "Float",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "City",
            "fieldname": "custom_city",
            "fieldtype": "Data",
            # "options": "City",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "State",
            "fieldname": "custom_state",
            "fieldtype": "Data",
            # "options": "State",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Country",
            "fieldname": "custom_country",
            "fieldtype": "Data",
            # "options": "Country",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Pincode",
            "fieldname": "custom_pincode",
            "fieldtype": "Data",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "Remarks",
            "fieldname": "custom_remarks",
            "fieldtype": "Text",
            "module": "Praveg",
            "is_system_generated": 1
        },
        {
            "doctype": "Custom Field",
            "dt": "CRM Lead",
            "label": "User Type",
            "fieldname": "custom_user_type",
            "fieldtype": "Select",
            "options": "Individual\nCorporate\nAgent",
            "module": "Praveg",
            "is_system_generated": 1
        }
    ]
    
    PROPERTY_SETTERS = [
        {
            "doc_type": "CRM Lead",
            "field_name": "organization",
            "property_type": "Data",
            "property": "depends_on",
            "value": "eval: doc.custom_user_type != 'Individual'",
            "module": "Praveg",
            "is_system_generated": 1
        }
    ]

    create_doctypes(DOCTYPES)
    create_or_update_custom_fields(custom_fields)
    create_or_update_property_setters(PROPERTY_SETTERS)
