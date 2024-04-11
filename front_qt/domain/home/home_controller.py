from PyQt5.QtCore import QObject


class HomeController(QObject):
    def __init__(self):
        super().__init__()
        self.page, self.ui = self.setup_ui()
        self.setup_signals()
        self.setup_value()

    def setup_ui(self):
        from front_qt.tab_settings import home_page
        from front_qt.view.home_view import Ui_Form

        self.page = home_page[0]
        self.ui = Ui_Form()
        self.ui.setupUi(self.page)

        return self.page, self.ui

    def setup_signals(self):
        pass

    def setup_value(self):
        pass
