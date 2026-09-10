import os

import pytest

if os.path.exists('solution.py'):
    from solution import MobilePhone
else:
    from main import MobilePhone  # type:ignore


def test_mobile_is_built(phone: MobilePhone):
    assert isinstance(phone, MobilePhone)
    assert phone.manufacturer == 'Huawei'
    assert phone.screen_size == 5.3
    assert phone.num_cores == 8
    assert not phone.status
    assert len(phone.apps) == 0


def test_mobile_is_switched_on(phone: MobilePhone):
    phone.power_on()
    assert phone.status


def test_mobile_is_switched_off(phone: MobilePhone):
    phone.power_off()
    assert not phone.status


def test_app_is_installed(phone: MobilePhone):
    phone.install_app('Twitter')
    assert 'Twitter' in phone.apps


def test_app_is_not_installed_when_exists(phone: MobilePhone):
    phone.install_app('Twitter')
    phone.install_app('Twitter')
    assert phone.apps.count('Twitter') == 1


def test_app_is_uninstalled(phone: MobilePhone):
    phone.install_app('Twitter')
    phone.uninstall_app('Twitter')
    assert 'Twitter' not in phone.apps


def test_app_is_not_uninstalled_when_not_exists(phone: MobilePhone):
    phone.uninstall_app('Twitter')
    assert 'Twitter' not in phone.apps


@pytest.mark.parametrize(
    'apps',
    [
        ('Twitter', 'Instagram', 'TikTok'),
        ('Facebook', 'WhatsApp'),
    ],
)
def test_multiple_apps_are_installed(phone: MobilePhone, apps: tuple[str]):
    phone.install_app(*apps)
    assert all(app in phone.apps for app in apps)


@pytest.mark.parametrize(
    'apps',
    [
        ('Twitter', 'Instagram', 'TikTok'),
        ('Facebook', 'WhatsApp'),
    ],
)
def test_multiple_apps_are_uninstalled(phone: MobilePhone, apps: tuple[str]):
    phone.install_app(*apps)
    phone.uninstall_app(*apps)
    assert all(app not in phone.apps for app in apps)
