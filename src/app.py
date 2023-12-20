import os
import json
from pathlib import Path
from tools.configs_editor import read_config, write_config
from project_manager.manager import ProjectManager
from project_manager.session_manager import SessionManager
from project_manager.cim_project import CimProject
from api.cim_api import CimplicityApi


if __name__ == "__main__":

    ########################################### App initialization ###########################################
    # App settings
    if read_config("USER", "WORK_DIR") is None:
        documents_path = Path.home() / "Documents"
        work_dir = documents_path.joinpath(
            read_config("DEFAULT", "work_folder"))
        projects_dir = work_dir.joinpath(
            read_config("DEFAULT", "projects_folder"))
        work_dir = str(work_dir)
        projects_dir = str(projects_dir)
        write_config("USER", "work_dir", work_dir)
        write_config("USER", "projects_dir", projects_dir)
        os.mkdir(read_config("USER", "work_dir"))
        os.mkdir(read_config("USER", "projects_dir"))

    ########################################### App commands ###########################################
    # manager = ProjectManager()
    # manager.init_project("TG1")
###############################################################################
    # manager = ProjectManager()
    # manager.set_project("TG1")
    # manager.create_objects()
    # proj = CimProject()
    # proj.create_objects("TG1")
###############################################################################
    # manager = ProjectManager()
    # manager.set_project("TG")
    # manager.update_template()

    # manager.get_current_project_name()
    # print(manager.get_projects_names())

    # obj_dict = {
    #     "ObjectsInstances": [{
    #         "ID": "ANALOG_TEST_04",
    #         "ClassID": "ANALOG",
    #         "Description": "Analog test 2",
    #         "Attributes": [
    #             {
    #                 "ID": "OPC_CHANNEL",
    #                 "Value": "OPC"
    #             },
    #             {
    #                 "ID": "$DEVICE_ID",
    #                 "Value": "PANEL_MAIN"
    #             },
    #             {
    #                 "ID": "CAPTION",
    #                 "Value": "Analog"
    #             },
    #             {
    #                 "ID": "$SCREEN_ID",
    #                 "Value": "Analog"
    #             },
    #             {
    #                 "ID": "$RESOURCE_ID",
    #                 "Value": "$SYSTEM"
    #             },
    #             {
    #                 "ID": "SP_EX",
    #                 "Value": "1"
    #             },
    #             {
    #                 "ID": "OPC_DEVICE",
    #                 "Value": "OPC"
    #             },
    #             {
    #                 "ID": "COMMENT",
    #                 "Value": "Analog2"
    #             }
    #         ], "Routing": []
    #     }
    #     ]
    # }

    # api = CimplicityApi()
    # session = api.get_sessionId("TG1")

    # session_id = session.get("sessionId")
    # res = api.create_objects("TG1", session_id, obj_dict)
    # print(res)

    # headers = dict(Authorization=f"Basic {session_id}")
    # ok, res = api.make_request("TG5", headers=headers)
    # print(res.get("title"))
