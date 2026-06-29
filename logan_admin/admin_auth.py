import traceback
import requests
import json




class Auth:

    def __init__(self):
        pass

    def login_admin(self):
        try:
            print("b")
            email = "testuser23@yopmail.com"
            password = "Pass@123"

            # response = requests.post(
            #     "https://adminapi-logan.kodedice.com/api/v1/auth/login",
            #     json=payload
            # )

            payload = {"token":0,"email":email,"password":password}
            response = requests.post("https://adminapi-logan.kodedice.com/api/v1/auth/login", json=payload)
            print("responce: ",response.json())

            if response.status_code != 200:
                message = response.json()["message"]

                print(f"{message}")
                return message
            else:
                print("Login successful")
                return response

        except Exception:
            traceback.print_exc()
            print("error")
            raise





