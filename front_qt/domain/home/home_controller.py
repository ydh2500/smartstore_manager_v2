from datetime import datetime

from PyQt5.QtCore import QObject


class HomeController(QObject):
    def __init__(self):
        super().__init__()
        self.all_changed_list = None
        self.page, self.ui = self.setup_ui()
        self.setup_signals()
        self.setup_value()

        self.initialize_ui()

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

    def initialize_ui(self):
        from front_qt.domain.home.home_request import get_all_changed_list
        today_strftime = datetime.now().strftime('%Y-%m-%d')  # ISO 8601 포맷
        self.all_changed_list = get_all_changed_list(today_strftime)

        self.ui.label.setText(f"전체 변경된 주문 리스트: {self.all_changed_list}")