from flask import Flask
from data import db_session
from data.users import User
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():



if __name__ == '__main__':
    main()
