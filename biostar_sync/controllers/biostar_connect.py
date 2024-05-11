import json
import frappe
from frappe.utils import today
from frappe.utils.password import get_decrypted_password
from datetime import datetime
from ..api.make_http_request import make_http_request
from .check_cookie_expired import is_cookie_expired

SETTINGS_DOCTYPE = "Biostar Sync Settings"
ta_base_url = frappe.db.get_single_value(SETTINGS_DOCTYPE, "ta_url").__str__()


class BiostarConnect:
    def __init__(self, username, password) -> None:
        if not username:
            frappe.throw(f"Please set a username on {SETTINGS_DOCTYPE}")

        if not password:
            frappe.throw(f"Please set a password on {SETTINGS_DOCTYPE}")

        self.username = username
        self.password = password
        self.cookie = self.login()

    def login(self) -> str:
        login_url = f"{ta_base_url}/login"
        request_body = {
            "notification_token": "string",
            "mobile_device_type": "string",
            "mobile_os_version": "string",
            "mobile_app_version": "string",
            "user_id": self.username,
            "password": self.password,
        }
        response = make_http_request(login_url, data=request_body, method="POST")

        if response:
            return response.headers["Set-Cookie"]

    def get_attendance_report(
        self, start_date=today().__str__(), end_date=today().__str__()
    ):
        headers = {"Content-Type": "application/json"}
        attendance_url = f"{ta_base_url}/report.json"

        self.attendance_logs = []

        offset = 0
        limit = 200

        while True:
            if not self.cookie or is_cookie_expired(self.cookie):
                self.cookie = self.login()

            headers["Cookie"] = self.cookie

            request_body = {
                "limit": limit,
                "offset": offset,
                "type": "CUSTOM",
                "start_datetime": start_date,
                "end_datetime": end_date,
                "user_id_list": [],
                "group_id_list": ["1"],
                "report_type": "REPORT_DAILY",
                "report_filter_type": "",
                "language": "en",
                "rebuild_time_card": True,
                "columns": [{}],
            }

            response = make_http_request(
                attendance_url,
                method="POST",
                data=json.dumps(request_body),
                headers=headers,
            )

            """no more records, break loop"""
            if not response.json()["records"]:
                if self.attendance_logs:
                    """filter for entries with only checkin/out time"""
                    self.attendance_logs = [
                        log
                        for log in self.attendance_logs
                        if log.get("inTime") != "-" or log.get("outTime") != "-"
                    ]

                break

            self.attendance_logs.extend(response.json()["records"])
            offset += limit

    def format_attendance_logs(self):
        if self.attendance_logs:
            self.attendance_logs = [
                {
                    "date": log["datetime"],
                    "in_time": log["inTime"],
                    "out_time": log["outTime"],
                    "employee_field_value": log["userId"],
                    "name": log["userName"],
                }
                for log in self.attendance_logs
            ]

    def create_punch_logs(self):
        """from the attendance report, create checkin/out logs to be sent to erpnext"""
        if self.attendance_logs:
            self.punch_logs = []
            datetime_format = "%d/%m/%Y %H:%M:%S"

            for log in self.attendance_logs:
                if log["in_time"] != "-":

                    datetime_str = f"{log['date']} {log['in_time']}"
                    log["datetime_in"] = datetime.strptime(
                        datetime_str, datetime_format
                    )

                    self.punch_logs.extend(
                        [
                            {
                                "employee_field_value": log["employee_field_value"],
                                "timestamp": log["datetime_in"],
                                "log_type": "IN",
                            }
                        ]
                    )

                if log["out_time"] != "-":

                    datetime_str = f"{log['date']} {log['out_time']}"
                    log["datetime_out"] = datetime.strptime(
                        datetime_str, datetime_format
                    )

                    self.punch_logs.extend(
                        [
                            {
                                "employee_field_value": log["employee_field_value"],
                                "timestamp": log["datetime_out"],
                                "log_type": "OUT",
                            }
                        ]
                    )
