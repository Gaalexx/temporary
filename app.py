from flask import Flask
from typing import Dict, Optional
from func.actions import *  # index_page, calendar_page, calendar_month_page, calendar_week_page, calendar_day_page, home,


def create_app(config_overrides: Optional[Dict] = None) -> Flask:
    app = Flask(__name__)

    app.config.from_object("config")
    if config_overrides is not None:
        app.config.from_mapping(config_overrides)

    app.add_url_rule("/calendar/", "calendar_page", calendar_page)
    app.add_url_rule("/calendar/month/", "calendar_month_page", calendar_month_page)
    app.add_url_rule("/calendar/month/<year>/<month>/", "calendar_month_page", calendar_month_page)
    app.add_url_rule("/calendar/week/", "calendar_week_page", calendar_week_page)
    app.add_url_rule("/calendar/week/<year>/<month>/<week>/", "calendar_week_page", calendar_week_page)
    app.add_url_rule("/calendar/day/", "calendar_day_page", calendar_day_page, methods=["GET", "POST", "PUT"])
    app.add_url_rule("/calendar/day/<year>/<month>/<day>/", "calendar_day_page", calendar_day_page,
                     methods=["GET", "POST", "PUT"])
    app.add_url_rule("/", "main", home, methods=["GET", "POST"])
    app.add_url_rule("/reg", "registration", registration, methods=["GET", "POST"])
    app.add_url_rule("/check", "check", check, methods=["GET", "POST"])
    app.add_url_rule("/log", "login", login, methods=["GET", "POST"])
    app.add_url_rule("/checkForLogin", "is_Logined", is_Logined, methods=["GET", "POST"])
    app.add_url_rule("/calendar", "calendar", is_Logined, methods=["GET", "POST"])
    app.add_url_rule("/unLogin", "unLogin", unLogin, methods=["GET", "POST"])
    app.add_url_rule("/settings", "settings", settings, methods=["GET", "POST"])
    app.add_url_rule("/calendar/day/<day>/<month>/<year>/<num_hour>/add", "add", get_Info, methods=["GET", "POST"])
    app.add_url_rule("/change_password", "ch_p", change_password, methods=["GET", "POST"])
    app.add_url_rule("/check_for_change", "ch_check", check_for_change, methods=["GET", "POST"])
    app.add_url_rule("/change", "change", change, methods=["GET", "POST"])
    app.add_url_rule('/calendar/event/<year>/<month>/<day>/<time>/<id>', "view", viewNote, methods=["GET", "POST"])

    return app


if __name__ == "__main__":
    app = create_app()
    app.secret_key = b"9245a0065e066c7b07198c8e762ffda1278ead01b47adfc605eeb159fc9e9602"
    app.run(debug=app.config["DEBUG"],
            host=app.config["HOST_IP"],
            port=app.config["PORT"])

