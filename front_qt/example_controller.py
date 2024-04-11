import time
import traceback

from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget
from serial.tools import list_ports
import pyqtgraph as pg

from front.mcu_tab_view import Ui_Form
from front.utils.TimeAxis.TimeAxisItem import TimeAxisItem
from mcu.ReadCommandEnums import ReadPacketEnums
from mcu.laser_utils import convert_volt_to_temperature, convert_tempvolt_readrange_to_setrange
from mcu.mcu_manager import MCUManager
from results.results_manager import ResultsManager
from settings.settings_manager import SettingsManager


class McuTabController(QObject):
    def __init__(self, page: QWidget,
                 settings_manager: SettingsManager,
                 mcu_manager: MCUManager,
                 results_manager: ResultsManager,
                 update_interval=1000):
        super().__init__()

        self.laser_1_history_plot = None
        self.laser_2_history_plot = None
        self.laser_3_history_plot = None
        self.das_temperature_history_plot = None
        self.temperature_history_plot_1 = None
        self.temperature_history_plot_0 = None
        self.pressure_history_plot = None
        self._block_signals = False  # 신호 블록을 관리하기 위한 플래그 추가

        self.update_timer = None
        self.update_interval = update_interval
        self.settings_manager = settings_manager
        self.mcu_manager = mcu_manager
        self.results_manager = results_manager

        self.page = page
        self.ui = Ui_Form()
        self.ui.setupUi(page)

        self.initialize_ui()
        self.initialize_values()
        self.initialize_update_timer()

        # Connect signals to slots
        self.ui.connect_button.clicked.connect(self.connect_serial)

        self.ui.pressure_params_apply_button.clicked.connect(self._apply_pressure_parameters)
        self.ui.cell_box_params_apply_button.clicked.connect(self._apply_cell_box_parameters)
        self.ui.das_box_params_apply_button.clicked.connect(self._apply_das_box_parameters)

        self.ui.laser_temperature_celcius_input_1.valueChanged.connect(
            lambda: self._convert_temperature_celcius_to_volt(self.ui.laser_temperature_celcius_input_1,
                                                              self.ui.laser_temperature_volt_input_1))
        self.ui.laser_temperature_celcius_input_2.valueChanged.connect(
            lambda: self._convert_temperature_celcius_to_volt(self.ui.laser_temperature_celcius_input_2,
                                                              self.ui.laser_temperature_volt_input_2))
        self.ui.laser_temperature_celcius_input_3.valueChanged.connect(
            lambda: self._convert_temperature_celcius_to_volt(self.ui.laser_temperature_celcius_input_3,
                                                              self.ui.laser_temperature_volt_input_3))
        self.ui.laser_temperature_volt_input_1.valueChanged.connect(
            lambda: self._convert_volt_to_temperature_celcius(self.ui.laser_temperature_volt_input_1,
                                                              self.ui.laser_temperature_celcius_input_1))
        self.ui.laser_temperature_volt_input_2.valueChanged.connect(
            lambda: self._convert_volt_to_temperature_celcius(self.ui.laser_temperature_volt_input_2,
                                                              self.ui.laser_temperature_celcius_input_2))
        self.ui.laser_temperature_volt_input_3.valueChanged.connect(
            lambda: self._convert_volt_to_temperature_celcius(self.ui.laser_temperature_volt_input_3,
                                                              self.ui.laser_temperature_celcius_input_3))

        self.ui.laser_control_apply_button_1.clicked.connect(self._apply_laser_1_parameters)
        self.ui.laser_control_apply_button_2.clicked.connect(self._apply_laser_2_parameters)
        self.ui.laser_control_apply_button_3.clicked.connect(self._apply_laser_3_parameters)

    def initialize_ui(self):
        self.ui.comboBox_baudrate_list.addItem("115200")

        if self.mcu_manager.serial_instance is not None:
            if self.mcu_manager.serial_instance.is_open:
                self.ui.connect_button.setText("Disconnect")
            else:
                self.ui.connect_button.setText("Connect")

        self.ui.pressure_history_graph.setBackground('w')
        self.ui.pressure_history_graph.setTitle("Pressure History")
        self.ui.pressure_history_graph.setAxisItems({'bottom': TimeAxisItem(orientation='bottom')})
        self.ui.pressure_history_graph.showGrid(x=True, y=True)
        self.pressure_history_plot = self.ui.pressure_history_graph.plot(pen=pg.mkPen(color=(0, 0, 255)))

        self.ui.cell_temperature_history_graph.setBackground('w')
        self.ui.cell_temperature_history_graph.setTitle("Cell Temperature History")
        self.ui.cell_temperature_history_graph.setAxisItems({'bottom': TimeAxisItem(orientation='bottom')})
        self.ui.cell_temperature_history_graph.showGrid(x=True, y=True)
        self.temperature_history_plot_0 = self.ui.cell_temperature_history_graph.plot(pen=pg.mkPen(color=(0, 0, 255)))
        self.temperature_history_plot_1 = self.ui.cell_temperature_history_graph.plot(pen=pg.mkPen(color=(0, 255, 0)))

        self.ui.das_temperature_history_graph.setBackground('w')
        self.ui.das_temperature_history_graph.setTitle("DAS Temperature History")
        self.ui.das_temperature_history_graph.setAxisItems({'bottom': TimeAxisItem(orientation='bottom')})
        self.ui.das_temperature_history_graph.showGrid(x=True, y=True)
        self.das_temperature_history_plot = self.ui.das_temperature_history_graph.plot(pen=pg.mkPen(color=(0, 0, 255)))

        self.ui.laser_1_history_graph.setBackground('w')
        self.ui.laser_1_history_graph.setTitle("Laser 1 History")
        self.ui.laser_1_history_graph.setAxisItems({'bottom': TimeAxisItem(orientation='bottom')})
        self.ui.laser_1_history_graph.setLabel('left', '°C')
        self.ui.laser_1_history_graph.showGrid(x=True, y=True)
        self.laser_1_history_plot = self.ui.laser_1_history_graph.plot(pen=pg.mkPen(color=(0, 0, 255)))

        self.ui.laser_2_history_graph.setBackground('w')
        self.ui.laser_2_history_graph.setTitle("Laser 2 History")
        self.ui.laser_2_history_graph.setAxisItems({'bottom': TimeAxisItem(orientation='bottom')})
        self.ui.laser_2_history_graph.setLabel('left', '°C')
        self.ui.laser_2_history_graph.showGrid(x=True, y=True)
        self.laser_2_history_plot = self.ui.laser_2_history_graph.plot(pen=pg.mkPen(color=(0, 255, 0)))

        self.ui.laser_3_history_graph.setBackground('w')
        self.ui.laser_3_history_graph.setTitle("Laser 3 History")
        self.ui.laser_3_history_graph.setAxisItems({'bottom': TimeAxisItem(orientation='bottom')})
        self.ui.laser_3_history_graph.setLabel('left', '°C')
        self.ui.laser_3_history_graph.showGrid(x=True, y=True)
        self.laser_3_history_plot = self.ui.laser_3_history_graph.plot(pen=pg.mkPen(color=(255, 0, 0)))

    def initialize_values(self):
        # 설정 초기값을 설정
        settings = self.settings_manager.get_settings()

        # COM Port list 설정
        self.refresh_comport_list()

        # PID 초기값 설정
        self.ui.pressure_kp_input.setValue(settings.mcu_params.PV_Kp)
        self.ui.pressure_ki_input.setValue(settings.mcu_params.PV_Ki)
        self.ui.pressure_kd_input.setValue(settings.mcu_params.PV_Kd)
        self.ui.pressure_target_input.setValue(settings.mcu_params.PV_setpoint)

        self.ui.celltemp_kp_input.setValue(settings.mcu_params.TEC_Kp)
        self.ui.celltemp_ki_input.setValue(settings.mcu_params.TEC_Ki)
        self.ui.celltemp_kd_input.setValue(settings.mcu_params.TEC_Kd)
        self.ui.celltemp_target_input.setValue(settings.mcu_params.TEC_setpoint)

        self.ui.das_temp_kp_input.setValue(settings.mcu_params.DAS_Kp)
        self.ui.das_temp_ki_input.setValue(settings.mcu_params.DAS_Ki)
        self.ui.das_temp_kd_input.setValue(settings.mcu_params.DAS_Kd)
        self.ui.das_temp_target_input.setValue(settings.mcu_params.DAS_setpoint)

        # 레이저 초기값 설정
        self.ui.laser_temperature_celcius_input_1.setValue(settings.mcu_params.laser_1_celcius_setpoint)
        self.ui.laser_temperature_celcius_input_2.setValue(settings.mcu_params.laser_2_celcius_setpoint)
        self.ui.laser_temperature_celcius_input_3.setValue(settings.mcu_params.laser_3_celcius_setpoint)

        self.ui.laser_temperature_volt_input_1.setValue(settings.mcu_params.laser_1_voltage_setpoint)
        self.ui.laser_temperature_volt_input_2.setValue(settings.mcu_params.laser_2_voltage_setpoint)
        self.ui.laser_temperature_volt_input_3.setValue(settings.mcu_params.laser_3_voltage_setpoint)

    def initialize_update_timer(self):
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_connection_textEdit)
        self.update_timer.timeout.connect(self._update_conditions_tab)
        self.update_timer.timeout.connect(self._update_lasers_tab)

    def start_update_timer(self):
        self.update_timer.start(self.update_interval)

    def stop_update_timer(self):
        self.update_timer.stop()

    def refresh_comport_list(self):
        try:
            self.ui.comboBox_com_lists.clear()
            comport_list = list_ports.comports()
            for comport in comport_list:
                self.ui.comboBox_com_lists.addItem(comport.device)

            if self.mcu_manager.serial_instance.port is not None:
                self.ui.comboBox_com_lists.setCurrentText(self.mcu_manager.serial_instance.port)
        except Exception as e:
            traceback.print_exc()

    def connect_serial(self):
        settings = self.settings_manager.get_settings()
        self.stop_update_timer()  # 반드시 먼저 멈춰야 함
        if self.ui.connect_button.text() == "Connect":
            self.mcu_manager.start_serial_communication(self.ui.comboBox_com_lists.currentText(),
                                                        int(self.ui.comboBox_baudrate_list.currentText()))
            self.ui.connect_button.setText("Disconnect")
            settings.mcu_params.comport = self.ui.comboBox_com_lists.currentText()
            settings.mcu_params.baudrate = int(self.ui.comboBox_baudrate_list.currentText())
            self.settings_manager.save_settings()
            self.start_update_timer()
        else:
            self.mcu_manager.exit()
            self.ui.connect_button.setText("Connect")

    def _update_connection_textEdit(self):
        try:
            received_data = self.results_manager.get_mcu_result()
            if self.mcu_manager.serial_instance.is_open:
                self.ui.connection_textEdit.clear()
                # 쉼표를 줄바꿈으로 교체
                str_data = str(received_data)
                formatted_data = str_data.replace(" ", "\n")
                datetime_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

                self.ui.connection_textEdit.append(datetime_str)
                self.ui.connection_textEdit.append(formatted_data)
        except Exception as e:
            traceback.print_exc()

    def _update_conditions_tab(self):
        try:
            mcu_result = self.results_manager.get_mcu_result()
            if mcu_result is not None:
                self.ui.label_pressure_kp.setText(str(round(mcu_result.PV_fKp, 3)))
                self.ui.label_pressure_ki.setText(str(round(mcu_result.PV_fKi, 3)))
                self.ui.label_pressure_kd.setText(str(mcu_result.PV_fKd))
                self.ui.label_pressure_value.setText(str(round(mcu_result.pressure, 2)))
                self.ui.label_pressure_output.setText(str(mcu_result.PV_nOutput))

                self.ui.label_celltemp_kp.setText(str(round(mcu_result.TEC_fKp, 3)))
                self.ui.label_celltemp_ki.setText(str(round(mcu_result.TEC_fKi, 3)))
                self.ui.label_celltemp_kd.setText(str(round(mcu_result.TEC_fKd, 3)))
                self.ui.label_celltemp_value_0.setText(str(round(mcu_result.temperature0, 5)))
                self.ui.label_celltemp_value_1.setText(str(round(mcu_result.temperature1, 5)))
                self.ui.label_celltemp_output.setText(str(mcu_result.TEC_nOutput))

                self.ui.label_das_temp_kp.setText(str(round(mcu_result.FAN_fKp, 3)))
                self.ui.label_das_temp_ki.setText(str(round(mcu_result.FAN_fKi, 3)))
                self.ui.label_das_temp_kd.setText(str(round(mcu_result.FAN_fKd, 3)))
                self.ui.label_das_temp_value.setText(str(round(mcu_result.temperature2, 5)))
                self.ui.label_das_temp_output.setText(str(mcu_result.FAN_nOutput))
                self.ui.label_das_temp_tach_0.setText(str(mcu_result.F_FAN_SPEED))
                self.ui.label_das_temp_tach_1.setText(str(mcu_result.R_FAN_SPEED))

            self.pressure_history_plot.setData(self.results_manager.results_history.time,
                                               self.results_manager.results_history.pressure)
            self.temperature_history_plot_0.setData(self.results_manager.results_history.time,
                                                    self.results_manager.results_history.cell_temperature0)
            self.temperature_history_plot_1.setData(self.results_manager.results_history.time,
                                                    self.results_manager.results_history.cell_temperature1)
            self.das_temperature_history_plot.setData(self.results_manager.results_history.time,
                                                      self.results_manager.results_history.das_temperature)
        except Exception as e:
            traceback.print_exc()

    def _update_lasers_tab(self):
        try:
            mcu_result = self.results_manager.get_mcu_result()
            if mcu_result is not None:
                lc_temp_volt_raw_1 = mcu_result.LC1_T_ACT_MON
                lc_temp_volt_raw_2 = mcu_result.LC2_T_ACT_MON
                lc_temp_volt_raw_3 = mcu_result.LC3_T_ACT_MON
                lc_temp_volt_converted_range_like_setpoint_1 = convert_tempvolt_readrange_to_setrange(
                    lc_temp_volt_raw_1)
                lc_temp_volt_converted_range_like_setpoint_2 = convert_tempvolt_readrange_to_setrange(
                    lc_temp_volt_raw_2)
                lc_temp_volt_converted_range_like_setpoint_3 = convert_tempvolt_readrange_to_setrange(
                    lc_temp_volt_raw_3)
                lc_temp_celcius_1 = convert_volt_to_temperature(lc_temp_volt_raw_1)
                lc_temp_celcius_2 = convert_volt_to_temperature(lc_temp_volt_raw_2)
                lc_temp_celcius_3 = convert_volt_to_temperature(lc_temp_volt_raw_3)
                self.ui.label_temperature_celcius_1.setText(str(round(lc_temp_celcius_1, 5)))
                self.ui.label_temperature_celcius_2.setText(str(round(lc_temp_celcius_2, 5)))
                self.ui.label_temperature_celcius_3.setText(str(round(lc_temp_celcius_3, 5)))
                self.ui.label_temperature_volt_1.setText(str(round(lc_temp_volt_converted_range_like_setpoint_1, 5)))
                self.ui.label_temperature_volt_2.setText(str(round(lc_temp_volt_converted_range_like_setpoint_2, 5)))
                self.ui.label_temperature_volt_3.setText(str(round(lc_temp_volt_converted_range_like_setpoint_3, 5)))

            self.laser_1_history_plot.setData(self.results_manager.results_history.time,
                                              self.results_manager.results_history.LC1_T_ACT_MON_TEMP)
            self.laser_2_history_plot.setData(self.results_manager.results_history.time,
                                              self.results_manager.results_history.LC2_T_ACT_MON_TEMP)
            self.laser_3_history_plot.setData(self.results_manager.results_history.time,
                                              self.results_manager.results_history.LC3_T_ACT_MON_TEMP)
        except Exception as e:
            traceback.print_exc()

    def _apply_pressure_parameters(self):
        pressure_kp = self.ui.pressure_kp_input.value()
        pressure_ki = self.ui.pressure_ki_input.value()
        pressure_kd = self.ui.pressure_kd_input.value()
        pressure_target = self.ui.pressure_target_input.value()

        settings = self.settings_manager.get_settings()
        settings.mcu_params.PV_Kp = pressure_kp
        settings.mcu_params.PV_Ki = pressure_ki
        settings.mcu_params.PV_Kd = pressure_kd
        settings.mcu_params.PV_setpoint = pressure_target

        self.settings_manager.save_settings()
        self.mcu_manager.send_pressure_command(pressure_target, pressure_kp, pressure_ki, pressure_kd)

    def _apply_cell_box_parameters(self):
        celltemp_kp = self.ui.celltemp_kp_input.value()
        celltemp_ki = self.ui.celltemp_ki_input.value()
        celltemp_kd = self.ui.celltemp_kd_input.value()
        celltemp_target = self.ui.celltemp_target_input.value()

        settings = self.settings_manager.get_settings()
        settings.mcu_params.TEC_Kp = celltemp_kp
        settings.mcu_params.TEC_Ki = celltemp_ki
        settings.mcu_params.TEC_Kd = celltemp_kd
        settings.mcu_params.TEC_setpoint = celltemp_target

        self.settings_manager.save_settings()
        self.mcu_manager.send_tec_command(celltemp_target, celltemp_kp, celltemp_ki, celltemp_kd)

    def _apply_das_box_parameters(self):
        das_temp_kp = self.ui.das_temp_kp_input.value()
        das_temp_ki = self.ui.das_temp_ki_input.value()
        das_temp_kd = self.ui.das_temp_kd_input.value()
        das_temp_target = self.ui.das_temp_target_input.value()

        settings = self.settings_manager.get_settings()
        settings.mcu_params.DAS_Kp = das_temp_kp
        settings.mcu_params.DAS_Ki = das_temp_ki
        settings.mcu_params.DAS_Kd = das_temp_kd
        settings.mcu_params.DAS_setpoint = das_temp_target

        self.settings_manager.save_settings()
        self.mcu_manager.send_das_command(das_temp_target, das_temp_kp, das_temp_ki, das_temp_kd)

    def _apply_laser_1_parameters(self):
        laser_temp_celcius = self.ui.laser_temperature_celcius_input_1.value()
        laser_temp_volt = self.ui.laser_temperature_volt_input_1.value()

        settings = self.settings_manager.get_settings()
        settings.mcu_params.laser_1_celcius_setpoint = laser_temp_celcius
        settings.mcu_params.laser_1_voltage_setpoint = laser_temp_volt

        self.settings_manager.save_settings()
        self.mcu_manager.send_laser_command(1, laser_temp_volt)

    def _apply_laser_2_parameters(self):
        laser_temp_celcius = self.ui.laser_temperature_celcius_input_2.value()
        laser_temp_volt = self.ui.laser_temperature_volt_input_2.value()

        settings = self.settings_manager.get_settings()
        settings.mcu_params.laser_2_celcius_setpoint = laser_temp_celcius
        settings.mcu_params.laser_2_voltage_setpoint = laser_temp_volt

        self.settings_manager.save_settings()
        self.mcu_manager.send_laser_command(2, laser_temp_volt)

    def _apply_laser_3_parameters(self):
        laser_temp_celcius = self.ui.laser_temperature_celcius_input_3.value()
        laser_temp_volt = self.ui.laser_temperature_volt_input_3.value()

        settings = self.settings_manager.get_settings()
        settings.mcu_params.laser_3_celcius_setpoint = laser_temp_celcius
        settings.mcu_params.laser_3_voltage_setpoint = laser_temp_volt

        self.settings_manager.save_settings()
        self.mcu_manager.send_laser_command(3, laser_temp_volt)

    def _convert_temperature_celcius_to_volt(self, input_number, volt_ui):
        if self._block_signals:  # 신호가 블록된 경우 변환을 수행하지 않음
            return
        laser_temp_celcius = input_number.value()
        from mcu.laser_utils import convert_t_set_to_v_set
        laser_temp_volt = convert_t_set_to_v_set(laser_temp_celcius)
        self._block_signals = True  # 신호 블록 활성화
        volt_ui.setValue(laser_temp_volt)
        self._block_signals = False  # 신호 블록 해제

    def _convert_volt_to_temperature_celcius(self, input_number, celcius_ui):
        if self._block_signals:  # 신호가 블록된 경우 변환을 수행하지 않음
            return
        laser_temp_volt = input_number.value()
        from mcu.laser_utils import convert_v_set_to_t_set
        laser_temp_celcius = convert_v_set_to_t_set(laser_temp_volt)
        self._block_signals = True  # 신호 블록 활성화
        celcius_ui.setValue(laser_temp_celcius)
        self._block_signals = False  # 신호 블록 해제

