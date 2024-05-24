from flask import Flask, request, render_template
from flask import render_template_string
from Exceptions import SearchExeption
#from app import app
import sqlite3


class DataBase:
    from User_class import User

    def __init__(self, path=None):
        self.path = path
        self._connection = sqlite3.connect("instance/userInfo.db")
        self._cursor = self._connection.cursor()

    def addUser(self, user: User):
        res = self._checkForDif(user)
        if res != SearchExeption and not res:
            try:
                self._cursor.execute(
                    "INSERT INTO userInfo (username, mail, password) VALUES (?, ?, ?)",
                    (f"{user.name}", f"{user.mail}", f"{user.password}"),
                )
                self._connection.commit()
                self._connection.close()
                return True
            except:
                print("Ошибка при добавлении ползователя в базу данных")
                return False
        else:
            return False
        
    def returnUserId(self, user: User):
        res = self._checkForLog(user)
        print(res)
        return res[0]

    def _checkForDif(self, user: User):
        try:
            self._cursor.execute(
                "SELECT username, mail FROM userInfo WHERE username = ? OR mail = ?",
                (f"{user.name}", f"{user.mail}"),
            )
            results = self._cursor.fetchall()

            if len(results) != 0:
                return True
            else:
                return False
        except:
            return SearchExeption

    def _checkForLog(self, user: User):
        import hashlib

        user.password = hashlib.md5(bytes(user.password, encoding="utf8")).hexdigest()
        try:
            self._cursor.execute(
                "SELECT id, username, mail FROM userInfo WHERE (username = ? OR mail = ?) AND password = ?",
                (f"{user.name}", f"{user.mail}", f"{user.password}"),
            )
            results = self._cursor.fetchall()

            if len(results) != 0:
                return results
            else:
                return False
        except:
            return SearchExeption
    
    def change_pas(self, pas, user: User):
        import hashlib

        pas = hashlib.md5(bytes(pas, encoding="utf8")).hexdigest()
        try:
            self._cursor.execute(
                "UPDATE userInfo SET password = ? WHERE mail = ?", (pas, user.mail),
            )
            self._connection.commit()
            self._cursor.close()
            return True
        except:
            return False
        

class EventsDataBase():
    from User_class import User

    def __init__(self, path = None):
        self.path = path
        self._connection = sqlite3.connect("instance/userInfo.db")
        self._cursor = self._connection.cursor()
    
    def addEvent(self, userId, event, date):
        try:
            self._connection = sqlite3.connect("instance/userInfo.db")
            self._cursor = self._connection.cursor()
            self._cursor.execute(
                        "INSERT INTO eventsInfo (userId, name, description, year, month, day, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (f"{userId[0]}", f"{event[0]}", f"{event[1]}", f"{date[0]}", f"{date[1]}", f"{date[2]}", f"{date[3]}"),
                    )
            self._connection.commit()
            self._connection.close()
            return True
        except:
           return False
    
    def deleteEvent(self, userId, date, id):
        try:
            #self._connection = sqlite3.connect("instance/userInfo.db")
            self._cursor.execute(
                            "DELETE FROM eventsInfo WHERE userId = ? AND year = ? AND month = ? AND day = ? AND time = ? AND Id = ?",
                            (f"{userId[0]}", f"{date[0]}", f"{date[1]}", f"{date[2]}", f"{date[3]}", f"{id}"),
                        )
            self._connection.commit()
            self._connection.close()
            return True
        except:
            return False
    
    def getAllEventsMonth(self, userId, month):
        try:
            self._cursor.execute(
                "SELECT description, name, day FROM eventsInfo WHERE (userId = ? AND month = ?)",
                (f"{userId}", f"{month}"),
            )
            results = self._cursor.fetchall()
            res = list(set(int(results[x][-1]) for x in range(len(results))))
            if len(res) != 0:
                return res
            else:
                return []
        except:
            return SearchExeption
    
    def getAllEventsWeek(self, userId, month):
        try:
            self._cursor.execute(
                "SELECT description, name, year, month, day, time FROM eventsInfo WHERE (userId = ? AND month = ?)",
                (f"{userId}", f"{month}"),
            )
            results = self._cursor.fetchall()
            res = [[int(results[x][-4]), int(results[x][-3]), int(results[x][-2]), int(results[x][-1]), str(results[x][1])] for x in range(len(results))]
            if len(res) != 0:
                return res
            else:
                return []
        except:
            return SearchExeption
    
    def getEvent(self, userId, date, id):
        try:
            self._cursor.execute(
                "SELECT name, description FROM eventsInfo WHERE (userId = ? AND year = ? AND month = ? and day = ? and time = ? and Id = ?)",
                (f"{userId}", f"{date[0]}", f"{date[1]}", f"{date[2]}", f"{date[3]}", f"{id}"),
            )
            results = self._cursor.fetchall()
            if len(results) != 0:
                return list(results[0])
            else:
                return []
        except:
            return SearchExeption #изменить ошибку
    
    def getDayEvents(self, userId, date):
        try:
            self._cursor.execute(
                "SELECT name, description, time, id FROM eventsInfo WHERE (userId = ? AND year = ? AND month = ? and day = ?)",
                (f"{userId}", f"{date[0]}", f"{date[1]}", f"{date[2]}"),
            )
            results = self._cursor.fetchall()
            if len(results) != 0:
                return list(results)
            else:
                return []
        except:
            return SearchExeption #изменить ошибку
    
    def updateEvent(self, userId, new_date, information, old_date):
        try:
            self._cursor.execute(
                    "UPDATE eventsInfo SET name = ?, description = ?, year = ?, month = ?, day = ?, time = ? WHERE userId = ? AND year = ? AND month = ? AND day = ? and time = ?",
                    (f"{information[0]}", f"{information[1]}", f"{new_date[0]}", f"{new_date[1]}", f"{new_date[2]}", f"{new_date[3]}", f"{userId}", f"{old_date[0]}", f"{old_date[1]}", f"{old_date[2]}", f"{old_date[3]}"),
                )
            self._connection.commit()
            self._cursor.close()
        except:
            print("Ошибка при изменении события")