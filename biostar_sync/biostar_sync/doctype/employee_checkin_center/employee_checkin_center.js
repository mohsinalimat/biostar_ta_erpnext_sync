// Copyright (c) 2024, Lucky Tsuma and contributors
// For license information, please see license.txt

frappe.ui.form.on("Employee Checkin Center", {
    fetch_attendance_logs: function (frm) {
        return frappe
            .call({
                doc: frm.doc,
                method: "get_checkin_checkout_logs",
                freeze: true,
                freeze_message: __("Fetching checkin/checkout logs..."),
            })
            .then((response) => {
                frappe.msgprint(response.message);
            });
    },
});
