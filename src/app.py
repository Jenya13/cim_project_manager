import os
from pathlib import Path
from tools.configs_editor import read_config, write_config
from project_manager.manager import ProjectManager
import json

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
    manager = ProjectManager()
    classes = manager.init_project("TG1")

    # project_dict = {
    #     "id": "sss",
    #     "session": "sss",
    #     "cim_classes": classes,
    #     "cim_objects": "obj"
    # }
    # json_object = json.dumps(project_dict, indent=4)

    # json_file = os.path.join(
    #     "C:\\Users\\evgenyb\\Documents\\cim_data_manager\\projects", f"test.json")
    # # Writing to json file
    # with open(json_file, "w") as outfile:
    #     outfile.write(json_object)
