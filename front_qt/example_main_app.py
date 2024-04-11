import os
import multiprocessing
import sys
import threading
import time

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QMessageBox, QAction

from ringdown.ringdown_manager import RingdownManager
from data_stream.buffer_manager import BufferManager
from data_stream.data_stream_thread import DataStreamThread
from daq.analog_input_scan_manager import AnalogInputScanManager
from daq.analog_output_generator import AnalogOutputScanGenerator
from daq.board_manager import BoardManager
from front import ringdown_tab_view
from front.mcu_tab_controller import McuTabController
from front.signal_quality_tab_controller import QualityTabController
from front.ringdown_tab_controller import RingdownTabController
from front.results_tab_controller import ResultsTabController
from front.tcp_tab_controller import TCPTabController

from front.settings_tab_controller import SettingsTabController
from mcu.mcu_manager import MCUManager
from results.results_manager import ResultsManager
from results.smoothing_activation_function import SmoothingActivationFunction
from results.smoothing_manager import SmoothingManager
from settings.settings_manager import SettingsManager
from signal_quality.signal_quality_manager import SignalQualityManager
from tcp.TCP_manager import TCPManager
from front.activate_window import activate_window
from dataview.dataview_main import dataview_main


__version__ = '1.0.0'

class MainApp(QMainWindow):
    def __init__(self, board_manager: BoardManager,
                 # ao_generator: AnalogOutputScanGenerator,
                 # ai_scan_manager: AnalogInputScanManager,
                 data_stream_thread: DataStreamThread,
                 buffer_manager: BufferManager,
                 settings_manager: SettingsManager,
                 ringdown_manager: RingdownManager,
                 signal_quality_manager: SignalQualityManager,
                 mcu_manager: MCUManager,
                 results_manager: ResultsManager,
                 smoothing_manager: SmoothingManager,
                 tcp_manager: TCPManager):
        super().__init__()

        self.quality_tab_controller = None
        self.results_tab_page = None
        self.controllers = None
        self.tab_order = None
        self.mcu_tab_controller = None
        self.settings_tab_page = None
        self.ringdown_tab_page = None
        self.mcu_tab_page = None
        self.tcp_tab_page = None
        self.ringdown_tab_controller = None
        self.settings_tab_controller = None
        self.tcp_tab_controller = None
        self.setWindowTitle("WITHTECH CRDS System v{}".format(__version__))
        self.setGeometry(100, 100, 800, 900)
        self.setFont(QFont("Arial"))

        self.process_alive = None
        self.__process_check_thread = None

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.board_manager = board_manager
        self.ao_generator = board_manager.ao_generator
        self.ai_scan_manager = board_manager.ai_scan_manager
        self.waveform_settings = self.ao_generator.get_waveform_settings()
        self.data_stream_thread = data_stream_thread
        self.buffer_manager = buffer_manager
        self.settings_manager = settings_manager
        self.ringdown_manager = ringdown_manager
        self.mcu_manager = mcu_manager
        self.results_manager = results_manager
        self.smoothing_manager = smoothing_manager
        self.tcp_manager = tcp_manager
        self.signal_quality_manager = signal_quality_manager

        self.setup_ui()
        self.setup_controller()

        self.setup_menubar()

    def setup_ui(self):
        self.settings_tab_page = QWidget()  # SettingsTabView()
        self.ringdown_tab_page = QWidget()
        self.quality_tab_page = QWidget()
        self.results_tab_page = QWidget()
        self.mcu_tab_page = QWidget()
        self.tcp_tab_page = QWidget()

        self.tab_order = [
            (self.settings_tab_page, 'Settings'),
            (self.ringdown_tab_page, 'Ringdown'),
            (self.quality_tab_page, 'Quality'),
            (self.results_tab_page, 'Results'),
            (self.mcu_tab_page, 'MCU'),
            (self.tcp_tab_page, 'TCP')]

        for page, name in self.tab_order:
            self.tab_widget.addTab(page, name)

    def setup_controller(self):
        self.settings_tab_controller = SettingsTabController(page=self.settings_tab_page,
                                                             board_manager=self.board_manager,
                                                             ao_generator=self.ao_generator,
                                                             ai_scan_manager=self.ai_scan_manager,
                                                             settings_manager=self.settings_manager,
                                                             analysis_manager=self.ringdown_manager,
                                                             data_stream_thread=self.data_stream_thread,
                                                             buffer_manager=self.buffer_manager,
                                                             mcu_manager=self.mcu_manager,
                                                             results_manager=self.results_manager,
                                                             quality_manager=self.signal_quality_manager,)

        self.ringdown_tab_controller = RingdownTabController(page=self.ringdown_tab_page,
                                                             settings_manager=self.settings_manager,
                                                             ringdown_manager=self.ringdown_manager,
                                                             buffer_manager=self.buffer_manager,
                                                             results_manager=self.results_manager, )

        self.quality_tab_controller = QualityTabController(page=self.quality_tab_page,
                                                           settings_manager=self.settings_manager,
                                                           quality_manager=self.signal_quality_manager,
                                                           results_manager=self.results_manager, )

        self.mcu_tab_controller = McuTabController(page=self.mcu_tab_page,
                                                   mcu_manager=self.mcu_manager,
                                                   settings_manager=self.settings_manager,
                                                   results_manager=self.results_manager, )

        self.results_tab_controller = ResultsTabController(page=self.results_tab_page,
                                                           settings_manager=self.settings_manager,
                                                           results_manager=self.results_manager,
                                                           smoothing_manager=self.smoothing_manager, )

        self.tcp_tab_controller = TCPTabController(page=self.tcp_tab_page, settings_manager=self.settings_manager,
                                                   results_manager=self.results_manager, tcp_manager=self.tcp_manager)

        # self.graph_tab_controller = DaqTabController(view=self.graph_tab_view,
        #                                              buffer_manager=self.buffer_manager,
        #                                              data_stream_thread=self.data_stream_thread,
        #                                              analysis_manager=self.analysis_manager,
        #                                              settings_manager=self.settings_manager)

        self.controllers = [self.settings_tab_controller,
                            self.ringdown_tab_controller,
                            self.quality_tab_controller,
                            self.results_tab_controller,
                            self.mcu_tab_controller,
                            self.tcp_tab_controller]

        self.controllers[0].start_update_timer()
        self.tab_widget.currentChanged.connect(self.onTabChange)

    def setup_menubar(self):
        menubar = self.menuBar()

        dataview_menu = menubar.addMenu('DataView')

        # 파일 메뉴에 액션 추가
        new_action = QAction('Run DataView', self)
        new_action.triggered.connect(self.run_dataview_action)
        dataview_menu.addAction(new_action)

    def run_dataview_action(self):
        if self.process_alive is True:
            activate_window()
            return

        login_state = str(1)
        dataview_process = multiprocessing.Process(target=dataview_main, args=login_state)
        dataview_process.start()

        self.process_alive = True
        self.start_process_check_thread(dataview_process)

    def start_process_check_thread(self, dataview_process):
        self.__process_check_thread = threading.Thread(target=self.check_subprocess, args=(dataview_process,))
        self.__process_check_thread.daemon = True
        self.__process_check_thread.start()

    def check_subprocess(self, dataview_process):
        while dataview_process.is_alive():
            time.sleep(1)
        self.process_alive = False

    def onTabChange(self, index):
        page = self.tab_order[index][0]
        for controller in self.controllers:
            if controller.page == page:
                controller.start_update_timer()
            else:
                controller.stop_update_timer()

    def closeEvent(self, event):
        """
        응용 프로그램이 닫힐 때 호출되는 이벤트 핸들러.
        스레드를 안전하게 정리하고 필요한 설정을 저장합니다.
        """
        # 종료 여부를 물어보기
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure you want to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            return

        print("Application closing")
        # tcp server stop
        self.tcp_manager.stop_tcp_server()
        print("TCP server stopped")

        # 데이터 스트림 스레드 정지
        if self.data_stream_thread and self.data_stream_thread.is_alive():
            self.data_stream_thread.stop()
            self.data_stream_thread.join()
        print("Data stream thread stopped")
        # 설정 저장
        self.settings_manager.save_settings()
        print("Settings saved")
        # 분석 스레드 정지
        if self.ringdown_manager.is_alive:
            self.ringdown_manager.stop_analysis()
        print("Analysis thread stopped")
        self.ai_scan_manager.stop_scan()
        self.ao_generator.stop()
        print("DAQ stopped")
        # 보드 해제
        self.board_manager.release_board()
        print("Board released")
        # 필요한 추가 정리 작업이 있다면 여기에 작성
        print("Application closed")
        # 이벤트를 부모 클래스에 전달
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
