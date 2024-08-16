import pytest
import rpyc
import multiprocessing
from qudi.core import application
from PySide2 import QtWidgets
from PySide2.QtCore import QTimer
import os
import time
CONFIG = os.path.join(os.getcwd(),'tests/test.cfg')

def run_qudi():
    app_cls = QtWidgets.QApplication
    app = app_cls.instance()
    if app is None:
        app = app_cls()
    qudi_instance = application.Qudi.instance()
    if qudi_instance is None:
        qudi_instance = application.Qudi(config_file=CONFIG)
    QTimer.singleShot(30000, qudi_instance.quit)
    qudi_instance.run()

def run_module():
    conn = rpyc.connect("localhost", 18861)
    root = conn.root
    module_manager = root._qudi.module_manager
    odmr_gui = 'odmr_gui'
    odmr_logic = 'odmr_logic'
    module_manager.activate_module(odmr_gui)
    logic_instance = module_manager._modules[odmr_logic].instance
    logic_instance.runtime = -5
    logic_instance.start_odmr_scan()
    time.sleep(10)
    module_manager.deactivate_module(odmr_logic)

    module_manager.clear_module_app_data(odmr_logic)
    module_manager.reload_module(odmr_logic)
    module_manager.activate_module(odmr_logic)

    module_manager.activate_module(odmr_gui)


def test_module(qtbot):
    qt_bot = qtbot
    processes = []
    qudi_main_process  = multiprocessing.Process(target=run_qudi)
    module_process  = multiprocessing.Process(target=run_module)
    processes.append(qudi_main_process)
    processes.append(module_process)
    for proc in processes:
        proc.start()
        time.sleep(5)
    for proc in processes:
        proc.join()



