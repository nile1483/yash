frappe.ui.form.on("CRM Deal", {
    onload: function (frm) {
        frm.trigger("modified_status_query")
    },

    refresh: function (frm) {
        frm.trigger("set_hidden_fields")
    },

    status: function (frm) {
        frm.trigger("set_hidden_fields")
    },

    lead: function (frm) {
        frm.trigger("auto_fill_lead_related_fields")
    },

    set_hidden_fields(frm) {
        frm.toggle_display(["lost_reason", "lost_notes"], frm.doc.status == "Lost")
    },

    modified_status_query: function (frm) {
        frm.set_query("status", function () {
            return {
                query: "shayona.shayona.doctype.crm_deal.crm_deal.get_crm_deal_status_master",
            }
        })
    },

    auto_fill_lead_related_fields(frm) {
        const lead = frm.doc.lead;
        
        if (lead) {
            frappe.db.get_value("CRM Lead", lead, [
                "lead_name",
                "source",
                "organization",
            ], (r) => {
                if (r) {
                    frm.set_value("lead_name", r.lead_name);
                    frm.set_value("source", r.source);
                    frm.set_value("organization_name", r.organization);
                }
            });
        }
    }
})