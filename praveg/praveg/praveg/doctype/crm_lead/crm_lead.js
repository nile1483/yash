frappe.ui.form.on('CRM Lead', {
    onload(frm) {
        // Snapshot DB values ONCE
        frm._old_check_in = frm.doc.custom_check_in;
        frm._old_check_out = frm.doc.custom_check_out;

        set_room_category_meal_plan_by_property(frm);
    },

    refresh(frm) {

    },

    validate(frm) {
        frm.trigger('check_valid_date');
    },

    custom_hotel_property(frm) {
        set_room_category_meal_plan_by_property(frm);
    },

    custom_check_in(frm) {
        // Optional: auto-correct checkout
        // if (frm.doc.custom_check_out && frm.doc.custom_check_out < frm.doc.custom_check_in) {
        //     frm.set_value('custom_check_out', frm.doc.custom_check_in);
        // }
    },

    check_valid_date(frm) {
        const today = frappe.datetime.get_today();

        const old_check_in = frm._old_check_in;
        const old_check_out = frm._old_check_out;

        const new_check_in = frm.doc.custom_check_in;
        const new_check_out = frm.doc.custom_check_out;

        const check_in_changed = old_check_in !== new_check_in;
        const check_out_changed = old_check_out !== new_check_out;

        // --- INVARIANT: checkout requires check-in (ALWAYS) ---
        if (new_check_out && !new_check_in) {
            frappe.msgprint(__('Check-out date cannot be set without Check-in date.'));
            frappe.validated = false;
            return;
        }

        // --- INVARIANT: order (ALWAYS) ---
        if (new_check_in && new_check_out && new_check_out < new_check_in) {
            frappe.msgprint(__('Check-out date cannot be before Check-in date.'));
            frappe.validated = false;
            return;
        }

        // --- Validate ONLY if new OR check-in changed ---
        if (frm.is_new() || check_in_changed) {
            if (new_check_in && new_check_in < today) {
                frappe.msgprint(__('Check-in date cannot be before today.'));
                frappe.validated = false;
                return;
            }
        }

        // --- Checkout requires checkin (only if checkout changed) ---
        if (check_out_changed) {
            if (new_check_out && !new_check_in) {
                frappe.msgprint(__('Check-out date cannot be set without Check-in date.'));
                frappe.validated = false;
                return;
            }
        }

        // --- Order validation (only if something changed) ---
        if (check_in_changed || check_out_changed) {
            if (new_check_in && new_check_out && new_check_out < new_check_in) {
                frappe.msgprint(__('Check-out date cannot be before Check-in date.'));
                frappe.validated = false;
            }
        }
    }
});

frappe.ui.form.on('CRM Guest Details', {
    // Trigger whenever a new row is added
    // This ensures default values are reflected
    custom_guest_add (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        // Set default meal_plan_count_person from adult
        row.meal_plan_count_person = row.adult || 0;
        frm.refresh_field('custom_guest');
    },

    adult(frm, cdt, cdn) {
        // Get the specific row object
        let row = locals[cdt][cdn];

        // Set the meal_plan_count_person for THIS row only
        row.meal_plan_count_person = row.adult || 0;

        // Refresh the row field in the grid
        frm.refresh_field('custom_guest');
    }
});

function set_room_category_meal_plan_by_property(frm) {
    frm.fields_dict['custom_guest'].grid.get_field('room_category').get_query =
        function (doc, cdt, cdn) {
            if (!frm.doc.custom_hotel_property) {
                return {
                    filters: {
                        name: '__invalid__'   // forces empty list
                    }
                };
            }

            return {
                filters: {
                    hotel_property: doc.custom_hotel_property
                }
            };
        };

    frm.fields_dict['custom_guest'].grid.get_field('meal_plan').get_query =
        function (doc, cdt, cdn) {
            if (!frm.doc.custom_hotel_property) {
                return {
                    filters: {
                        name: '__invalid__'
                    }
                };
            }

            return {
                filters: {
                    hotel_property: doc.custom_hotel_property
                }
            };
        };
}