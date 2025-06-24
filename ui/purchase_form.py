from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDateEdit, QDoubleSpinBox
from PyQt6.QtCore import QDate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

class PurchaseForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Purchase Form')

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.jumlah_rupiah_input = QLineEdit()

        layout.addRow('Nama', self.name_input)
        layout.addRow('NIK', self.nik_input)
        layout.addRow('Jumlah Transaksi (Rupiah)', self.jumlah_rupiah_input)

        self.submit_button = QPushButton('save')
        self.submit_button.clicked.connect(self.save_customer)

        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        vbox.addWidget(self.submit_button)
        self.setLayout(vbox)
    
    def save_customer(self):
        name = self.name_input.text().strip()
        nik = self.nik_input.text().strip()
        tanggal_transaksi = QDate.currentDate().toString('yyyy-MM-dd')
        jumlah_transaksi_rupiah = int(self.jumlah_rupiah_input.text())

        if not all([name, nik]) or jumlah_transaksi_rupiah <= 0:
            QMessageBox.warning(self, 'Error', 'Harap lengkapi data pelanggan beserta jumlah transaksi')
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO purchase_history (nama, nik, tanggal_transaksi, jumlah_rupiah)
                        VALUES (?, ?, ?, ?)
                """, 
                (name, nik, tanggal_transaksi, jumlah_transaksi_rupiah))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Sukses', f'Transaksi untuk {name}, {nik} pada tanggal {tanggal_transaksi} berhasil disimpan')
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Gagal untuk menyimpan data transaksi: {str(e)}')
    
    def clear_fields(self):
        self.name_input.clear()
        self.nik_input.clear()
        self.jumlah_rupiah_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = PurchaseForm()
    form.showFullScreen()
    sys.exit(app.exec())