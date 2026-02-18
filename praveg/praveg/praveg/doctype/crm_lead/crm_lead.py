import frappe
from frappe.utils import getdate, today

def validate(doc, method):
    validate_dates(doc)
    calculate_nights(doc)
    calculate_child_rows(doc)
    calculate_totals(doc)

def validate_dates(doc):
    if not doc.custom_check_in:
        return

    new_check_in = getdate(doc.custom_check_in) if doc.custom_check_in else None
    new_check_out = getdate(doc.custom_check_out) if doc.custom_check_out else None

    # -------------------------------------------------
    # 🔹 CREATE TIME VALIDATION
    # -------------------------------------------------
    if doc.is_new():
        # Check-in cannot be in the past
        if new_check_in and new_check_in < getdate(today()):
            frappe.throw("Check-in date cannot be before today.")

        # Check-out requires check-in
        if new_check_out and not new_check_in:
            frappe.throw("Check-out date cannot be set without Check-in date.")

        # Check-in vs Check-out order
        if new_check_in and new_check_out:
            if new_check_out < new_check_in:
                frappe.throw("Check-out date cannot be before Check-in date.")

        # Proper order validation
        if new_check_in and new_check_out:
            if new_check_out <= new_check_in:
                frappe.throw("Check-out date must be after Check-in date.")

    # -------------------------------------------------
    # 🔹 UPDATE TIME VALIDATION
    # -------------------------------------------------
    else:
        old_check_in = getdate(doc.get_db_value("custom_check_in")) if doc.get_db_value("custom_check_in") else None
        old_check_out = getdate(doc.get_db_value("custom_check_out")) if doc.get_db_value("custom_check_out") else None

        check_in_changed = old_check_in != new_check_in
        check_out_changed = old_check_out != new_check_out

        # If check-in changed → validate past date
        if check_in_changed:
            if new_check_in and new_check_in < getdate(today()):
                frappe.throw("Check-in date cannot be before today.")

        # If checkout changed → require check-in
        if check_out_changed:
            if new_check_out and not new_check_in:
                frappe.throw("Check-out date cannot be set without Check-in date.")

        # If check-in changed → validate order
        if check_in_changed:
            if new_check_in and new_check_out:
                if new_check_out < new_check_in:
                    frappe.throw("Check-out date cannot be before Check-in date.")

        # If any date changed → validate order
        if check_in_changed or check_out_changed:
            if new_check_in and new_check_out:
                if new_check_out <= new_check_in:
                    frappe.throw("Check-out date must be after Check-in date.")


# def validate_dates(doc):
#     if not doc.custom_check_in:
#         return
    
#     # Normalize everything to date objects
#     old_check_in = getdate(doc.get_db_value("custom_check_in"))
#     old_check_out = getdate(doc.get_db_value("custom_check_out"))
    
#     new_check_in = getdate(doc.custom_check_in)
#     new_check_out = getdate(doc.custom_check_out)

#     check_in_changed = old_check_in != new_check_in
#     check_out_changed = old_check_out != new_check_out

#     # --- Validate ONLY if new OR check-in changed ---
#     if doc.is_new() or check_in_changed:
#         if doc.custom_check_in:
#             if new_check_in < getdate(today()):
#                 frappe.throw("Check-in date cannot be before today.")

#     # --- Check-out requires check-in (only if checkout changed) ---
#     if check_out_changed:
#         if doc.custom_check_out and not doc.custom_check_in:
#             frappe.throw("Check-out date cannot be set without Check-in date.")

#     # --- Check-in vs Check-out order (only if any date changed) ---
#     if (check_in_changed or check_out_changed):
#         if doc.custom_check_in and doc.custom_check_out:
#             if new_check_out < new_check_in:
#                 frappe.throw("Check-out date cannot be before Check-in date.")

#     # --- Check-in vs Check-out order (only if any date changed) ---
#     if check_in_changed or check_out_changed:
#         if doc.custom_check_in and doc.custom_check_out:
#             if new_check_out <= new_check_in:
#                 frappe.throw("Check-out date must be after Check-in date.")

def calculate_nights(doc):
    if doc.custom_check_in and doc.custom_check_out:
        check_in = getdate(doc.custom_check_in)
        check_out = getdate(doc.custom_check_out)
        doc.custom_no_of_nights = (check_out - check_in).days
    else:
        doc.custom_no_of_nights = 0

def calculate_child_rows(doc):
    if not doc.custom_guest:
        return

    nights = float(doc.custom_no_of_nights or 0)

    for row in doc.custom_guest:

        # -------------------
        # ROOM CALCULATION
        # -------------------
        no_of_rooms = float(row.no_of_rooms or 0)
        room_rate = float(row.room_rate or 0)

        row.room_quantity = no_of_rooms * nights
        row.room_amount = row.room_quantity * room_rate

        # -------------------
        # MEAL CALCULATION
        # -------------------
        meal_persons = get_meal_person_count(row)
        meal_rate = float(row.meal_rate or 0)

        row.meal_persons = meal_persons
        row.meal_qty = meal_persons * nights
        row.meal_amount = row.meal_qty * meal_rate

        # -------------------
        # EXTRA BED
        # -------------------
        extra_beds = float(row.no_of_extra_bed or 0)
        extra_bed_rate = float(doc.custom_extra_bed_rate or 0)

        row.extra_bed_quantity = extra_beds * nights
        row.extra_bed_amount = row.extra_bed_quantity * extra_bed_rate

        # -------------------
        # LINE TOTAL
        # -------------------
        row.line_total = (
            row.room_amount
            + row.meal_amount
            + row.extra_bed_amount
        )

def get_meal_person_count(row):
    adult_count = int(row.adult or 0)
    
    child_ages = [
        getattr(row, "first_child_age", None),
        getattr(row, "second_child_age", None),
        getattr(row, "third_child_age", None),
        getattr(row, "fourth_child_age", None),
        getattr(row, "fifth_child_age", None)
    ]
            
    # Only count children age 7 or older
    child_count = 0

    for age in child_ages:
        if age is None or age == "":
            continue

        age = int(age)

        if age >= 7:
            child_count += 1

    return adult_count + child_count

def calculate_totals(doc):
    subtotal = 0

    for row in doc.custom_guest:
        subtotal += float(row.line_total or 0)

    doc.custom_sub_total = subtotal

    discount_percent = float(doc.custom_discount_percent or 0)
    doc.custom_discount_amount = (subtotal * discount_percent) / 100

    taxable_amount = subtotal - doc.custom_discount_amount
    doc.custom_taxable_amount = taxable_amount

    # hardcoding tax rate for now, can be made dynamic later if needed
    tax_rate = float(18)

    doc.custom_tax_amount = (taxable_amount * tax_rate) / 100
    doc.custom_rates = taxable_amount + doc.custom_tax_amount