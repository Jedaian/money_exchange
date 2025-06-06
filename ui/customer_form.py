from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDateEdit
from PyQt6.QtCore import QDate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

class CustomerForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Entry Form")
        self.setGeometry(100, 100, 400, 350)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.nik_input = QLineEdit()
        self.tempat_lahir_input = QLineEdit()
        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setCalendarPopup(True)
        self.tanggal_lahir_input.setDisplayFormat('yyyy-MM-dd')
        self.tanggal_lahir_input.setDate(QDate.currentDate())
        self.alamat_input = QLineEdit()
        self.no_telp_input = QLineEdit()
        self.npwp_input = QLineEdit()

        layout.addRow('Nama', self.name_input)
        layout.addRow('NIK', self.nik_input)
        layout.addRow('Tempat Lahir', self.tempat_lahir_input)
        layout.addRow('Tanggal Lahir', self.tanggal_lahir_input)
        layout.addRow('Tempat Tinggal', self.alamat_input)
        layout.addRow('Nomor Handphone', self.no_telp_input)
        layout.addRow('No NPWP', self.npwp_input)

        self.submit_button = QPushButton('Save')
        self.submit_button.clicked.connect(self.save_customer)

        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        vbox.addWidget(self.submit_button)
        self.setLayout(vbox)
    
    def save_customer(self):
        name = self.name_input.text().strip()
        nik = self.nik_input.text().strip()
        tempat_lahir = self.tempat_lahir.text().strip()
        tanggal_lahir = self.tanggal_lahir.date().toString('yyyy-MM-dd')
        ttl = f'{tempat_lahir}, {tanggal_lahir}'
        alamat = self.alamat_input.text().strip()
        no_telp = self.no_telp_input.text().strip()
        npwp = self.npwp_input.text().strip()

        if not all([name, nik, ttl, alamat, no_telp]):
            QMessageBox(self, 'Error', 'Harap isi semua field diluar NPWP')
            return
        
        if not nik.is_digit() and len(nik) != 16:
            QMessageBox(self, 'Error', 'Nik harus terdiri dari 16 digit angka')
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (nama, nik, tempat_tanggal_lahir, alamat, no_telp, npwp)
                        VALUES (?, ?, ?, ?, ?, ?)
                """, 
                (name, nik, ttl, alamat, no_telp, npwp or None))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Sukses', 'Data pelanggan berhasil disimpan')
            self.clear_fields()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Gagal menyimpan data customer {str(e)}')

    def clear_fields(self):
        self.nama_input.clear()
        self.nik_input.clear()
        self.tempat_lahir_input.clear()
        self.tanggal_lahir.clear()
        self.alamat_input.clear()
        self.no_telp_input.clear()
        self.npwp_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CustomerForm()
    form.show()
    sys.exit(app.exec())