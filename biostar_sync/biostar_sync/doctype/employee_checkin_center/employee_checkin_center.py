# Copyright (c) 2024, Lucky Tsuma and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class EmployeeCheckinCenter(Document):
	@frappe.whitelist()
	def get_checkin_checkout_logs(self):
		if self.start_date > self.end_date:
			frappe.throw(_('Start date cannot be later than end date'))
