from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
import json
import hashlib
from email.header import Header
from random import randint


class User:
    def __init__(self, name, password, mail):
        self.name = name
        self.password = password
        self.mail = mail

    def send_code(self):
        from Mail_class import Mail

        mail_sender = Mail(self)
        code = randint(1000, 9999)
        flag = mail_sender.send_email(
            f"Hi, {self.name}!\nYour code is {code}", "Your code."
        )
        if flag:
            return code  # письмо отправилось - возвращаем код, иначе -1, что значит, что что-то не так
        else:
            return 0

    def to_JSON(self):
        return json.dumps(self, default=self._encode_user)

    def to_SET(self):
        return {"name": self.name, "password": self.password, "mail": self.mail}

    def _encode_user(self, user):
        if isinstance(user, User):
            return {"name": user.name, "password": user.password, "mail": user.mail}
        raise TypeError(f"Object {user} is not of type User")

    def login(self):
        from DataBase_class import DataBase

        db = DataBase("")
        return db.returnUserId(self)

    def user_registration(self):
        from DataBase_class import DataBase

        db = DataBase("qqq")
        self.password = hashlib.md5(
            bytes(self.password, encoding="utf8")
        ).hexdigest()  # bytes(self.password)
        return db.addUser(self)
    
    def change_password(self, pas):
        from DataBase_class import DataBase

        db = DataBase()
        return db.change_pas(pas, self)

