import pytest
import shutil
import os
from project_manager.session_manager import SessionManager
from project_manager.cim_project import CimProject
from project_manager.cim_class import CimClass
from project_manager.cim_object import CimObject
from tools.configs_editor import read_config
from api.cim_api import CimplicityApi
from tests.settings.configs import project_name


@pytest.fixture(scope="module")
def init_project():
    project = CimProject()
    project.init_project(project_name)
    yield project
    projects_dir = read_config("USER", "projects_dir")
    project_dir = os.path.join(projects_dir, project_name)
    shutil.rmtree(project_dir)


@pytest.fixture(scope="module")
def init_cim_api():
    api = CimplicityApi()
    return api


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


@pytest.fixture(scope="module")
def init_cim_class():
    cls = {
        "classId": "ANALOG",
        "classVersion": 10,
        "dataItems": [
            {
                "dataItemId": "SP",
                "dataType": "REAL",
                "description": "{$DESCRIPTION} - Setpoint Value #[SP_EX]"
            },
            {
                "dataItemId": "PV",
                "dataType": "REAL",
                "description": "{$DESCRIPTION} - Present Value #[PV_EX]"
            }
        ],
        "description": "Analog",
        "compositeMembers": None
    }
    cim_class = CimClass(cls.get("classId"), cls.get("classVersion"), cls.get(
        "dataItems"), cls.get("description"), cls.get("compositeMembers"))

    return cim_class


@pytest.fixture(scope="module")
def init_cim_object():
    obj = {
        "Attributes": [
            {
                "ID": "OPC_CHANNEL",
                "Value": "OPC"
            },
            {
                "ID": "$DEVICE_ID",
                "Value": "PANEL_MAIN"
            },
            {
                "ID": "CAPTION",
                "Value": "Analog"
            },
            {
                "ID": "$SCREEN_ID",
                "Value": "Analog"
            },
            {
                "ID": "$RESOURCE_ID",
                "Value": "$SYSTEM"
            },
            {
                "ID": "SP_EX",
                "Value": "1"
            },
            {
                "ID": "OPC_DEVICE",
                "Value": "OPC"
            },
            {
                "ID": "COMMENT",
                "Value": "Analog"
            }
        ],
        "ClassID": "ANALOG",
        "Description": "Analog test",
        "ID": "ANALOG_TEST",
        "Routing": []
    }

    cim_object = CimObject(obj.get("Attributes"), obj.get(
        "ClassID"), obj.get("Description"), obj.get("ID"), obj.get("Routing"))

    return cim_object
