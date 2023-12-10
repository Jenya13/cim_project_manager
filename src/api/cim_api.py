import requests
import json
import constants.defs as defs

############# Not for production use - you have to generate SSL certificate #############
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#########################################################################################


class CimplicityApi:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    # def get_project_classes(self, project:dict)->list[dict]:
    #     project_id = project["id"]
    #     session_id = project["session"]["sessionId"]

    #     url = f"{project_id}/classes"

    #     headers = dict(Authorization=f"Basic {session_id}")

    #     ok, data = self.make_request(url, headers=headers)

    #     if ok == True:
    #         return data
    #     else:
    #         print("ERROR get_project_classes()", data)
    #         return None

    # def get_project_objects(self, project:dict,params):

    #     project_id = project["id"]
    #     session_id = project["session"]["sessionId"]

    #     url = f"{project_id}/objects"

    #     headers = dict(Authorization=f"Basic {session_id}")

    #     ok, data = self.make_request(url, params=params ,headers=headers)

    #     if ok == True:
    #         return data
    #     else:
    #         print("ERROR get_project_objects()", data)
    #         return None

    # def get_sessionId(self,project:dict):

    #     project_id = project["id"]
    #     username = project["auth"]["username"]
    #     password = project["auth"]["password"]

    #     url = f"{project_id}/session"

    #     ok, data = self.make_request(
    #         url, verb="post", auth=(username, password))

    #     if ok == True:
    #         return data
    #     else:
    #         print("ERROR get_sessionId()", data)
    #         return None

    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None, auth=None):
        full_url = f"{defs.CIM_URL}/{url}"

        if data is not None:
            data = json.dumps(data)

        try:
            response = None
            if verb == "get":
                response = self.session.get(
                    full_url, params=params, data=data, headers=headers, verify=False)
            if verb == "post":
                response = self.session.post(full_url, params=params, data=data, headers=headers, auth=(
                    auth[0], auth[1]), verify=False)

            if response == None:
                return False, {'error': 'verb not found'}

            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()

        except Exception as error:
            return False, {'Exception': error}


# import time
#
# class SessionManager:
#     def __init__(self, session_timeout_ms):
#         self.session_timeout_ms = session_timeout_ms
#         self.last_activity_time = time.time() * 1000  # Current time in milliseconds

#     def is_session_expired(self):
#         current_time = time.time() * 1000
#         elapsed_time = current_time - self.last_activity_time
#         return elapsed_time > self.session_timeout_ms

#     def update_activity_time(self):
#         self.last_activity_time = time.time() * 1000

# # Example usage:
# session_timeout_ms = 900000  # 15 minutes in milliseconds
# session_manager = SessionManager(session_timeout_ms)

# # Before making an API request, check if the session has expired
# if session_manager.is_session_expired():
#     # Get a new session here (e.g., by sending a new login request)
#     # Once you have the new session, update the last activity time
#     session_manager.update_activity_time()
