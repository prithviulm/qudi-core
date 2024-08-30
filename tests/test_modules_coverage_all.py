# -*- coding: utf-8 -*-

"""
This file contains unit tests for all qudi fit routines for exponential decay models.

Copyright (c) 2021, the qudi developers. See the AUTHORS.md file at the top-level directory of this
distribution and on <https://github.com/Ulm-IQO/qudi-core/>

This file is part of qudi.

Qudi is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Qudi is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with qudi.
If not, see <https://www.gnu.org/licenses/>.
"""

import coverage
import os
import time

    
def test_coverage_combined(qt_app, module_manager, config, teardown_modules):
    """THis test starts every GUI module and saves one coverage report 
    Parameters
    ----------
    qt_app : fixture
        fixture for qt application
    module_manager : fixture
        fixture for loaded module manager
    config : fixture
        fixture for loaded configuration
    teardown_modules : fixture
        fixture for tearing down modules at the end
    """      
    for base in ['gui', 'logic', 'hardware']:
        for module_name, module_cfg in list(config[base].items()):
            module_manager.add_module(module_name, base, module_cfg, allow_overwrite=False, emit_change=True )
    cov = coverage.Coverage()
    cov.start()
    gui_base = 'gui'
    for module_name, _ in list(config[gui_base].items()):
        module_manager.activate_module(module_name)
        assert module_manager.modules[module_name].is_active            
    time.sleep(15)

    cov.stop()
    test_dir =  os.path.join('coverage',"coverage_all_qudi_iqo_modules")
    os.makedirs(test_dir, exist_ok=True)
    
    cov.html_report(directory=test_dir)
    cov.save()

    print(f"Coverage report saved to {test_dir}")


