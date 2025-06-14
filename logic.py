import sqlite3
import os

class WarJetDatabase:
    def __init__(self, db_name="war_jets.db"):
        self.db_name = db_name

    def create_tables(self):
        conn = sqlite3.connect(self.db_name)
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS jets (
                    jet_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jet_name TEXT NOT NULL
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS stats (
                    jet_id INTEGER,
                    kd_ratio TEXT,
                    FOREIGN KEY (jet_id) REFERENCES jets(jet_id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS abilities (
                    jet_id INTEGER,
                    max_speed INTEGER,
                    turn_ratio INTEGER,
                    max_takeoff_weight TEXT,
                    FOREIGN KEY (jet_id) REFERENCES jets(jet_id)
                )
            ''')

    def add_jet(self, jet_name):
        conn = sqlite3.connect(self.db_name)
        with conn:
            cursor = conn.execute('INSERT INTO jets (jet_name) VALUES (?)', (jet_name,))
            return cursor.lastrowid 

    def add_stats(self, jet_id, kd_ratio):
        conn = sqlite3.connect(self.db_name)
        with conn:
            conn.execute('INSERT INTO stats (jet_id, kd_ratio) VALUES (?, ?)', (jet_id, kd_ratio))

    def add_abilities(self, jet_id, max_speed, turn_ratio, max_takeoff_weight):
        conn = sqlite3.connect(self.db_name)
        with conn:
            conn.execute('''
                INSERT INTO abilities (jet_id, max_speed, turn_ratio, max_takeoff_weight)
                VALUES (?, ?, ?, ?)
            ''', (jet_id, max_speed, turn_ratio, max_takeoff_weight))


db = WarJetDatabase()
db.create_tables()

jets = [
    {
        "name": "F-22 Raptor",
        "kd": "4.5",
        "speed": 2410,
        "turn": 28,
        "weight": "38,000 kg"
    },
    {
        "name": "F-35 Lightning II",
        "kd": "3.8",
        "speed": 1930,
        "turn": 24,
        "weight": "31,800 kg"
    },
    {
        "name": "SU-27 Flanker",
        "kd": "2.9",
        "speed": 2500,
        "turn": 26,
        "weight": "30,000 kg"
    },
    {
        "name": "F-15 Eagle",
        "kd": "3.2",
        "speed": 2655,
        "turn": 25,
        "weight": "30,845 kg"
    },
    {
        "name": "F-14 Tomcat",
        "kd": "2.5",
        "speed": 2485,
        "turn": 22,
        "weight": "33,724 kg"
    }
]
for jet in jets:
    jet_id = db.add_jet(jet["name"])
    db.add_stats(jet_id, jet["kd"])
    db.add_abilities(jet_id, jet["speed"], jet["turn"], jet["weight"])
