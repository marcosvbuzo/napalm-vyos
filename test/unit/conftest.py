"""Test fixtures."""
from builtins import super

import pytest
from napalm.base.test import conftest as parent_conftest

from napalm.base.test.double import BaseTestDouble

from napalm_vyos import vyos


@pytest.fixture(scope='class')
def set_device_parameters(request):
    """Set up the class."""
    def fin():
        request.cls.device.close()
    request.addfinalizer(fin)

    request.cls.driver = vyos.VyOSDriver
    request.cls.patched_driver = PatchedVyOSDriver
    request.cls.vendor = 'vyos'
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedVyOSDriver(vyos.VyOSDriver):
    """Patched VyOS Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        super().__init__(hostname, username, password, timeout, optional_args)

        self.patched_attrs = ['device']
        self.device = FakeVyOSDevice()

    def close(self):
        pass

    def is_alive(self):
        return {
            'is_alive': True  # In testing everything works..
        }

    def open(self):
        pass


class FakeVyOSDevice(BaseTestDouble):
    """VyOS device test double."""

    def __init__(self):
        self.mode_config = False

    def send_command(self, command, **kwargs):
        filename = '{}.text'.format(self.sanitize_text(command))
        full_path = self.find_file(filename)
        return self.read_txt_file(full_path)

    def config_mode(self):
        self.mode_config = True

    def exit_config_mode(self):
        self.mode_config = False
