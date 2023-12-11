import time
import json
import os
from api.cim_api import CimplicityApi
from tools.configs_reader import read_config


class ProjectManager():

    def __init__(self):
        self.api = CimplicityApi()

    def init_project(self, project_id: str):
        # settting new project in to projects folder

        projects_dir = read_config("USER", "projects_dir")
        projects = [project_id for project_id in os.listdir(
            projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]
        # try to get session id for the spesific project
        session_id = self.api.get_sessionId(project_id)
        if session_id is not None:
            # check if the project exist in projects folder, if not set folders for new project
            if project_id in projects:
                print(f"Project: {project_id} already exist")
            else:
                try:
                    project_dir = os.path.join(projects_dir, project_id)
                    os.mkdir(project_dir)
                    os.mkdir(os.path.join(project_dir, "settings"))
                    os.mkdir(os.path.join(project_dir, "templates"))
                except OSError as error:
                    print(error)

                project_classes = self.api.get_project_classes(
                    project_id, session_id["sessionId"])

                # project_objects =

                project_dict = {
                    "id": project_id,
                    "session": session_id,
                    "classes": project_classes

                }
                json_object = json.dumps(project_dict, indent=4)

                json_file = os.path.join(
                    project_dir, f"settings\\{project_id}.json")
                # Writing to json file
                with open(json_file, "w") as outfile:
                    outfile.write(json_object)
                print(f"Project {project_id} successfully initialized")
        else:
            if project_id in projects:
                print(
                    f"Project: {project_id} exist in file system but doesn't exist in cimplicity")
            else:
                print(
                    f"Project: {project_id} doesn't exist in file system nor in cimplicity")

    # def set_project(self, name: str = None):
    #     path = get_settings_path()
    #     projects_data = None
    #     if name is not None:
    #         try:
    #             with open(f'{path}\\projects.json', 'r') as file:
    #                 projects_data = json.load(file)
    #         except (FileNotFoundError, json.decoder.JSONDecodeError):
    #             print("file doesn't exist or is empty")

    #         if name not in projects_data:
    #             projects_data[name] = {}
    #             projects_data[name]["id"] = name
    #             projects_data[name]["auth"] = dict(username=defs.USER,
    #                                                password=defs.PASSWORD)

    #             session = self.api.get_sessionId(projects_data[name])
    #             session["last_activity_time"] = time.time() * 1000

    #             if session is None:
    #                 return None

    #             projects_data[name]["session"] = session

    #             classes = self.api.get_project_classes(projects_data[name])
    #             projects_data[name]["classes"] = {}

    #             for cls in classes:
    #                 cls_id = cls["classId"]
    #                 cls.pop("classId")
    #                 projects_data[name]["classes"][cls_id] = cls

    #             object_id = "*_TEST"
    #             params = {"ObjectID": object_id}
    #             objects = self.api.get_project_objects(
    #                 projects_data[name], params=params)
    #             projects_data[name]["objects"] = objects["Objects"]

    #             with open(f'{path}\\projects.json', 'w') as file:
    #                 json.dump(projects_data, file, indent=4)
    #             # self.project =  projects_data[name]

    #             print(f"project {name} was set")
    #         else:
    #             print(f"project {name} already exist")
    #     else:
    #         return None

    # def get_project(self, name: str = None):
    #     path = get_settings_path()
    #     data = None
    #     if name is not None:
    #         try:
    #             with open(f'{path}\\projects.json', 'r') as file:
    #                 data = json.load(file)

    #         except (FileNotFoundError, json.decoder.JSONDecodeError):
    #             print("file doesn't exist or is empty")

    #         if name in list(data.keys()):
    #             self.project = data[name]
    #             return self.project

    #         else:
    #             return f"No project with name: {name}"

    #     else:
    #         return "No project name provided, please provide project name"

    # def is_session_expired(self, session: dict):

    #     current_time = time.time() * 1000
    #     elapsed_time = current_time - session["last_activity_time"]
    #     return elapsed_time > session["refreshInterval"]

    # if self.is_session_expired(self.project["session"]):

    #                 session = self.api.get_sessionId(self.project[name])
    #                 session["last_activity_time"] = time.time() * 1000
    #                 self.project[name]["session"] = session
