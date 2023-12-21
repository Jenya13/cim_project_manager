import os
import json
import time
from api.cim_api import CimplicityApi
from tools.configs_editor import read_config


class SessionManager:

    def __init__(self, project_id: str, session_from_dict: dict = None):
        self._is_initialized = False
        self.project_id = project_id
        if session_from_dict is not None:
            self.sessionId = session_from_dict["sessionId"]
            self.refreshInterval = session_from_dict["refreshInterval"]
            self.inactivityTimeout = session_from_dict["inactivityTimeout"]
            self.privileges = session_from_dict["privileges"]
            self.creationTime = session_from_dict["creationTime"]
        else:
            self.get_new_session()

    def get_new_session(self):
        api = CimplicityApi()
        session_dict = api.get_sessionId(self.project_id)
        if session_dict is not None:
            self.sessionId = session_dict["sessionId"]
            self.refreshInterval = session_dict["refreshInterval"]
            self.inactivityTimeout = session_dict["inactivityTimeout"]
            self.privileges = session_dict["privileges"]
            self.creationTime = time.time()*1000  # Current time in milliseconds

            if not self._is_initialized:
                self._is_initialized = True
                return
            session = self.to_dict()
            projects_dir = read_config("USER", "projects_dir")
            project_dir = os.path.join(projects_dir, self.project_id)
            json_file = os.path.join(
                project_dir, f"settings\\{self.project_id}.json")

            update_dict = {
                "session": session
            }
            self.update_json_file(json_file, update_dict)

    def is_session_expired(self) -> bool:
        current_time = time.time() * 1000
        elapsed_time = current_time - self.creationTime
        return elapsed_time > self.refreshInterval

    def get_session_id(self) -> str:
        session = self.sessionId[:]
        return session

    def get_project_id(self):
        project_id = self.project_id[:]
        return project_id

    def to_dict(self) -> dict:
        session_dict = self.__dict__
        session_updated_dict = session_dict.copy()
        del session_updated_dict["project_id"]
        return session_updated_dict

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

            print(f'Session successfully updated')

        except IOError as e:
            print(f'Error: Unable to update {file_path}. {e}')
