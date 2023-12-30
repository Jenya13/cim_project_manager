import os
import shutil
from .cim_project import CimProject
from tools.configs_editor import read_config


class ProjectManager():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ProjectManager, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.project = CimProject()

    def init_project(self, project_id: str):
        self.project = CimProject()
        status, data = self.project.init_project(project_id)

        if isinstance(data, CimProject) and status is True:
            self.project = data
            print(
                f"Project {self.project.project_id} successfully initialized")
            return
        print(data)

    def set_project(self, project_id: str):
        project = self.project.set_project(project_id)
        if project is None:
            print(f"No project: {project_id} in projects folder")
        else:
            self.project = project
            print(f"Project: {self.project.project_id} is set")

    def get_current_project_name(self):
        if self.is_project_set():
            return self.project.project_id
        return None

    def update_template(self):
        if self.is_project_set():
            ok, res = self.project.update_template()
            print(res)
        print("No project was set or initialized")

    def create_objects(self, update_file: str = None):
        if not self.is_project_set():
            print("No project was set or initialized")
            return None
        else:
            if update_file is not None:
                project_id = self.get_current_project_name()
                if project_id == None:
                    return None
                projects_dir = read_config("USER", "projects_dir")
                project_dir = os.path.join(projects_dir, project_id)
                obj_file = os.path.join(project_dir, f"updates\\{update_file}")

                if os.path.isfile(obj_file):
                    res: dict = self.project.create_objects(obj_file)
                    print("Objects create/update result: ")
                    if res.get("status") == 500:
                        print(f"Error: {res.get('detail')}")
                    else:
                        print(f"Total items: {len(res.get('ItemResults'))}")
                        print(f"Total successes: {res.get('NumSuccesses')}")
                        print(f"Total failures: {res.get('NumFailures')}")

                else:
                    print(f"No file: {update_file} in updates directory ")

            else:
                self.project.create_objects()
                res: dict = self.project.create_objects()
                print("Objects create/update result: ")
                if res.get("status") == 500:
                    print(f"Error: {res.get('detail')}")
                else:
                    print(f"Total items: {len(res.get('ItemResults'))}")
                    print(f"Total successes: {res.get('NumSuccesses')}")
                    print(f"Total failures: {res.get('NumFailures')}")

    def is_project_set(self):
        if self.project.project_id != "" and self.project.session_manager is not None and self.project.cim_classes != [] and self.project.cim_objects != []:
            return True
        return False

    @staticmethod
    def get_projects_names():
        projects_dir = read_config("USER", "projects_dir")
        projects = [project_id for project_id in os.listdir(
            projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]

        return projects

    @staticmethod
    def delet_project(project_id: str = None):
        projects_dir = read_config("USER", "projects_dir")
        if project_id is None:
            projects = [project_id for project_id in os.listdir(
                projects_dir) if os.path.isdir(os.path.join(projects_dir, project_id))]
            for project in projects:
                project_path = os.path.join(projects_dir, project)
                shutil.rmtree(project_path)
            ls = ", ".join(proj for proj in projects)
            print(f"Projects deleted: {ls}")

        else:
            if os.path.isdir(os.path.join(projects_dir, project_id)):
                project_path = os.path.join(projects_dir, project_id)
                shutil.rmtree(project_path)
                print(f"Project deleted: {project_id}")

            else:
                print(f"No project with id: [{project_id}] to delete")
        # create a case sensetivity check
