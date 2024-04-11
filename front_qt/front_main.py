import sys
import traceback

from PyQt5 import QtWidgets

from front_qt.domain.home.home_controller import HomeController
from front_qt.domain.main.main_controller import MainController

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        main_controller = MainController()
        home_controller = HomeController()



        main_controller.show()
        sys.exit(app.exec_())
    except Exception as e:
        traceback.print_exc()
