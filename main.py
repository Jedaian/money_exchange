from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedWidget
import os
import sys

from ui.customer_form import CustomerForm
from ui.purchase_form import PurchaseForm
from ui.search_history import SearchHistory

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Aplikasi Money Exchange')
        self.setMinimumSize(800, 600)
        self.showFullScreen()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.stack = QStackedWidget()

        self.menu_widget = QWidget()
        self.menu_layout = QVBoxLayout()

        self.label = QLabel("Selamat datang di Aplikasi Money Exchange")
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px")

        self.customer_btn = QPushButton('Form Input Customer')
        self.customer_btn.clicked.connect(self.show_customer_form)

        self.purchase_btn = QPushButton('Form Input Transaksi')
        self.purchase_btn.clicked.connect(self.show_purchase_form)

        self.history_btn = QPushButton('Cari Riwayat Transaksi')
        self.history_btn.clicked.connect(self.show_search_form)

        self.quit_btn = QPushButton('Keluar')
        self.quit_btn.clicked.connect(self.close)

        for btn in [self.customer_btn, self.purchase_btn, self.history_btn, self.quit_btn]:
            btn.setStyleSheet('padding: 10px; font-size: 18px')
        
        self.menu_layout.addWidget(self.label)
        self.menu_layout.addWidget(self.customer_btn)
        self.menu_layout.addWidget(self.purchase_btn)
        self.menu_layout.addWidget(self.history_btn)
        self.menu_layout.addStretch()
        self.menu_layout.addWidget(self.quit_btn)
        self.menu_widget.setLayout(self.menu_layout)

        self.customer_form = CustomerForm()
        self.purchase_form = PurchaseForm()
        self.search_form = SearchHistory()

        self.add_back_button(self.customer_form)
        self.add_back_button(self.purchase_form)
        self.add_back_button(self.search_form)

        self.stack.addWidget(self.menu_widget)
        self.stack.addWidget(self.customer_form)
        self.stack.addWidget(self.purchase_form)
        self.stack.addWidget(self.search_form)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.central_widget.setLayout(main_layout)

    def add_back_button(self, widget):
        back_btn = QPushButton('Kembali ke menu')
        back_btn.setStyleSheet('padding: 8px; font-size: 16px')
        back_btn.clicked.connect(self.go_to_menu)
        layout = widget.layout()
        if layout is not None:
            layout.addWidget(back_btn)

    def show_customer_form(self):
        self.stack.setCurrentWidget(self.customer_form)
    
    def show_purchase_form(self):
        self.stack.setCurrentWidget(self.purchase_form)

    def show_search_form(self):
        self.stack.setCurrentWidget(self.search_form)
    
    def go_to_menu(self):
        self.stack.setCurrentWidget(self.menu_widget)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())