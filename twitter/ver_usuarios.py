# -*- coding: utf-8 -*-
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'twitter.db')

if not os.path.exists(DB_PATH):
    print("❌ No se encontró la base de datos twitter.db en esta carpeta.")
else:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute('SELECT id, username, password, bio FROM user;')
    registros = cur.fetchall()

    print(f"{'ID':<5} | {'USUARIO':<20} | {'PASSWORD':<12} | {'BIO'}")
    print("-" * 65)

    for row in registros:
        id_usr, username, password, bio = row
        print(f"{id_usr:<5} | {username:<20} | {password:<12} | {bio or ''}")

    con.close()
