import frappe
from datetime import datetime


def set_last_sync_of_checkin_as_now():
    shift_types = frappe.db.get_all(
        "Shift Type", filters={"enable_auto_attendance": 1}, pluck="name"
    )

    for shift_type in shift_types:
        frappe.db.set_value(
            "Shift Type",
            shift_type,
            "last_sync_of_checkin",
            datetime.now(),
            update_modified=False,
        )
        frappe.db.commit()
