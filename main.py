import time

import requests
import selectorlib
import smtplib
import ssl
import sqlite3

URL = "http://programmer100.pythonanywhere.com/tours/"
connection = sqlite3.connect("db_data.db")


def scrape(url):
    """scrape the page source from URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "e...a@gmail.com"
    password = "k...i"

    receiver = "e...a@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email was sent")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def store_db(extracted):

    row = extracted.split(",")
    row = [x.strip() for x in row]
    print(row)

    # connect to DB and write data
    cursor = connection.cursor()

    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


def read_db(extracted):
    row = extracted.split(",")
    row = [x.strip() for x in row]
    print(row)
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    print(cursor)
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print("EXTRACTED " + str(extracted))

        if extracted != "No upcoming tours":
            row = read_db(extracted)
            if not row:
                store_db(extracted)
                send_email(message="new event found")

        time.sleep(1)
