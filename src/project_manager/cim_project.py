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
        self._project_id: str = ""
        self._session_manager: SessionManager = None
        self._cim_classes: List[CimClass] = []
        self._cim_objects: List[CimObject] = []

    @property
    def project_id(self) -> str:
        project_id = self._project_id[:]
        return project_id

    @property
    def session_manager(self):
        return self._session_manager

    @property
    def cim_classes(self):
        return self._cim_classes

    @property
    def cim_objects(self):
        return self._cim_objects

    def init_project(self, project_id: str):
        # settting new project in to projects folder
        projects_dir = read_config("USER", "projects_dir")
        projects = [project_id for project_id in os.listdir(
            projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]

        self._session_manager = SessionManager(project_id)
        session = self._session_manager.to_dict()
        if session:
            # check if the project exist in projects folder, if not, set folders for new project
            if project_id in projects:
                print(f"Project: {project_id} already exist")
                self._project_id = project_id
            else:
                try:
                    project_dir = os.path.join(projects_dir, project_id)
                    os.mkdir(project_dir)
                    os.mkdir(os.path.join(project_dir, "settings"))
                    os.mkdir(os.path.join(project_dir, "templates"))
                except OSError as error:
                    print(error)
                    return

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

                # Template list creation
                template_list = self.create_template_list(
                    classes_list, object_list)

                # Template file creation
                self.create_template_file(
                    project_id, project_dir, template_list)

                print(f"Project {project_id} successfully initialized")
                self._project_id = project_id
        else:
            if project_id in projects:
                print(
                    f"Project: {project_id} exist in file system but doesn't exist in cimplicity")
            else:
                print(
                    f"Project: {project_id} doesn't exist in file system nor in cimplicity")

    def _get_classes(self, project_id, session):
        self._cim_classes = []
        classes = self.api.get_project_classes(
            project_id, session.get("sessionId"))
        for cls in classes:
            self._cim_classes.append(CimClass(cls.get("classId"), cls.get("classVersion"), cls.get(
                "dataItems"), cls.get("description"), cls.get("compositeMembers")))
        return self._cim_classes.copy()

    def _get_objects(self, project_id, session, params):
        self._cim_objects = []
        objects = self.api.get_project_objects(
            project_id, session.get("sessionId"), params=params)
        for obj in objects["Objects"]:
            self._cim_objects.append(CimObject(obj.get("Attributes"), obj.get(
                "ClassID"), obj.get("Description"), obj.get("ID"), obj.get("Routing")))
        return self._cim_objects.copy()

    def create_template_list(self, classes: dict, objects: dict) -> list[dict]:
        """ """

        def custom_sort(item):
            if item == "ID":
                return (0, item)
            else:
                return (1, item)

        template_list = []
        for obj in objects:
            class_id = obj.get("ClassID")

            for cls in classes:
                if class_id == cls.get("classId"):
                    obj_data_items = []

                    for dt in obj.get("Attributes"):
                        obj_data_items.append(dt.get("ID"))
                    obj_data_items.append("$Description")
                    obj_data_items.append("ID")

                    for dt in cls.get("dataItems"):
                        result = self._extract_substring(dt.get("description"))
                        if result is not None and result in obj_data_items:
                            index = obj_data_items.index(result)
                            obj_data_items[index] = dt.get("dataItemId")
                    obj_data_items = sorted(obj_data_items)
                    obj_data_items = sorted(obj_data_items, key=custom_sort)
                    df = pd.DataFrame(columns=obj_data_items)
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
            self._project_id = project_id
            self._session_manager = SessionManager(
                self._project_id, project_data.get("session"))

            classes = project_data.get("classes")
            for cls in classes:
                self._cim_classes.append(CimClass(cls.get("classId"), cls.get("classVersion"), cls.get(
                    "dataItems"), cls.get("description"), cls.get("compositeMembers")))

            objects = project_data.get("objects")
            for obj in objects:
                self._cim_objects.append(CimObject(obj.get("Attributes"), obj.get(
                    "ClassID"), obj.get("Description"), obj.get("ID"), obj.get("Routing")))
            f.close()
        except Exception as error:
            return print(f"Something went wrong when opening the file {project_id}.json")

        return self

    def create_objects(self, objects_file: str = None):
        if objects_file is not None:
            pass

    def update_template(self):
        if self._project_id != "":
            if self._session_manager.is_session_expired():
                self._session_manager.get_new_session()
            project_classes = self._get_classes(
                self._project_id, self._session_manager.to_dict())

            object_id = "*_TEST"
            params = {"projectId": self._project_id, "ObjectID": object_id}
            project_objects = self._get_objects(
                self._project_id, self._session_manager.to_dict(), params)

            classes_list = []
            for cls in project_classes:
                classes_list.append(cls.to_dict())

            object_list = []
            for obj in project_objects:
                object_list.append(obj.to_dict())

            projects_dir = read_config("USER", "projects_dir")
            project_dir = os.path.join(projects_dir, self._project_id)
            json_file = os.path.join(
                project_dir, f"settings\\{self._project_id}.json")

            update_dict = {
                "classes": classes_list,
                "objects": object_list
            }
            self.update_json_file(json_file, update_dict)

            # Template file creation
            template_list = self.create_template_list(
                classes_list, object_list)

            self.create_template_file(
                self._project_id, project_dir, template_list)

        else:
            print("Project not set, Try to set project befor update template")

    def create_template_file(self, project_id: str, project_dir: str, template_list: list):

        current_time = datetime.now()
        current_time_str = current_time.strftime("%d-%m-%Y_%H-%M")
        template_file_path = os.path.join(
            project_dir, f"templates\\{project_id}_{current_time_str}.xlsx")

        # Create an Excel writer
        with pd.ExcelWriter(template_file_path, engine='xlsxwriter') as writer:

            for data_dict in template_list:
                sheet_name = data_dict.get("class")
                df = data_dict.get("data_items")
                # Write each DataFrame to a separate sheet
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def update_json_file(self, file_path, updates):
        try:
            # Read the existing JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Update the relevant attributes
            data.update(updates)

            # Write the updated data back to the JSON file
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)

            print(f'Changes successfully written to {file_path}')

        except IOError as e:
            print(f'Error: Unable to update {file_path}. {e}')
