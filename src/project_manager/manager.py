from .cim_project import CimProject


class ProjectManager():

    def __init__(self):
        self.project = CimProject()

    def init_project(self, project_id: str):
        self.project = CimProject()
        self.project.init_project(project_id)

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
