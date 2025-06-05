import sqlite3

db_name = 'database.db'

def get_connection():
    return sqlite3.connect(db_name)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            nama TEXT NOT NULL,
            nik TEXT PRIMARY KEY,
            tempat_tanggal_lahir TEXT NOT NULL,
            alamat TEXT NOT NULL,
            no_telp TEXT NOT NULL,
            npwp TEXT NULLABLE
            )
            """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            nik TEXT NOT NULL,
            tanggal_transaksi DATE,
            jumlah_rupiah INTEGER NOT NULL,
            FOREIGN KEY(nik) REFERENCES customers(nik)
            )
            """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print('Database and tables initialized')