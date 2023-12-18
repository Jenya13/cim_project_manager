import pytest
from tools.configs_editor import read_config


@pytest.mark.api
def test_validation_make_post_request(init_cim_api):
    cim_api = init_cim_api

    url = f"TG/session"
    username = read_config("CIM", "user")
    password = read_config("CIM", "password")

    ok, res = cim_api.make_request(
        url, verb="post", auth=(username, password))

    assert ok == True
    assert isinstance(res, dict)


@pytest.mark.api
def test_validation_make_get_request(init_cim_api, init_new_session):
    cim_api = init_cim_api
    session = init_new_session
    session_id = session.get_session_id()
    headers = dict(Authorization=f"Basic {session_id}")
    ok, res = cim_api.make_request("TG", headers=headers)
    assert ok == True
    assert isinstance(res, dict)


@pytest.mark.api
def test_validation_session_creation(init_cim_api):
    cim_api = init_cim_api
    session = cim_api.get_sessionId("TG")
    assert session is not None
    assert isinstance(session, dict)
    session_dict_keys = list(session.keys())
    keys_list = ["inactivityTimeout", "privileges",
                 "refreshInterval", "sessionId"]
    assert len(session_dict_keys) == len(keys_list)
    assert sorted(session_dict_keys) == sorted(keys_list)


@pytest.mark.api
def test_validation_session_not_created(init_cim_api):
    cim_api = init_cim_api
    session = cim_api.get_sessionId("TG5")
    assert session is not None
    assert isinstance(session, str)
    assert session == 'Project with ID "TG5" was not found.'
