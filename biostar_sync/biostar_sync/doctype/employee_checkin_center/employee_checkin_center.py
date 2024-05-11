# Copyright (c) 2024, Lucky Tsuma and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from ....api.add_checkin_logs import add_checkin_logs_for_specified_dates


class EmployeeCheckinCenter(Document):
    @frappe.whitelist()
    def get_checkin_checkout_logs(self):
        if self.start_date > self.end_date:
            frappe.throw(_("Start date cannot be later than end date"))

        add_checkin_logs_for_specified_dates(self.start_date, self.end_date)
