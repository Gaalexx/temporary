import schedule
import time

def reminder():
    from DataBase_class import EventsDataBase, DataBase
    from Mail_class import Mail
    edb = EventsDataBase()
    db = DataBase()
    ml = Mail()
    print(time.strftime("%Y-%m-%d-%H").split('-'))
    def sendReminder():
        cur_date = time.strftime("%Y-%m-%d-%H").split('-')
        
        data = edb.getAllEventsDayOfAll(cur_date[:3])
        users = db.getAllUsers()
        print(data, users)
        for x in data:
            if cur_date[-1] == x[-1] + 1:
                ml.send_email_to(x[1], f"The event {x[0]} will begin soon!", users[x[2]])
                
    # Запланировать выполнение функции sendReminder каждые 60 минут с начала часа
    schedule.every().hour.at(":00").do(sendReminder)

    while True:
        schedule.run_pending()
        time.sleep(1)

reminder()