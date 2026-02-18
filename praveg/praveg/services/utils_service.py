import os
import json
import frappe

# BASE_DIR = os.path.dirname(__file__)

def load_json(filepath):
    # try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    # except FileNotFoundError:
        # frappe.throw("File not found.")