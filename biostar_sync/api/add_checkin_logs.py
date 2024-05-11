import frappe
import time
from ..controllers.biostar_connect import BiostarConnect
from ..controllers.set_last_sync_of_checkin_as_now import (
    set_last_sync_of_checkin_as_now,
)
from frappe.utils.password import get_decrypted_password
from .send_logs_to_erpnext import send_to_erpnext

SETTINGS_DOCTYPE = "Biostar Sync Settings"
username = frappe.db.get_single_value(SETTINGS_DOCTYPE, "username") or None
password = (
    get_decrypted_password(SETTINGS_DOCTYPE, SETTINGS_DOCTYPE, "password") or None
)


@frappe.whitelist()
def add_checkin_logs_for_current_day(username=username, password=password):

    biostar = BiostarConnect(username, password)
    biostar.get_attendance_report()
    biostar.format_attendance_logs()
    biostar.create_punch_logs()

    if biostar.punch_logs:
        for log in biostar.punch_logs:
            send_to_erpnext(
                log.get("employee_field_value"),
                log.get("timestamp"),
                log.get("log_type"),
            )
            time.sleep(3)

    set_last_sync_of_checkin_as_now()


@frappe.whitelist()
def add_checkin_logs_for_specified_dates(
    start_date, end_date, username=username, password=password
):

    biostar = BiostarConnect(username, password)
    biostar.get_attendance_report(start_date, end_date)
    biostar.format_attendance_logs()
    biostar.create_punch_logs()

    if biostar.punch_logs:
        for log in biostar.punch_logs:
            send_to_erpnext(
                log.get("employee_field_value"),
                log.get("timestamp"),
                log.get("log_type"),
            )
            time.sleep(3)

    set_last_sync_of_checkin_as_now()
