import frappe
from frappe.utils import today, getdate, format_date
from frappe.desk.search import search_link

@frappe.whitelist()
def get_date_utils():
    # This returns a dictionary of helpful date strings to the frontend
    return {
        "today": getdate(today()),
    }

@frappe.whitelist()
def custom_search_link(
        doctype, 
        txt, 
        filters=None
    ):

    if doctype == "CRM Property Room Category":
        pass

    return search_link(
        doctype=doctype, 
        txt=txt,
        filters=filters,
    )