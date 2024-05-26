from flask import Flask, request
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from random import randint
from User_class import User


class Mail:
    def __init__(self, user:User=None):
        if user != None:
            self.user_mail = user.mail
            self.user_name = user.name
        self.bot_mail = "FootballSearchBot@yandex.ru"

    def send_email(self, message_text, header_text):
        login = "FootballSearchBot@yandex.ru"
        password = "yddbtfcmygtgmgqs"

        msg = MIMEText(f"{message_text}", "plain", "utf-8")
        msg["Subject"] = Header(header_text, "utf-8")
        msg["From"] = login
        msg["To"] = self.user_mail

        s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=10)
        is_sent = True
        try:
            s.starttls()
            s.login(login, password)
            s.sendmail(msg["From"], self.user_mail, msg.as_string())
            print("Email sent")
        except Exception as ex:
            is_sent = False
            print(ex)
        finally:
            s.quit()
            return is_sent

    def send_email_to(self, message_text: str, header_text: str, to: str):
        login = "FootballSearchBot@yandex.ru"
        password = "yddbtfcmygtgmgqs"

        msg = MIMEText(f"{message_text}", "plain", "utf-8")
        msg["Subject"] = Header(header_text, "utf-8")
        msg["From"] = login
        msg["To"] = to

        s = smtplib.SMTP("smtp.yandex.ru", 587, timeout=10)
        is_sent = True
        try:
            s.starttls()
            s.login(login, password)
            s.sendmail(msg["From"], to, msg.as_string())
            print("Email sent")
        except Exception as ex:
            is_sent = False
            print(ex)
        finally:
            s.quit()
            return is_sent