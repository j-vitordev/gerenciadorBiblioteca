# backend/conexao.py

import pyodbc
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv(dotenv_path=Path(__file__).resolve().parent / "credenciais.env")

def conectar():
    driver = os.getenv('DB_DRIVER')
    server = os.getenv('DB_SERVER')
    database = os.getenv('DB_NAME')
    trusted_connection = os.getenv('DB_TRUSTED')

    if not all([driver, server, database, trusted_connection]):
        raise ValueError("Faltam variáveis de ambiente!")

    conn_str = (
        f"DRIVER={{{driver}}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection={trusted_connection}"
    )

    return pyodbc.connect(conn_str)
