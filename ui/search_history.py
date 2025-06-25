from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QHeaderView
import sys, os
import sqlite3
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_connection

class SearchHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cari Riwayat Transaksi")

        layout = QVBoxLayout()

        form_layout = QFormLayout()
        self.name_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.range_combo = QComboBox()
        self.range_combo.addItems(["Bulan ini", "3 Bulan terakhir", "6 Bulan terakhir", "1 tahun terakhir"])

        form_layout.addRow('Nama', self.name_input)
        form_layout.addRow('NIK', self.nik_input)
        form_layout.addRow('Periode', self.range_combo)

        self.search_button = QPushButton('Cari')
        self.search_button.clicked.connect(self.search)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(['Tanggal Transaksi', 'Jumlah Transaksi (Rp)'])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.total_label = QLabel('Total: Rp 0')

        layout.addLayout(form_layout)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_table)
        layout.addWidget(self.total_label)

        self.setLayout(layout)

    def search(self):
        name = self.name_input.text().strip()
        nik = self.nik_input.text().strip()

        if not all([name, nik]):
            QMessageBox.warning(self, 'Input tidak lengkap', 'Harap isi Nama dan NIK.')
            return
        
        if len(nik) != 16:
            QMessageBox.warning(self, 'Error', 'Harap isi NIK dengan 16 angka.')
            return
        
        today = datetime.today()
        range_option = self.range_combo.currentText()
        if range_option == 'Bulan ini':
            start_date = today.replace(day = 1)
        elif range_option == '3 Bulan terakhir':
            start_date = today - timedelta(days = 90)
        elif range_option == '6 Bulan terakhir':
            start_date = today - timedelta(days = 180)
        else:
            start_date = today - timedelta(days = 365)
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            start_date_str = start_date.strftime('%Y-%m-%d')
            cursor.execute("""
            SELECT tanggal_transaksi, jumlah_rupiah
            FROM purchase_history
            WHERE nama = ? AND nik = ? AND tanggal_transaksi >= ?
            ORDER BY tanggal_transaksi ASC
                           """, (name, nik, start_date_str))
            
            records = cursor.fetchall()
            conn.close()

            if not records:
                QMessageBox(self, 'Tidak ada data', 'Tidak ditemukan data transaksi pada periode ini')
                self.result_table.setRowCount(0)
                self.total_label.setText('Total Rp. 0')
                return
            
            self.result_table.setRowCount(len(records))
            total = 0
            for i, (tanggal, jumlah) in enumerate(records):
                self.result_table.setItem(i, 0, QTableWidgetItem(tanggal))
                self.result_table.setItem(i, 1, QTableWidgetItem(f'Rp. {int(jumlah):,}'))
                total += jumlah
            
            self.total_label.setText(f'Total: Rp {int(total):,}')
    
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Terjadi kesalahan saat mengambil data: \n{str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchHistory()
    window.showFullScreen()
    sys.exit(app.exec())