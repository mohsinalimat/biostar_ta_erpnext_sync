from datetime import datetime
from http.cookies import SimpleCookie


def is_cookie_expired(cookie_string):
    """parse cookie string"""
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    """extract 'expires' attribute"""
    bs_ta_session_id_cookie = cookie.get("bs-ta-session-id")

    """ Check if 'bs-ta-session-id' cookie exists and has 'expires' attribute """
    if bs_ta_session_id_cookie is None or "expires" not in bs_ta_session_id_cookie:
        return False

    expires = bs_ta_session_id_cookie["expires"]

    expires_date = datetime.strptime(expires, "%a, %d %b %Y %H:%M:%S %Z")

    return expires_date <= datetime.utcnow()
