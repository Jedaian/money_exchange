from PyQt6.QtWidgets import (QLabel, QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QVBoxLayout)
from db import get_connection

class CustomerEditForm(QWidget):
    def __init__(self, nik, refresh_callback):
        super().__init__()
        self.nik = nik
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Edit Data Customer")
        self.setMinimumWidth(500)

        self.label = QLabel("Edit Data Customer")
        self.label.setStyleSheet("font-size: 20px; font-weight: boldl; margin: 10px")

        self.name_input = QLineEdit()
        self.name_input.setMinimumWidth(300)

        self.tempat_lahir_input = QLineEdit()
        self.tempat_lahir_input.setMinimumWidth(140)

        self.tanggal_lahir_input = QLineEdit()
        self.tanggal_lahir_input.setMinimumWidth(140)
        self.tanggal_lahir_input.setPlaceholderText("yyyy-mm-dd")

        ttl_layout = QHBoxLayout()
        ttl_layout.addWidget(self.tempat_lahir_input)
        ttl_layout.addWidget(self.tanggal_lahir_input)

        self.alamat_input = QLineEdit()
        self.alamat_input.setMinimumWidth(300)

        self.no_telp_input = QLineEdit()
        self.no_telp_input.setMinimumWidth(300)

        self.npwp_input = QLineEdit()
        self.npwp_input.setMinimumWidth(300)

        form_layout = QFormLayout()
        form_layout.addRow(self.label)
        form_layout.addRow("Nama", self.name_input)
        form_layout.addRow("Tempat & Tanggal Lahir", ttl_layout)
        form_layout.addRow("Alamat", self.alamat_input)
        form_layout.addRow("No HP", self.no_telp_input)
        form_layout.addRow("NPWP", self.npwp_input)

        self.save_button = QPushButton("Simpan")
        self.save_button.clicked.connect(self.save_changes)

        self.back_button = QPushButton("Kembali")
        self.back_button.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.save_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addSpacing(20)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        self.load_customer_data()

    def load_customer_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nama, tempat_tanggal_lahir, alamat, no_telp, npwp FROM customers WHERE nik = ?", (self.nik,))
        customer = cursor.fetchone()
        conn.close()

        if customer:
            self.name_input.setText(customer[0])
            if customer[1] and ',' in customer[1]:
                tempat, tanggal = customer[1].split(',', 1)
                self.tempat_lahir_input.setText(tempat.strip())
                self.tanggal_lahir_input.setText(tanggal.strip())
            else:
                self.tempat_lahir_input.setText(customer[1] or "")
                self.tanggal_lahir_input.setText("")
            self.alamat_input.setText(customer[2])
            self.no_telp_input.setText(customer[3])
            self.npwp_input.setText(customer[4] if customer[4] else "")

    def save_changes(self):
        name = self.name_input.text().strip()
        ttl = self.ttl_input.text().strip()
        alamat = self.alamat_input.text().strip()
        no_telp = self.no_telp_input.text().strip()
        npwp = self.npwp_input.text().strip()

        if not all([name, ttl, alamat, no_telp]):
            QMessageBox.warning(self, "Input Error", "Harap isi semua field kecuali NPWP.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET nama = ?, tempat_tanggal_lahir = ?, alamat = ?, no_telp = ?, npwp = ?
                WHERE nik = ?
            """, (name, ttl, alamat, no_telp, npwp or None, self.nik))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sukses", "Data customer berhasil diperbarui.")
            self.close()
            self.refresh_callback()  # refresh customer list table
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Gagal menyimpan perubahan: {str(e)}")
