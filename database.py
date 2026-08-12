import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def crear_tabla():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            code INTEGER PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            price FLOAT NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def crear_tabla_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) PRIMARY KEY,
            password VARCHAR(50) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def crear_tabla_empleados():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            document INTEGER PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            position VARCHAR(50) NOT NULL,
            salary FLOAT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def crear_tabla_categorias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def crear_tabla_productos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(150) NOT NULL,
            precio NUMERIC(10,2) NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            categoria_id INTEGER NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()