from PyQt6.QtWidgets import QWidget, QFormLayout, QLineEdit, QPushButton, QMessageBox, QVBoxLayout
from db import get_connection

class CustomerEditForm(QWidget):
    def __init__(self, nik, refresh_callback):
        super().__init__()
        self.nik = nik
        self.refresh_callback = refresh_callback
        self.setWindowTitle("Edit Data Customer")
        self.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.ttl_input = QLineEdit()
        self.alamat_input = QLineEdit()
        self.no_telp_input = QLineEdit()
        self.npwp_input = QLineEdit()

        layout.addRow("Nama", self.name_input)
        layout.addRow("Tempat & Tanggal Lahir", self.ttl_input)
        layout.addRow("Alamat", self.alamat_input)
        layout.addRow("No HP", self.no_telp_input)
        layout.addRow("NPWP", self.npwp_input)

        self.save_button = QPushButton("Simpan")
        self.save_button.clicked.connect(self.save_changes)

        vbox = QVBoxLayout()
        vbox.addLayout(layout)
        vbox.addWidget(self.save_button)
        self.setLayout(vbox)

        self.load_customer_data()

    def load_customer_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nama, tempat_tanggal_lahir, alamat, no_telp, npwp FROM customers WHERE nik = ?", (self.nik,))
        customer = cursor.fetchone()
        conn.close()

        if customer:
            self.name_input.setText(customer[0])
            self.ttl_input.setText(customer[1])
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
