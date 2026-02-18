import os
import click
from ..services.doctype_service import create_doctypes
from ..services.custom_fields_service import create_or_update_custom_fields
from ..services.property_setter_service import create_or_update_property_setters
from ..services.crm_fields_layout_service import override_default_fields_layout
from ..services.default_records_service import create_default_records
from ..services.utils_service import load_json

# Get folder of this file
BASE_DIR = os.path.dirname(__file__)


BASE_FILE_PATH = os.path.join(BASE_DIR, "data")

def after_install():
    print("Setting up Praveg...")
    
    CRM_LEAD_CUSTOM_FIELDS = load_json(os.path.join(BASE_FILE_PATH, "crm_lead_new_fields.json"))
    CRM_DEAL_CUSTOM_FIELDS = load_json(os.path.join(BASE_FILE_PATH, "crm_deal_new_fields.json"))
    PROPERTY_SETTERS = load_json(os.path.join(BASE_FILE_PATH, "new_property_setters.json"))
    DEFAULT_RECORDS = load_json(os.path.join(BASE_FILE_PATH, "default_records.json"))

    custom_fields = CRM_LEAD_CUSTOM_FIELDS + CRM_DEAL_CUSTOM_FIELDS

    create_or_update_custom_fields(custom_fields)
    create_or_update_property_setters(PROPERTY_SETTERS)
    override_default_fields_layout()
    create_default_records(DEFAULT_RECORDS)
    
    click.secho("Thank you for installing Praveg!", fg="green")
    
def after_app_install(app_name):
    pass