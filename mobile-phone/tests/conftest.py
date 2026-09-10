import os

import pytest

if os.path.exists('solution.py'):
    from solution import MobilePhone
else:
    from main import MobilePhone  # type:ignore


# ==============================================================================
# FIXTURES
# ==============================================================================


@pytest.fixture
def phone():
    return MobilePhone('Huawei', 5.3, 8)
