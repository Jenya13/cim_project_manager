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

    def get_sessionId(self, project_id: str):

        username = read_config("CIM", "user")
        password = read_config("CIM", "password")

        url = f"{project_id}/session"

        ok, data = self.make_request(
            url, verb="post", auth=(username, password))

        if ok == True:
            return data
        else:
            return None

    def get_project_classes(self, project_id: str, session_id: str) -> list[dict]:

        url = f"{project_id}/classes"

        headers = dict(Authorization=f"Basic {session_id}")

        ok, data = self.make_request(url, headers=headers)

        if ok == True:
            return data
        else:
            print(data)
            return None

    def get_project_objects(self, project_id: str, session_id: str, params) -> list[dict]:

        url = f"{project_id}/objects"

        headers = dict(Authorization=f"Basic {session_id}")

        ok, data = self.make_request(url, params=params, headers=headers)

        if ok == True:
            return data
        else:
            print(data)
            return None

    def create_objects(self, project_id: str, session_id: str, obj_data):

        url = f"{project_id}/objects"

        headers = dict(Authorization=f"Basic {session_id}")

        verb = "post"

        ok, data = self.make_request(url, verb, data=obj_data, headers=headers)

        if ok == True:
            return data
        else:
            return data

    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None, auth=None):
        CIM_URL = read_config("CIM", "cim_url")
        full_url = f"{CIM_URL}{url}"

        if data is not None:
            data = json.dumps(data)

        try:
            response = None
            if verb == "get":

                response = self.session.get(
                    full_url, params=params, data=data, headers=headers, verify=False)

            if verb == "post" and auth is not None:

                response = self.session.post(
                    full_url, params=params, data=data, headers=headers, auth=(auth[0], auth[1]), verify=False)

            if verb == "post" and auth is None:

                response = self.session.post(
                    full_url, params=params, data=data, headers=headers, verify=False)

            if response is None:
                return False, {'error': 'verb not found'}

            if response.status_code == code:
                return True, response.json()
            elif response.status_code == 400:
                try:
                    # Attempt to parse the response content as JSON
                    json_data = response.json()

                    return True, json_data
                except json.JSONDecodeError:
                    # If parsing as JSON fails, return the response text
                    return True, response.text
            else:
                return False, response.json()

        except Exception as error:
            return False, {'Exception': error, "Response": response}


# print("in post")
# print(f"url:{full_url}")
# print(f"params:{params}")
# print(f"data:{data}")
# print(f"headers:{headers}")
# print(f"auth:{auth}")
