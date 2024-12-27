import time

import requests
import selectorlib
import smtplib, ssl
from datetime import datetime
import streamlit as st
import pandas as pd
import sqlite3

URL = "http://programmer100.pythonanywhere.com/"

# Specify the database file name
database_file = "db_data.db"
# Create a connection to the SQLite database
connection = sqlite3.connect(database_file)
# Optionally, create a cursor to interact with the database
cursor = connection.cursor()


def scrape(url):
    """scrape the page source from URL"""
    response = requests.get(url)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["temp"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "eric.codes.qa@gmail.com"
    password = "krbc tgyv ljpj iasi"

    receiver = "eric.codes.qa@gmail.com"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

    print("Email was sent")


def store(extracted):
    with open("temp.csv", "a") as file:
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file.write(f"{current_datetime},{extracted} \n")

def store_db(extracted):
    temperature_value = int(extracted.strip())
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    cursor.execute("INSERT INTO temp (date, temp) VALUES (?, ?)", (current_datetime, temperature_value))
    connection.commit()

def read(extracted):
    with open("temp.csv", "r") as file:
        return file.read()

def read_db(extracted):
    print(extracted)

if __name__ == "__main__":
    for x in range(10):
        scraped = scrape(URL)
        print(scraped)
        extracted = extract(scraped)

        print(extracted)
        store_db(extracted)

        time.sleep(2)
        pass

    # df = pd.read_csv("temp.csv")
    #
    # df.columns = ["Date", "Temp"]
    # print(df)
    #
    # st.write("Data used for the graph:")
    # st.dataframe(df)
    #
    # st.title("Line Graph from DataFrame")
    # st.line_chart(df.set_index("Date"))




