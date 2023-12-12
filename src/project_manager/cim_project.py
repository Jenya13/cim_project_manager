import json
import os
from typing import List
from api.cim_api import CimplicityApi
from tools.configs_editor import read_config
from .cim_class import CimClass
from .cim_object import CimObject


class CimProject:

    def __init__(self):
        self.api = CimplicityApi()
        self.project_id: str = ""
        self.cim_classes: List[CimClass] = []
        self.cim_objects: List[CimObject] = []

    def init_project(self, project_id: str):
        # settting new project in to projects folder

        projects_dir = read_config("USER", "projects_dir")
        projects = [project_id for project_id in os.listdir(
            projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]
        # try to get session id for the spesific project
        session_id = self.api.get_sessionId(project_id)
        if session_id is not None:
            # check if the project exist in projects folder, if not, set folders for new project
            if project_id in projects:
                print(f"Project: {project_id} already exist")
                self.project_id = project_id
            else:
                try:
                    project_dir = os.path.join(projects_dir, project_id)
                    os.mkdir(project_dir)
                    os.mkdir(os.path.join(project_dir, "settings"))
                    os.mkdir(os.path.join(project_dir, "templates"))
                except OSError as error:
                    print(error)

                project_classes = self._get_classes(project_id, session_id)

                object_id = "*_TEST"  # "projectId": project_id,
                params = {"projectId": project_id, "ObjectID": object_id}
                project_objects = self._get_objects(
                    project_id, session_id, params)

                classes_list = []
                for cls in project_classes:
                    classes_list.append(cls.to_dict())

                object_list = []
                for obj in project_objects:
                    object_list.append(obj.to_dict())

                project_dict = {
                    "id": project_id,
                    "session": session_id,
                    "classes": classes_list,
                    "objects": object_list
                }
                json_object = json.dumps(project_dict, indent=4)

                json_file = os.path.join(
                    project_dir, f"settings\\{project_id}.json")
                # Writing to json file
                with open(json_file, "w") as outfile:
                    outfile.write(json_object)
                print(f"Project {project_id} successfully initialized")
                self.project_id = project_id
                return project_classes
        else:
            if project_id in projects:
                print(
                    f"Project: {project_id} exist in file system but doesn't exist in cimplicity")
            else:
                print(
                    f"Project: {project_id} doesn't exist in file system nor in cimplicity")

    def _get_classes(self, project_id, session_id):
        self.cim_classes = []
        classes = self.api.get_project_classes(
            project_id, session_id["sessionId"])
        for cls in classes:
            self.cim_classes.append(CimClass(cls.get("classId"), cls.get("classVersion"), cls.get(
                "dataItems"), cls.get("description"), cls.get("compositeMembers")))
        return self.cim_classes.copy()

    def _get_objects(self, project_id, session_id, params):
        self.cim_objects = []
        objects = self.api.get_project_objects(
            project_id, session_id["sessionId"], params=params)
        for obj in objects["Objects"]:
            self.cim_objects.append(CimObject(obj.get("Attributes"), obj.get(
                "ClassID"), obj.get("Description"), obj.get("ID"), obj.get("Routing")))
        return self.cim_objects.copy()
