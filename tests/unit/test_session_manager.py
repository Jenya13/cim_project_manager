from functools import reduce
import time
import pytest


def test_validate_session_expiresion(init_new_session, init_session_from_file):
    new_session = init_new_session
    old_session = init_session_from_file
    assert new_session.is_session_expired() == False
    assert old_session.is_session_expired() == True


def test_validate_session_dict(init_new_session):
    session = init_new_session
    session_dict = session.to_dict()
    assert type(session_dict) == dict
    assert session_dict.get("project_id") is None
    keys_list = ["inactivityTimeout", "privileges",
                 "refreshInterval", "sessionId",  "creationTime"]
    session_dict_keys = list(session_dict.keys())
    assert len(session_dict_keys) == len(keys_list)
    assert sorted(session_dict_keys) == sorted(keys_list)


def test_validation_session_id(init_session_from_file):
    session = init_session_from_file
    session_id_test = "heJGFtDlk2Ykptfc3aRLF1qzxFbtpJY1r8Pp0zTYE3Y+FDCwXFR73LZgO9kgfJ44/8Ms8iUJ3mWtmHrsq8ej/CBuJ5NSw/bsJUFHylLUzkmQ7gCoNjrnGPjhtHPaaLrfYcJBtZdM78FIf7GRHStvexdZ6ObwaSNNiqZZsEYc8q0xpp+SZGkhy5LZLgQlU86k481iLjkr39zsTvHo4YlyMutz7vFqr+q1y9DSbiJrqKBl4yhex255po95BSh4Cc3Sr/x5OOUzAKl2ynhRGkH5XnsZWOTKJdlsIW/jmHC1yw5+ZD48skNY3W6wtgziDkERJNwXL8hpKhVFfCxCEzxxHw=="
    session_id = session.get_session_id()
    assert type(session_id) is str
    assert session_id == session_id_test
