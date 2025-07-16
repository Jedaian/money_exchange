from PyQt6.QtWidgets import QLabel, QApplication, QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDateEdit
from PyQt6.QtCore import QDate
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

class CustomerForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Entry Form")

        layout = QFormLayout()

        self.label = QLabel("Input Data Customer")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px")

        self.name_input = QLineEdit()
        self.name_input.setMinimumWidth(200)

        self.nik_input = QLineEdit()
        self.nik_input.setMinimumWidth(200)

        self.tempat_lahir_input = QLineEdit()
        self.tempat_lahir_input.setMinimumWidth(200)

        self.tanggal_lahir_input = QDateEdit()
        self.tanggal_lahir_input.setCalendarPopup(True)
        self.tanggal_lahir_input.setDisplayFormat('yyyy-MM-dd')
        self.tanggal_lahir_input.setDate(QDate.currentDate())

        self.alamat_input = QLineEdit()
        self.alamat_input.setMinimumWidth(200)

        self.no_telp_input = QLineEdit()
        self.no_telp_input.setMinimumWidth(200)

        self.npwp_input = QLineEdit()
        self.npwp_input.setMinimumWidth(200)

        layout.addRow(self.label)
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
        tempat_lahir = self.tempat_lahir_input.text().strip()
        tanggal_lahir = self.tanggal_lahir_input.date().toString('yyyy-MM-dd')
        ttl = f'{tempat_lahir}, {tanggal_lahir}'
        alamat = self.alamat_input.text().strip()
        no_telp = self.no_telp_input.text().strip()
        npwp = self.npwp_input.text().strip()

        if not all([name, nik, ttl, alamat, no_telp]):
            QMessageBox.critical(self, 'Error', 'Harap isi semua field diluar NPWP')
            return
        
        if nik.isdigit() and len(nik) != 16:
            QMessageBox.critical(self, 'Error', 'Nik harus terdiri dari 16 digit angka')
            return
        
        try:
            conn = get_connection()
            cursor = conn.cursor()

            #Check NIK
            cursor.execute("SELECT * FROM customers WHERE nik = ?", (nik))
            if cursor.fetchone():
                QMessageBox.warning(self, 'Data Duplikat', 'Data Customer dengan NIK ini sudah ada.')
                conn.close()
                return
            
            confirmation_message = (
                f'Apakah data berikut sudah benar ?\n\n'
                f'Nama: {name}\n'
                f'NIK: {nik}\n'
                f'Tempat & Tanggal Lahir: {ttl}\n'
                f'Alamat: {alamat}\n'
                f'No Telp: {no_telp}\n'
                f'NPWP: {npwp or "-"}'
            )

            reply = QMessageBox.question(self, 'Konfirmasi Data Customer', 
                                         confirmation_message, 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply != QMessageBox.StandardButton.Yes:
                return

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
            QMessageBox.critical(self, 'Error', f'Gagal menyimpan data customer: {str(e)}')

    def clear_fields(self):
        self.name_input.clear()
        self.nik_input.clear()
        self.tempat_lahir_input.clear()
        self.tanggal_lahir_input.clear()
        self.alamat_input.clear()
        self.no_telp_input.clear()
        self.npwp_input.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = CustomerForm()
    form.showFullScreen()
    sys.exit(app.exec())