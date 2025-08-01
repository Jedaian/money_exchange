from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QHeaderView, QVBoxLayout, QLineEdit, QTableWidget, 
                             QTableWidgetItem, QPushButton, QLabel, QMessageBox)
from db import get_connection
from ui.customer_edit import CustomerEditForm

class CustomerList(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer List")
        self.setMinimumWidth(900)

        title = QLabel("Daftar Seluruh Customer")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari nama atau NIK")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.filter_table)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.load_data)

        top_layout = QHBoxLayout()
        top_layout.addWidget(title)
        top_layout.addStretch()
        top_layout.addWidget(self.refresh_button)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Nama", "NIK", "Tempat & \nTanggal Lahir", 
            "Alamat", "No Telp", "NPWP", "Edit" , "Delete"
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("font-size: 14px")

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.search_input)
        main_layout.addWidget(self.table)
        

        self.setLayout(main_layout)
        self.load_data()

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_key = ON")
        cursor.execute("SELECT nama, nik, tempat_tanggal_lahir, alamat, no_telp, npwp FROM customers")
        self.customer_data = cursor.fetchall()
        conn.close()
        self.update_table(self.customer_data)

    def update_table(self, data):
        self.table.setRowCount(len(data))
        self.table.clearContents()

        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value) if value else "-")
                self.table.setItem(row_idx, col_idx, item)
            
            name = row_data[0]
            nik = row_data[1]
            
            #Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, x = nik: self.open_edit_form(x))
            self.table.setCellWidget(row_idx, 6, edit_btn)

            #Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, x = nik, y = name: self.confirm_delete(x, y))
            self.table.setCellWidget(row_idx, 7, delete_btn)

    def filter_table(self, text):
        filtered = []
        text = text.lower()

        for row in self.customer_data:
            name, nik = row[0], row[1]
            if text in name.lower() or text in nik.lower():
                filtered.append(row)
        
        self.update_table(filtered)

    def open_edit_form(self, nik):
        self.edit_form = CustomerEditForm(nik, self.refresh_after_edit)
        self.edit_form.show()
    
    def refresh_after_edit(self):
        self.load_data()

    def confirm_delete(self, nik, name):
        reply = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Apakah anda yakin ingin menghapus data kustomer: {name, nik} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.delete_customer(nik)
    
    def delete_customer(self, nik):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE nik = ?", (nik, ))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Berhasil", "Data Customer berhasil dihapus")
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Gagal", f"Terjadi kesalahan saat mencoba menghapus data: {str(e)}")
    
    def clear_fields(self):
        self.table.setRowCount(0)