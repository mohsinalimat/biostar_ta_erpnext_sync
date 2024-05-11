import frappe
import requests


def make_http_request(url, method="POST", data=None, headers=None, verify=False):
    request_kwargs = {"url": url, "headers": headers, "verify": verify}

    if data:
        request_kwargs["data"] = data

    try:
        valid_methods = {"GET", "POST", "PUT", "PATCH", "DELETE"}

        if method.upper() not in valid_methods:
            frappe.throw(
                f"Invalid HTTP method: {method}. Valid methods are: {', '.join(valid_methods)}"
            )

        if method.upper() == "GET":
            response = requests.get(**request_kwargs)
        elif method.upper() == "POST":
            response = requests.post(**request_kwargs)
        elif method.upper() == "PUT":
            response = requests.put(**request_kwargs)
        elif method.upper() == "PATCH":
            response = requests.patch(**request_kwargs)
        elif method.upper() == "DELETE":
            response = requests.delete(**request_kwargs)
        else:
            frappe.throw("Invalid action!")

        if response.status_code != 200:
            frappe.throw(response.raise_for_status())
        return response
    except Exception as e:
        frappe.throw(str(e))
