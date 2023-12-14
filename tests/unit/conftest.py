import pytest
from project_manager.session_manager import SessionManager
# from src.api.cim_api import CimplicityApi


@pytest.fixture(scope="module")
def init_new_session():
    session_manager = SessionManager("TG")
    return session_manager


@pytest.fixture(scope="module")
def init_session_from_file():
    session_dict = {
        "inactivityTimeout": 1200000,
        "privileges": -1,
        "refreshInterval": 900000,
        "creationTime": 1702559000340.0522,
        "sessionId": "heJGFtDlk2Ykptfc3aRLF1qzxFbtpJY1r8Pp0zTYE3Y+FDCwXFR73LZgO9kgfJ44/8Ms8iUJ3mWtmHrsq8ej/CBuJ5NSw/bsJUFHylLUzkmQ7gCoNjrnGPjhtHPaaLrfYcJBtZdM78FIf7GRHStvexdZ6ObwaSNNiqZZsEYc8q0xpp+SZGkhy5LZLgQlU86k481iLjkr39zsTvHo4YlyMutz7vFqr+q1y9DSbiJrqKBl4yhex255po95BSh4Cc3Sr/x5OOUzAKl2ynhRGkH5XnsZWOTKJdlsIW/jmHC1yw5+ZD48skNY3W6wtgziDkERJNwXL8hpKhVFfCxCEzxxHw=="
    }
    session_manager = SessionManager("TG", session_dict)
    return session_manager
