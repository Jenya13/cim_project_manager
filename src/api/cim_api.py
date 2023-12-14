import requests
import json
from tools.configs_editor import read_config


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

    def get_project_classes(self, project_id: str, session_id) -> list[dict]:

        url = f"{project_id}/classes"

        headers = dict(Authorization=f"Basic {session_id}")

        ok, data = self.make_request(url, headers=headers)

        if ok == True:
            return data
        else:
            print("ERROR get_project_classes()", data)
            return None

    def get_project_objects(self, project_id: str, session_id, params) -> list[dict]:

        url = f"{project_id}/objects"

        headers = dict(Authorization=f"Basic {session_id}")

        ok, data = self.make_request(url, params=params, headers=headers)

        if ok == True:
            return data
        else:
            print("ERROR get_project_objects()", data)
            return None

    def get_sessionId(self, project_id: str):

        username = read_config("CIM", "user")
        password = read_config("CIM", "password")

        url = f"{project_id}/session"

        ok, data = self.make_request(
            url, verb="post", auth=(username, password))

        if ok == True:
            return data
        else:
            print("ERROR get_sessionId()", data)
            return None

    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None, auth=None):
        CIM_URL = read_config("CIM", "cim_url")
        full_url = f"{CIM_URL}/{url}"

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
