import os
from .cim_project import CimProject
from tools.configs_editor import read_config


class ProjectManager():

    def __init__(self):
        self.project = CimProject()

    def init_project(self, project_id: str):
        self.project = CimProject()
        self.project.init_project(project_id)

    def set_project(self, project_id: str):
        project = self.project.set_project(project_id)
        if project is None:
            print(f"No project: {project_id} in projects folder")
        else:
            self.project = project
            print(f"Project: {project_id} is set")

    def get_current_project_name(self):

        if self.is_project_set():
            print("No project was set")
        else:
            print(f"Project name: {self.project.project_id}")

    def update_template(self):
        if not self.is_project_set():
            print("No project was set")
        else:
            self.project.update_template()

    def create_objects(self, update_file: str = None):
        if not self.is_project_set():
            print("No project was set")
        else:
            if update_file is not None:
                self.project.create_objects(update_file)
            else:
                self.project.create_objects()

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
