import mysql
import mysql.connector
import os
import PySimpleGUI as sg
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnector:
    def __init__(self):
        self.host = os.getenv("HOST")
        self.username = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.database = os.getenv("DATABASE")
    
    def connect_database(self, sql):
        with mysql.connector.connect(username=self.username,
                                    password=self.password,
                                    host=self.host,
                                    database=self.database) as con:
            try:
                cur = con.cursor()
                cur.execute(sql)
                con.commit()
            except mysql.connector.Error as error:
                print(error)
            else:
                return "Successful!"

    def select_fetchall(self, query):
            with mysql.connector.connect(username=self.username,
                                    password=self.password,
                                    host=self.host,
                                    database=self.database) as con:
                try:
                    cur = con.cursor()
                    cur.execute(query)
                    result = cur.fetchall()
                except mysql.connector.Error as error:
                    print(error)
                
                else:
                    return result

    def select_fetchone(self, query):
        with mysql.connector.connect(username=self.username,
                                    password=self.password,
                                    host=self.host,
                                    database=self.database) as con:
            try:
                cur = con.cursor()
                cur.execute(query)
                result = cur.fetchone()
            except mysql.connector.Error as error:
                print(error)
            
            else:
                return result
            
    def insert_register(self, username, email, phone_number, birth, password, sexo):
        self.connect_database(f"""INSERT INTO users (username, email, phone_number, birth, password, sexo)
                            VALUES ('{username}','{email}','{phone_number}','{birth}','{password}','{sexo}');""")  
            
    def select_id_users(self, email):
        id_user = self.select_fetchone(f"SELECT user_id FROM users WHERE email='{email}'")
        return id_user
    
    def insert_table_codes_user_id(self, user_id, code):
        self.connect_database(f"INSERT INTO codes (user_id, code) VALUES ({user_id},'{code}')")

    def select_code_user_id(self, code):
        code = self.select_fetchall(f"SELECT user_id, code FROM codes WHERE code='{code}'")
        return code
    
    def select_change_password(self, password):
        password = self.select_fetchall(f"SELECT password FROM users WHERE password='{password}'")
        return password[0][0]
    
    def select_change_email(self, email):
        email = self.select_fetchall(f"SELECT email FROM users WHERE email='{email}'")
        return email[0][0]
    

# Craindo as tabelas de cadastro de usuário e código para recuperar a conta do usuário
db = DatabaseConnector()
db.connect_database(f"""
    CREATE TABLE IF NOT EXISTS users(
    user_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username varchar(30) NOT NULL UNIQUE,
    email varchar(100) NOT NULL UNIQUE,
    phone_number varchar(30) NOT NULL UNIQUE,
    birth date NOT NULL,
    password varchar(64) NOT NULL UNIQUE,
    sexo enum('M','F') NOT NULL);
""")    

db.connect_database("""
CREATE TABLE IF NOT EXISTS codes(
user_id int NOT NULL,
code char(4) UNIQUE NOT NULL,
PRIMARY KEY (user_id),
FOREIGN KEY (user_id) REFERENCES users(user_id)
);
""")

