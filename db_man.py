import psycopg2
import os
import datetime
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv("OWNER")
db_name = os.getenv("DBNAME")
host_ip = os.getenv("HOST")
now = datetime.datetime.now()
time = now.strftime("%Y-%m-%d %H:%M:%S")


def connectdb():
    try:
        db_link = psycopg2.connect(user = user_name, host = host_ip, dbname = db_name)
        return db_link
    except Exception as e:
        print("VALBOT : DB connection status ===> 500")
        print(f"VALBOT : Error {e}")

def create_table():
    db_link = connectdb()
    yap = db_link.cursor()
    try:
        yap.execute('''CREATE TABLE IF NOT EXISTS idstore(channelid TEXT PRIMARY KEY, latest_vidid TEXT NOT NULL);''')
        db_link.commit()
        db_link.close()
    except Exception as e:
        print(f"VALBOT : Error {e}")

def add_id(channel_id, new_video_id):
    db_link  = connectdb()
    yap = db_link.cursor()
    try:
        yap.execute("INSERT INTO idstore(channelid, latest_vidid) VALUES (%s, %s) ON CONFLICT (channelid) DO UPDATE SET latest_vidid = EXCLUDED.latest_vidid", (channel_id, new_video_id))
        db_link.commit()
        db_link.close()
        print("VALBOT : Latest Video ID Conflict!\nVALBOT : Updated Latest Video ID!")
    except Exception as e:
        print(f"VALBOT : Error {e}")

def get_id(channel_id):
    db_link = connectdb()
    yap = db_link.cursor()
    try:
        yap.execute("SELECT latest_vidid FROM idstore WHERE channelid = %s",(channel_id,))
        result = yap.fetchone()
        fetch_id = result[0]
        return fetch_id
    except Exception as e:
        create_table()
        print(f"VALBOT : Error {e}")
