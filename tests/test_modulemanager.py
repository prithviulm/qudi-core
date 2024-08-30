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

from qudi.core import modulemanager
import pytest
import coverage
import os


# @pytest.fixture(autouse=True)
# Uncomment above line to get coverage
def coverage_for_each_test(request):
    """
    Fixture to generate coverage report for each test function.

    Parameters
    ----------
    request : pytest.fixture
        Pytest fixture for request.
    """
    # Start coverage collection
    cov = coverage.Coverage()
    cov.start()
    yield
    # Stop coverage collection
    cov.stop()
    # Create a unique directory for each test function
    test_dir = f"coverage_{request.node.nodeid.replace('/', '_').replace(':', '_')}"
    os.makedirs(test_dir, exist_ok=True)

    cov.html_report(directory=test_dir)
    cov.save()


def test_add_module(module_manager, sample_module_gui, qtbot):
    """
    Test if modules can be added to the module manager.

    Parameters
    ----------
    module_manager : pytest.fixture
        Fixture for instance of module manager.
    sample_module_gui : pytest.fixture
        Fixture for instance of managed module for a sample gui module.
    qtbot : pytest.fixture
        Pytest fixture for qt.
    """
    sample_base, sample_module_name, sample_module_cfg = sample_module_gui
    assert sample_module_name not in module_manager.module_names

    with qtbot.waitSignal(module_manager.sigManagedModulesChanged) as blockers:
        module_manager.add_module(sample_module_name, sample_base, sample_module_cfg, emit_change=True)
    emitted_signal = blockers.args
    assert sample_module_name in emitted_signal[0]

    assert sample_module_name in module_manager.module_names
    assert isinstance(module_manager.modules[sample_module_name], modulemanager.ManagedModule)


def test_remove_module(module_manager, sample_module_gui, qtbot):
    """
    Test if modules can be removed from the module manager.

    Parameters
    ----------
    module_manager : pytest.fixture
        Fixture for instance of module manager.
    sample_module_gui : pytest.fixture
        Fixture for instance of managed module for a sample gui module.
    qtbot : pytest.fixture
        Pytest fixture for qt.
    """
    sample_base, sample_module_name, sample_module_cfg = sample_module_gui
    assert sample_module_name in module_manager.module_names

    with qtbot.waitSignal(module_manager.sigManagedModulesChanged) as blockers:
        module_manager.remove_module(sample_module_name, emit_change=True)
    emitted_signal = blockers.args
    assert sample_module_name not in emitted_signal[0]

    assert sample_module_name not in module_manager.module_names


def test_refresh_module_links(module_manager, sample_module_gui, sample_module_logic):
    """
    Test module link refreshing for both dependent and required modules.

    Parameters
    ----------
    module_manager : pytest.fixture
        Fixture for instance of module manager.
    sample_module_gui : pytest.fixture
        Fixture for instance of managed module for a sample gui module.
    sample_module_logic : pytest.fixture
        Fixture for instance of managed module for a sample logic module.
    """
    sample_gui_base, sample_gui_name, sample_gui_cfg = sample_module_gui
    # Adding a sample gui module
    gui_module = modulemanager.ManagedModule(
        module_manager._qudi_main_ref, sample_gui_name, sample_gui_base, sample_gui_cfg
    )
    module_manager._modules[sample_gui_name] = gui_module

    sample_logic_base, sample_logic_name, sample_logic_cfg = sample_module_logic
    # Adding a sample logic module to check if refresh links works
    logic_module = modulemanager.ManagedModule(
        module_manager._qudi_main_ref, sample_logic_name, sample_logic_base, sample_logic_cfg
    )
    module_manager._modules[sample_logic_name] = logic_module

    module_manager.refresh_module_links()

    # Checking whether links have been refreshed. Logic module should be in required modules list for gui module
    gui_required_modules = [ref() for ref in gui_module.required_modules]
    assert logic_module in gui_required_modules

    # Gui module should be in dependent modules list of logic module
    logic_dependent_modules = [ref() for ref in logic_module.dependent_modules]
    assert gui_module in logic_dependent_modules

    gui_module = module_manager._modules.pop(sample_gui_name, None)
    logic_module = module_manager._modules.pop(sample_logic_name, None)


def test_activate_module(
    module_manager, config, sample_module_hardware, sample_module_logic, sample_module_gui, teardown_modules
):
    """
    Test module activation and deactivation.

    Parameters
    ----------
    module_manager : pytest.fixture
        Fixture for instance of module manager.
    config : pytest.fixture
        Fixture for loaded yaml config.
    sample_module_hardware : pytest.fixture
        Fixture for instance of managed module for a sample hardware module.
    sample_module_gui : pytest.fixture
        Fixture for instance of managed module for a sample gui module.
    sample_module_logic : pytest.fixture
        Fixture for instance of managed module for a sample logic module.
    teardown_modules : pytest.fixture
        Fixture for tearing down modules at the end.
    """
    for base in ['gui', 'logic', 'hardware']:
        for module_name, module_cfg in list(config[base].items()):
            module_manager.add_module(module_name, base, module_cfg, allow_overwrite=False, emit_change=True)
    _, sample_hardware, _ = sample_module_hardware
    _, sample_logic, _ = sample_module_logic
    _, sample_gui, _ = sample_module_gui
    module_manager.activate_module(sample_gui)
    gui_managed_module = module_manager.modules[sample_gui]
    logic_managed_module = module_manager.modules[sample_logic]
    hardware_managed_module = module_manager.modules[sample_hardware]

    assert gui_managed_module.is_active
    assert logic_managed_module.is_active
    assert hardware_managed_module.is_active
