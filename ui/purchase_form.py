from PyQt6.QtWidgets import (QLabel, QApplication, QWidget, QFormLayout, QLineEdit, 
                             QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import QDate, Qt
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

class PurchaseForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Purchase Form')

        self.label = QLabel("Input Data Transaksi")
        self.label.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px")

        self.name_input = QLineEdit()
        self.name_input.setMinimumWidth(200)

        self.nik_input = QLineEdit()
        self.nik_input.setMinimumWidth(200)

        self.jumlah_rupiah_input = QLineEdit()
        self.jumlah_rupiah_input.setMinimumWidth(200)

        form_layout = QFormLayout()
        form_layout.addRow(self.label)
        form_layout.addRow('Nama', self.name_input)
        form_layout.addRow('NIK', self.nik_input)
        form_layout.addRow('Jumlah Transaksi (Rupiah)', self.jumlah_rupiah_input)

        form_wrapper = QWidget()
        form_wrapper.setLayout(form_layout)

        centered_form_layout = QHBoxLayout()
        centered_form_layout.addStretch()
        centered_form_layout.addWidget(form_wrapper)
        centered_form_layout.addStretch()

        self.submit_button = QPushButton('Save')
        self.submit_button.clicked.connect(self.save_customer)

        main_layout = QVBoxLayout()
        main_layout.addSpacing(20)
        main_layout.addLayout(centered_form_layout)
        main_layout.addWidget(self.submit_button, alignment = Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(15)

        self.setLayout(main_layout)
    
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

            partial_name = f'%{name}%'
            cursor.execute("SELECT * FROM customers WHERE nama LIKE ? AND nik = ?", (partial_name, nik))
            customer = cursor.fetchone()

            if not customer:
                QMessageBox.warning(self, 'Data tidak ditemukan', 'Customer tidak ditemukan')
                conn.close()
                return
            
            print(customer)
            full_name = customer[2]

            confirmation_message = (
                f'Apakah data berikut sudah benar ?\n\n'
                f'Nama Lengkap: {full_name}\n'
                f'NIK: {nik}\n'
                f'Jumlah Transaksi: Rp{jumlah_transaksi_rupiah}'
            )

            reply = QMessageBox.question(self, 'Konfirmasi Data Customer', 
                                         confirmation_message, 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply != QMessageBox.StandardButton.Yes:
                return

            cursor.execute("""
                INSERT INTO purchase_history (nama, nik, tanggal_transaksi, jumlah_rupiah)
                        VALUES (?, ?, ?, ?)
                """, 
                (full_name, nik, tanggal_transaksi, jumlah_transaksi_rupiah))
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