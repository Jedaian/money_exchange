from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QStackedWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
import os
import sys

from utils import resource_path
from db import init_db_if_not_exists
from ui.customer_form import CustomerForm
from ui.purchase_form import PurchaseForm
from ui.search_history import SearchHistory
from ui.customer_list import CustomerList
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.setWindowTitle('Aplikasi Money Exchange')
        self.setMinimumSize(900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stack = QStackedWidget()

        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()

        self.label = QLabel("Selamat datang di Aplikasi Money Exchange")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.menu_layout.addStretch()
        self.menu_layout.addWidget(self.label)

        self.menu_layout.addLayout(self.centered_button("Form Input Customer", self.show_customer_form))
        self.menu_layout.addLayout(self.centered_button("Form Input Transaksi", self.show_purchase_form))
        self.menu_layout.addLayout(self.centered_button("Cari Riwayat Transaksi", self.show_search_form))
        self.menu_layout.addLayout(self.centered_button("Lihat Daftar Customer", self.show_customer_list))
        self.menu_layout.addStretch()
        self.menu_layout.addLayout(self.centered_button("Keluar", self.close))


        self.menu_widget.setLayout(self.menu_layout)

        self.customer_form = CustomerForm()
        self.purchase_form = PurchaseForm()
        self.search_form = SearchHistory()
        self.customer_list = CustomerList()

        self.add_back_button(self.customer_form)
        self.add_back_button(self.purchase_form)
        self.add_back_button(self.search_form)
        self.add_back_button(self.customer_list)

        self.stack.addWidget(self.menu_widget)
        self.stack.addWidget(self.customer_form)
        self.stack.addWidget(self.purchase_form)
        self.stack.addWidget(self.search_form)
        self.stack.addWidget(self.customer_list)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.central_widget.setLayout(main_layout)

    def centered_button(self, text, on_click_callback):
        button = QPushButton(text)
        button.setFixedWidth(300)
        button.setStyleSheet('padding: 10px; font-size: 18px')
        button.clicked.connect(on_click_callback)

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(button)
        hbox.addStretch()
        return hbox
    
    def add_back_button(self, widget):
        layout = widget.layout()
        if layout is not None:
            layout.addLayout(self.centered_button("Kembali ke menu", self.go_to_menu))

    def show_customer_form(self):
        self.stack.setCurrentWidget(self.customer_form)
    
    def show_purchase_form(self):
        self.stack.setCurrentWidget(self.purchase_form)

    def show_search_form(self):
        self.stack.setCurrentWidget(self.search_form)
    
    def show_customer_list(self):
        self.stack.setCurrentWidget(self.customer_list)
    
    def go_to_menu(self):
        if self.stack.currentWidget() == self.customer_form:
            self.customer_form.clear_fields()
        elif self.stack.currentWidget() == self.purchase_form:
            self.purchase_form.clear_fields()
        elif self.stack.currentWidget() == self.search_form:
            self.search_form.clear_fields()
        elif self.stack.currentWidget() == self.customer_list:
            self.customer_list.clear_fields()

        self.stack.setCurrentWidget(self.menu_widget)

if __name__ == '__main__':
    init_db_if_not_exists()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())