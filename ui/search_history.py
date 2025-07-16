from PyQt6.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QComboBox, 
                             QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QHeaderView)
import sys, os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from db import get_connection

class SearchHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cari Riwayat Transaksi")

        self.label = QLabel("Search Data Transaksi")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px")

        self.name_input = QLineEdit()
        self.name_input.setMinimumWidth(200)

        self.nik_input = QLineEdit()
        self.nik_input.setMinimumWidth(200)

        self.range_combo = QComboBox()
        self.range_combo.addItems(["Bulan ini", "3 Bulan terakhir", "6 Bulan terakhir", "1 tahun terakhir"])

        form_layout = QFormLayout()
        form_layout.addRow(self.label)
        form_layout.addRow('Nama', self.name_input)
        form_layout.addRow('NIK', self.nik_input)
        form_layout.addRow('Periode', self.range_combo)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)

        centered_form_layout = QHBoxLayout()
        centered_form_layout.addStretch()
        centered_form_layout.addWidget(form_widget)
        centered_form_layout.addStretch()

        self.search_button = QPushButton('Cari')
        self.search_button.clicked.connect(self.search)

        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(['Tanggal Transaksi', 'Jumlah Transaksi (Rp)'])
        self.result_table.horizontalHeader().setStretchLastSection(True)
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.result_table.verticalHeader().setVisible(False)

        self.total_label = QLabel('Total: Rp 0')
        self.total_label.setStyleSheet("font-weight: bold; margin-top: 5px")
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(centered_form_layout)
        main_layout.addWidget(self.search_button)
        main_layout.addWidget(self.result_table)
        main_layout.addWidget(self.total_label)
        main_layout.addStretch()
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(15)

        self.setLayout(main_layout)

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

            cursor.execute("SELECT * FROM customers WHERE nik = ?", (nik, ))
            if cursor.fetchone() is None:
                QMessageBox.warning(self, "NIK tidak ditemukan", "NIK yang Anda masukkan tidak terdaftar")
                self.result_table.setRowCount(0)
                self.total_label.setText("Total Rp. 0")
                conn.close()
                return

            start_date_str = start_date.strftime("%Y-%m-%d")
            partial_name = f'%{name}%'
            cursor.execute("""
            SELECT tanggal_transaksi, jumlah_rupiah
            FROM purchase_history
            WHERE nama LIKE ? AND nik = ? AND tanggal_transaksi >= ?
            ORDER BY tanggal_transaksi ASC
            """, (partial_name, nik, start_date_str))
            
            records = cursor.fetchall()
            conn.close()

            if not records:
                QMessageBox.critical(self, 'Tidak ada data', 'Tidak ditemukan data transaksi pada periode ini')
                self.result_table.setRowCount(0)
                self.total_label.setText('Total Rp. 0')
                return
            
            self.result_table.setRowCount(len(records))
            total = 0
            
            for i, (tanggal, jumlah) in enumerate(records):
                try:
                    tanggal_obj = datetime.strptime(tanggal, '%Y-%m-%d')
                    tanggal_formatted = tanggal_obj.strftime('%-d %B %Y')
                except:
                    tanggal_formatted = tanggal
    
                self.result_table.setItem(i, 0, QTableWidgetItem(tanggal_formatted))
                self.result_table.setItem(i, 1, QTableWidgetItem(f'Rp. {int(jumlah):,}'))
                total += jumlah
            
            self.total_label.setText(f'Total: Rp {int(total):,}')
    
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Terjadi kesalahan saat mengambil data: \n{str(e)}')
    
    def clear_fields(self):
        self.name_input.clear()
        self.nik_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SearchHistory()
    window.showFullScreen()
    sys.exit(app.exec())