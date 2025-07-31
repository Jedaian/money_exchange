import os
import sqlite3
from pathlib import Path

def get_db_path():
    # Cross-platform user data folder (e.g., ~/.money_exchange or AppData)
    app_dir = Path.home() / '.money_exchange'
    print(f"Expected app_dir: {app_dir}")  # 🐛 Debug line
    app_dir.mkdir(parents=True, exist_ok=True)
    return str(app_dir / 'database.db')



def init_db_if_not_exists():
    db_path = get_db_path()

    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    if not os.path.exists(db_path):
        print("Initializing new database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ✅ Define your schema here (adjust to your actual structure!)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nik TEXT UNIQUE,
            nama TEXT NOT NULL,
            tempat_tanggal_lahir TEXT NOT NULL,
            alamat TEXT NOT NULL,
            no_telp TEXT NOT NULL,
            npwp TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nik TEXT NOT NULL,
            tanggal_transaksi DATE,
            jumlah_rupiah INTEGER NOT NULL,
            FOREIGN KEY(nik) REFERENCES customers(nik) ON DELETE CASCADE
            )
            """)
        conn.commit()
        conn.close()

def get_connection():
    init_db_if_not_exists()
    return sqlite3.connect(get_db_path())