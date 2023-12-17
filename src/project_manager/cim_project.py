import json
import os
import re
import pandas as pd
from datetime import datetime
from typing import List
from api.cim_api import CimplicityApi
from tools.configs_editor import read_config
from .cim_class import CimClass
from .cim_object import CimObject
from .session_manager import SessionManager


class CimProject:

    def __init__(self):
        self.api = CimplicityApi()
        self.project_id: str = ""
        self.session_manager: SessionManager = None
        self.cim_classes: List[CimClass] = []
        self.cim_objects: List[CimObject] = []

    def get_project_name(self) -> str:
        return self.project_id

    def init_project(self, project_id: str):
        # settting new project in to projects folder
        projects_dir = read_config("USER", "projects_dir")
        projects = [project_id for project_id in os.listdir(
            projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]

        self.session_manager = SessionManager(project_id)
        session = self.session_manager.to_dict()
        if session:
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

                project_classes = self._get_classes(project_id, session)

                object_id = "*_TEST"
                params = {"projectId": project_id, "ObjectID": object_id}
                project_objects = self._get_objects(
                    project_id, session, params)

                classes_list = []
                for cls in project_classes:
                    classes_list.append(cls.to_dict())

                object_list = []
                for obj in project_objects:
                    object_list.append(obj.to_dict())

                project_dict = {
                    "id": project_id,
                    "session": session,
                    "classes": classes_list,
                    "objects": object_list
                }
                json_object = json.dumps(project_dict, indent=4)

                json_file = os.path.join(
                    project_dir, f"settings\\{project_id}.json")

                # Writing to json file
                with open(json_file, "w") as outfile:
                    outfile.write(json_object)

                # Template file creation
                template_list = self.create_template_data(
                    classes_list, object_list)
                current_time = datetime.now()
                current_time_str = current_time.strftime("%Y-%m-%d_%H-%M")
                template_file_path = os.path.join(
                    project_dir, f"templates\\{project_id}-{current_time_str}.xlsx")
                # Create an Excel writer
                with pd.ExcelWriter(template_file_path, engine='xlsxwriter') as writer:
                    for data_dict in template_list:
                        sheet_name = data_dict.get("class")
                        df = data_dict.get("data_items")
                        # Write each DataFrame to a separate sheet
                        df.to_excel(writer, sheet_name=sheet_name, index=False)

                print(f"Project {project_id} successfully initialized")
                self.project_id = project_id
        else:
            if project_id in projects:
                print(
                    f"Project: {project_id} exist in file system but doesn't exist in cimplicity")
            else:
                print(
                    f"Project: {project_id} doesn't exist in file system nor in cimplicity")

    def _get_classes(self, project_id, session):
        self.cim_classes = []
        classes = self.api.get_project_classes(
            project_id, session.get("sessionId"))
        for cls in classes:
            self.cim_classes.append(CimClass(cls.get("classId"), cls.get("classVersion"), cls.get(
                "dataItems"), cls.get("description"), cls.get("compositeMembers")))
        return self.cim_classes.copy()

    def _get_objects(self, project_id, session, params):
        self.cim_objects = []
        objects = self.api.get_project_objects(
            project_id, session.get("sessionId"), params=params)
        for obj in objects["Objects"]:
            self.cim_objects.append(CimObject(obj.get("Attributes"), obj.get(
                "ClassID"), obj.get("Description"), obj.get("ID"), obj.get("Routing")))
        return self.cim_objects.copy()

    def create_template_data(self, classes: dict, objects: dict) -> list[dict]:
        """ """
        template_list = []
        for obj in objects:
            class_id = obj.get("ClassID")

            for cls in classes:
                if class_id == cls.get("classId"):
                    obj_data_items = []

                    for dt in obj.get("Attributes"):
                        obj_data_items.append(dt.get("ID"))
                    obj_data_items.append("$Description")

                    for dt in cls.get("dataItems"):
                        result = self._extract_substring(dt.get("description"))
                        if result is not None and result in obj_data_items:
                            index = obj_data_items.index(result)
                            obj_data_items[index] = dt.get("dataItemId")
                    df = pd.DataFrame(columns=sorted(obj_data_items))
                    cls_data = {"class": class_id,
                                "data_items": df}
                    template_list.append(cls_data)

        return template_list

    def _extract_substring(self, input_str: str) -> str:
        # Define the regular expression pattern
        pattern = r'#\[(.*?)\]'

        # Use re.findall to find all matches of the pattern
        matches = re.findall(pattern, input_str)

        # If matches are found, return the first match
        if matches:
            return matches[0]
        else:
            return None

    def set_project(self, project_id: str):
        projects_dir = read_config("USER", "projects_dir")
        projects = [project_id for project_id in os.listdir(
            projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]
        if project_id not in projects:
            return
        # setting object data from json
        project_dir = os.path.join(projects_dir, project_id)
        json_file = os.path.join(
            project_dir, f"settings\\{project_id}.json")
        try:
            # Opening JSON file
            f = open(json_file, "r")

            # returns JSON object as a dictionary
            project_data = json.load(f)
            self.project_id = project_id
            self.session_manager = SessionManager(
                self.project_id, project_data.get("session"))

            classes = project_data.get("classes")
            for cls in classes:
                self.cim_classes.append(CimClass(cls.get("classId"), cls.get("classVersion"), cls.get(
                    "dataItems"), cls.get("description"), cls.get("compositeMembers")))

            objects = project_data.get("objects")
            for obj in objects:
                self.cim_objects.append(CimObject(obj.get("Attributes"), obj.get(
                    "ClassID"), obj.get("Description"), obj.get("ID"), obj.get("Routing")))

        except Exception as error:
            return print(f"Something went wrong when opening the file {project_id}.json")

        return self
