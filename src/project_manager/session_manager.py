
import time
from api.cim_api import CimplicityApi


class SessionManager:

    def __init__(self, project_id: str, session_from_dict: dict = None):
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
        del session_dict["project_id"]
        return session_dict
