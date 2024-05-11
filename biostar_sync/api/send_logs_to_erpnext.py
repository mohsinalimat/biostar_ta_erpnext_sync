import frappe
from .make_http_request import make_http_request
from frappe.utils.password import get_decrypted_password
from frappe.utils import get_url

SETTINGS_DOCTYPE = "Biostar Sync Settings"
api_key = frappe.db.get_single_value(SETTINGS_DOCTYPE, "api_key")
api_secret = get_decrypted_password(SETTINGS_DOCTYPE, SETTINGS_DOCTYPE, "api_secret")


@frappe.whitelist()
def send_to_erpnext(employee_field_value, timestamp, log_type):
    headers = {
        "Authorization": "token " + api_key + ":" + api_secret,
        "Accept": "application/json",
    }

    request_body = {
        "employee_field_value": employee_field_value,
        "timestamp": timestamp.__str__(),
        "log_type": log_type,
    }

    send_to_erpnext_url = f"{get_url().__str__()}/api/method/hrms.hr.doctype.employee_checkin.employee_checkin.add_log_based_on_employee_field"

    response = make_http_request(
        send_to_erpnext_url, method="POST", data=request_body, headers=headers
    )
