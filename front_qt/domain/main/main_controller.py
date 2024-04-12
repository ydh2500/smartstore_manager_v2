from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget



class MainController(QObject):
    def __init__(self):
        super().__init__()
        self.main_window, self.ui = self.setup_ui()
        self.setup_signals()
        self.setup_value()
        self.setup_tab_pages(self.ui.tabWidget_main)


    def setup_ui(self):
        from front_qt.view.main_window import Ui_MainWindow

        main_window = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(main_window)

        return main_window, ui

    def setup_signals(self):
        pass

    def setup_value(self):
        pass

    def show(self):
        self.main_window.show()

    @staticmethod
    def setup_tab_pages(tabWidget):
        from front_qt.tab_settings import tab_order
        for tab in tab_order:
            widget = tab[0]
            name = tab[1]
            tabWidget.addTab(widget, name)