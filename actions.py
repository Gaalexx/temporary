from flask import render_template, make_response, current_app, request
from cls.gregorian_calendar import GregorianCalendar
from func.calendar_func import prev_month_link, next_month_link, previous_week_link, next_week_link, prev_day_link, \
    next_day_link
from flask import redirect
from flask import session
from Exceptions import SearchExeption
from GIGAchat.GigaChat import *


def index_page() -> make_response:
    return make_response(render_template("index.html"))


def calendar_page() -> make_response:
    calendar = calendar_month_page()
    return calendar


def calendar_month_page(year=None, month=None) -> make_response:
    GregorianCalendar.setfirstweekday(current_app.config["FIRST_DAY_WEEK"])
    from DataBase_class import EventsDataBase

    current_day, current_month, current_year = GregorianCalendar.current_date()
    if (year is None) and (month is None):
        year = current_year
        month = current_month
    else:
        year = int(year)
        month = int(month)
    edb = EventsDataBase()
    if not request.cookies.get("is_logined"):
        print("nothing")
    else:
        uId = request.cookies.get("is_logined")
        events = edb.getAllEventsMonth(uId, month)
    month_name = GregorianCalendar.MONTH_NAMES[month - 1]
    current_month_name = GregorianCalendar.MONTH_NAMES[current_month - 1]
    month_days = GregorianCalendar.month_days(year, month)
    print(events)
    return make_response(
        render_template(
            "calendar_month.html",
            current_month_name=current_month_name,
            month_name=month_name,
            month=month,
            year=year,
            current_day=current_day,
            current_month=current_month,
            current_year=current_year,
            days_of_events=events,
            weekdays_headers=current_app.config["WEEK_DAYS"],
            month_days=month_days,
            previous_month_link=prev_month_link(year, month),
            next_month_link=next_month_link(year, month),
        )
    )


def calendar_week_page(year=None, month=None, week=None) -> make_response:
    from DataBase_class import EventsDataBase
    import datetime as dt

    GregorianCalendar.setfirstweekday(current_app.config["FIRST_DAY_WEEK"])

    current_day, current_month, current_year = GregorianCalendar.current_date()
    current_week = GregorianCalendar.num_week_in_month_by_date(current_year, current_month, current_day)
    if (year is None) and (month is None):
        year = current_year
        month = current_month
        week = current_week
    else:
        year = int(year)
        month = int(month)
        week = int(week)

    week_days = GregorianCalendar.week_days(year, month, week)

    if week_days[0].month != week_days[6].month:
        month_name = f"{GregorianCalendar.MONTH_NAMES[week_days[0].month - 1]} - {GregorianCalendar.MONTH_NAMES[week_days[6].month - 1]}"
    else:
        month_name = GregorianCalendar.MONTH_NAMES[month - 1]

    current_month_name = GregorianCalendar.MONTH_NAMES[current_month - 1]

    edb = EventsDataBase()
    events = []
    if not request.cookies.get("is_logined"):
        print("nothing")
    else:
        uId = request.cookies.get("is_logined")
        events = edb.getAllEventsWeek(uId, month)
    week_events = [
        [dt.date(events[x][0], events[x][1], events[x][2]), events[x][3], events[x][4], events[x][0], events[x][1],
         events[x][2], events[x][3], events[x][-1]] for x in range(len(events))]
    print(week_events)
    return make_response(render_template(
        "calendar_week.html",
        month_name=month_name,
        current_month_name=current_month_name,
        week=week,
        month=month,
        year=year,
        current_day=current_day,
        current_week=current_week,
        current_month=current_month,
        current_year=current_year,
        week_events=week_events,
        weekdays_headers=current_app.config["WEEK_DAYS"],
        week_days=week_days,
        previous_week_link=previous_week_link(year, month, week),
        next_month_link=next_week_link(year, month, week)
    )
    )

def update_task_day_action(year=None, month=None, day=None, id=None) -> make_response:
    print("update_task_day_action")

def calendar_day_page(year=None, month=None, day=None) -> make_response:
    print("calendar_day_page")

    from DataBase_class import EventsDataBase

    if request.method == "PUT":
        print("calendar_day_page PUT")

        body = request.data.decode("utf-8")
        idd, newHour, oldHour = body.split("|")
        print("calendar_day_page newHour: %s, oldHour: %s" % (newHour, oldHour))

        db = EventsDataBase()
        date = [year, month, day, oldHour]
        n_date = [year, month, day, newHour]

        """
        viewNote POST date: ['2024', '5', '23', '0']
        viewNote POST n_date: [2024, 5, 23, 0]
        """

        print("calendar_day_page date: %s" % date)
        print("calendar_day_page n_date: %s" % n_date)

        print(body)

        #db.updateEvent(85, n_date, ["name", "description"], date)

        if not request.cookies.get("is_logined"):
            return "Вы не вошли в аккаунт"
        else:
            uId = request.cookies.get("is_logined")
            print(f"calendar_day_page uId: {uId}  date: {date}  id: {idd}")

            #calendar_day_page uId: 2  date: ['2024', '5', '29', '0']  id: 151

            res = db.getEvent(uId, date, idd)
            print("calendar_day_page res: %s" % res)
            if len(res) != 0:
                print("calendar_day_page res: %s" % res)
                #print("calendar_day_page res: %s" % res[0])

                db.updateEvent(uId, n_date, [res[0], res[1]], date)



    GregorianCalendar.setfirstweekday(current_app.config["FIRST_DAY_WEEK"])

    current_day, current_month, current_year = GregorianCalendar.current_date()

    if (year is None) and (month is None):
        year = current_year
        month = current_month
        day = current_day
    else:
        year = int(year)
        month = int(month)
        day = int(day)

    weekday_name = current_app.config["WEEK_DAYS"][GregorianCalendar.num_weekdays(year, month, day)]

    month_name = GregorianCalendar.MONTH_NAMES[month - 1]

    date = [year, month, day]
    edb = EventsDataBase()
    events = []
    if not request.cookies.get("is_logined"):
        print("nothing")
    else:
        uId = request.cookies.get("is_logined")
        events = edb.getDayEvents(uId, date)
        print("events: %s" % events)
    events = [[events[x][0], events[x][1], int(events[x][2]), events[x][3]] for x in range(len(events))]
    #print(events)
    return make_response(render_template(
        "calendar_day.html",
        day=day,
        weekday_name=weekday_name,
        month=month,
        year=year,
        month_name=month_name,
        current_day=current_day,
        current_month=current_month,
        current_year=current_year,
        events=events,
        previous_day_link=prev_day_link(year, month, day),
        next_day_link=next_day_link(year, month, day)
    )
    )


def home():
    if request.method == "POST":
        return registration()
    else:
        return render_template("main.html")


def registration():
    if request.method == "POST":
        name = request.form["username"]
        mail = request.form["mail"]
        password = request.form["password"]
        from User_class import User
        user = User(name, password, mail)
        code = user.send_code()
        user = user.to_SET()
        session["user"] = user
        session["code"] = code
        if code:
            return redirect("/check")
        else:
            return f"что-то пошло не так {code}"
    else:
        return render_template("register.html")


def check():
    if request.method == "POST":
        if "code" in session:
            if str(request.form["code"]) == str(session["code"]):
                session.pop("code", None)
                from User_class import User
                user = User(
                    session["user"]["name"],
                    session["user"]["password"],
                    session["user"]["mail"],
                )
                try:
                    session.pop("user", None)
                    if user.user_registration():
                        return redirect("/")
                    else:
                        return "Пользователь с такой почтой или именем уже есть."
                except:
                    session.pop("user", None)
                    return f"При добавлении пользователя произошла ошибка"
            else:
                session.pop("code", None)
                session.pop("user", None)
                return "Not Ok"
    else:
        return render_template("check.html")


def login():
    if request.method == "POST":
        from User_class import User
        name = request.form["login"]
        password = request.form["password"]
        user = User(name, password, name)
        try:
            res = user.login()
            if res != SearchExeption and res:
                # resp = make_response(render_template('calendar_month.html'))
                resp = make_response(redirect('/calendar/month/'))
                resp.set_cookie('is_logined', str(res[0]), 60 * 60 * 24)
                return resp
            elif res == SearchExeption:
                return "Произошла ошибка"
            else:
                return "Неверный логин или пароль"
        except:
            return "Произошла ошибка"
    else:
        return render_template("login.html")


def unLogin():
    if request.cookies.get('is_logined'):
        res = make_response(render_template('main.html'))
        res.set_cookie('is_logined', 'true', max_age=0)
        return res
    else:
        return "You aren't logined."


def is_Logined():
    if not request.cookies.get('is_logined'):
        return "You aren't logined."
    else:
        return redirect("/calendar/month")


def settings():
    if request.method == "POST":
        if request.form['submit'] == 'logout':
            if request.cookies.get('is_logined'):
                res = make_response(render_template('main.html'))
                res.set_cookie('is_logined', 'true', max_age=0)
                return res
            else:
                return "You aren't logined."
        elif request.form['submit'] == 'change':
            if request.cookies.get('is_logined'):
                res = make_response(redirect('/log'))
                res.set_cookie('is_logined', 'true', max_age=0)
                return res
            else:
                return "You aren't logined."
        elif request.form['submit'] == 'change_p':
            if request.cookies.get('is_logined'):
                res = make_response(redirect('/change_password'))
                return res
            else:
                return "You aren't logined."
    else:
        return render_template("settings.html")


def get_Info(day=None, month=None, year=None, num_hour=None):
    from DataBase_class import EventsDataBase
    if request.method == "GET":
        return render_template("addEvent.html", day=day, month=month, year=year, num_hour=num_hour)
    elif request.method == "POST":
        if request.form['submit'] == 'AI':
            import func.calendar_func as cf
            giga = GigaChatSDK(max_tokens=500)
            edb = EventsDataBase('')
            task_name = request.form['name']
            task_description = giga.requestGC(task_name)
            event = (task_name, task_description)
            freequency = ''
            try:
                freequency = request.form["frequency"]
            except:
                pass
            d_num = request.form["daynumber"]
            uId = 0
            if freequency != '':
                if d_num == '':
                    d_num = 0
                else:
                    d_num = int(d_num)

                n_dates = [[year, month, day, num_hour]]
                if freequency == "everyday":
                    for x in range(d_num):
                        n_dates.append(cf.next_day(n_dates[-1][0], n_dates[-1][1], n_dates[-1][2]) + [num_hour])
                elif freequency == "everyweek":
                    for x in range(d_num):
                        n_dates.append(cf.next_week(n_dates[-1][0], n_dates[-1][1], n_dates[-1][2]) + [num_hour])
                elif freequency == "everyyear":
                    for x in range(d_num):
                        n_dates.append(cf.next_year(n_dates[-1][0], n_dates[-1][1], n_dates[-1][2]) + [num_hour])

                if not request.cookies.get('is_logined'):
                    return "You aren't logined."
                else:
                    uId = request.cookies.get('is_logined')
                for x in n_dates:
                    edb.addEvent(uId, event, x)
            # получаем id
            date1 = [year, month, day]
            edb1 = EventsDataBase()
            events = []
            if not request.cookies.get("is_logined"):
                print("nothing")
            else:
                uId1 = request.cookies.get("is_logined")
                events = edb1.getDayEvents(uId1, date1)
            events = [[events[x][0], events[x][1], int(events[x][2]), events[x][3]] for x in range(len(events))]

            return redirect(f"/calendar/event/{year}/{month}/{day}/{num_hour}/{events[-1][3]}")

        elif request.form['submit'] == 'Подтвердить':
            import func.calendar_func as cf

            edb = EventsDataBase('')
            task_name = request.form['name']
            task_description = request.form['description']
            event = (task_name, task_description)
            freequency = ''
            try:
                freequency = request.form["frequency"]
            except:
                pass
            d_num = request.form["daynumber"]

            if freequency != '':
                if d_num == '':
                    d_num = 0
                else:
                    d_num = int(d_num)

                n_dates = [[year, month, day, num_hour]]
                if freequency == "everyday":
                    for x in range(d_num):
                        n_dates.append(cf.next_day(n_dates[-1][0], n_dates[-1][1], n_dates[-1][2]) + [num_hour])
                elif freequency == "everyweek":
                    for x in range(d_num):
                        n_dates.append(cf.next_week(n_dates[-1][0], n_dates[-1][1], n_dates[-1][2]) + [num_hour])
                elif freequency == "everyyear":
                    for x in range(d_num):
                        n_dates.append(cf.next_year(n_dates[-1][0], n_dates[-1][1], n_dates[-1][2]) + [num_hour])

                uId = 0
                if not request.cookies.get('is_logined'):
                    return "You aren't logined."
                else:
                    uId = request.cookies.get('is_logined')
                print(n_dates)
                for x in n_dates:
                    edb.addEvent(uId, event, x)
                return redirect(f"/calendar")

            uId = 0
            if not request.cookies.get('is_logined'):
                return "You aren't logined."
            else:
                uId = request.cookies.get('is_logined')
            edb.addEvent(uId, event, (year, month, day, num_hour))
            return redirect(f"/calendar")


def change_password():
    if request.method == "POST":
        from User_class import User
        mail = request.form["mail"]
        user = User(None, None, mail)
        code = user.send_code()
        session['code'] = code
        session['mail'] = mail
        if code:
            return redirect("/check_for_change")
        else:
            return f"что-то пошло не так {code}"
    return render_template("change_password.html")


def check_for_change():
    if request.method == "POST":
        if "code" in session:
            if str(request.form["code"]) == str(session["code"]):
                session.pop("code", None)
                return redirect("/change")
            else:
                session.pop("code", None)
                session.pop("mail", None)
                return "Не верный код"
        else:
            return "Произошла ошибка"
    return render_template("check.html")


def change():
    if request.method == "POST":
        if "mail" in session:
            from User_class import User
            mail = session["mail"]
            password = request.form["password"]
            user = User(None, password, mail)
            res = user.change_password(password)
            if res:
                session.pop('mail', None)
                return redirect("/")
            else:
                session.pop('mail', None)
                return "Произошла ошибка, попробуйте еще раз"
    return render_template("change.html")


def viewNote(year=None, month=None, day=None, time=None, id=None):
    from DataBase_class import EventsDataBase
    db = EventsDataBase()
    date = [year, month, day, time]
    if request.method == "GET":
        res = []
        if not request.cookies.get("is_logined"):
            return "Вы не вошли в аккаунт"
        else:
            uId = request.cookies.get("is_logined")

            print(f"calendar_day_page uId: {uId}  date: {date}  id: {id}")

            res = db.getEvent(uId, date, id)
        if int(day) < 10:
            day = "0" + str(day)
        if int(month) < 10:
            month = "0" + str(month)
        if int(time) < 10:
            time = "0" + str(time)
        return make_response(
            render_template(
                "event.html",
                event=res,
                year=year,
                month=month,
                day=day,
                time=time
            )
        )
    elif request.method == "POST":
        if request.form["submit"] == "save":
            name = request.form["title"]
            description = request.form["description"]
            n_date = request.form["calendar"]
            time = request.form["appt"]
            time = list(map(int, time.split(":")))
            n_date = list(map(int, n_date.split('-')))
            n_date.append(time[0])

            print("viewNote POST")


            print("viewNote POST date: %s" % date)
            print("viewNote POST n_date: %s" % n_date)

            if not request.cookies.get("is_logined"):
                return "Вы не вошли в аккаунт"
            else:
                uId = request.cookies.get("is_logined")
                print("viewNote POST uId: %s" % uId)
                db.updateEvent(uId, n_date, [name, description], date)
            return redirect("/calendar")
        elif request.form["submit"] == "delete":
            if not request.cookies.get("is_logined"):
                return "Вы не вошли в аккаунт"
            else:
                uId = request.cookies.get("is_logined")
                db.deleteEvent(uId, date, id)
            return make_response(redirect(f"/calendar/day/{year}/{month}/{day}"))
        elif request.form["submit"] == "ai":
            giga = GigaChatSDK(max_tokens=500)
            name = request.form["title"]
            description = giga.requestGC(name)
            if not request.cookies.get("is_logined"):
                return "Вы не вошли в аккаунт"
            else:
                uId = request.cookies.get("is_logined")
                db.updateEvent(uId, date, [name, description], date)
            return make_response(redirect(f"/calendar/event/{year}/{month}/{day}/{time}/{id}"))

