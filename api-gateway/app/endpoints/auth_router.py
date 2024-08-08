from json import JSONDecodeError
from fastapi import APIRouter, Depends, HTTPException, Request
import httpx
from starlette.responses import JSONResponse, RedirectResponse
import logging
import requests
from pydantic import BaseModel
from typing import List



host_ip = "87.242.86.68"
keycloak_client_id = "cpr_client"
keycloak_token_url = f"http://{host_ip}:8282/realms/master/protocol/openid-connect/token"
keycloak_user_info_url = f"http://{host_ip}:8282/realms/master/protocol/openid-connect/userinfo"
keycloak_client_secret = "2Mu3KLVzBABbOgCjhCjd610O8c9d086y"
keycloak_logout_uri = f"http://{host_ip}:8282/realms/master/protocol/openid-connect/logout"

client_id = "admin-cli"
client_secret = "WP5gm4tVfw5mnPJCp52LS09PQR5ZSHHs"
username = "admin"
password = "admin"
server_url = f"http://{host_ip}:8282"
realm_name = "master"

auth_router = APIRouter(prefix='/auth', tags=['auth'])

logging.basicConfig(level=logging.INFO)

def _get_access_token():
    token_url = f"{server_url}/realms/{realm_name}/protocol/openid-connect/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(token_url, data=payload, headers=headers)
    response.raise_for_status()  # This will raise an error for 4xx/5xx responses
    return response.json()['access_token']


def _get_token(request: Request):
    token = request.headers.get("Authorization")
    logging.info(f"Received token: {token}")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        return token.split(" ")[1]
    except IndexError:
        logging.error("Token format is incorrect")
        raise HTTPException(status_code=401, detail="Unauthorized")

def get_user_role(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    user = {'role': '', 'id': '', 'username': '', 'name': '', 'email': '', 'localized_role': ''}
    try:
        response = httpx.get(keycloak_user_info_url, headers=headers)
        response.raise_for_status()
        roles = response.json()
        logging.info("roles: %s", roles)

        if "realm_access" in roles and "roles" in roles["realm_access"]:
            if "supervisor" in roles["realm_access"]["roles"]:
                user['role'] = "supervisor"
                user["localized_role"] = "Руководитель"
            elif "employee" in roles["realm_access"]["roles"]:
                user['role'] = "employee"
                user["localized_role"] = "Специалист"
        else:
            logging.warning("realm_access or roles not found in token response")

        if "sub" in roles:
            user['id'] = roles["sub"]
        user['username'] = roles.get('preferred_username', 'unknown')
        user['name'] = roles.get('name', 'unknown')
        user['email'] = roles.get('email', 'unknown')
        
        return user
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except JSONDecodeError as e:
        raise HTTPException(status_code=403, detail="Forbidden")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=403, detail="Forbidden")


def require_role(roles: List[str]):
    logging.debug(f"Required roles: {roles}")

    def role_dependency(token: str = Depends(_get_token)):
        try:
            logging.debug(f"Token: {token}")
            user = get_user_role(token)
            logging.debug(f"User: {user}")
            if user['role'] not in roles:
                raise HTTPException(status_code=403, detail="Ошибка прав доступа")
            return user
        except JSONDecodeError as e:
            raise HTTPException(status_code=403, detail="Token expired")

    return role_dependency


class LoginRequest(BaseModel):
    username: str
    password: str


@auth_router.post("/login")
async def login(request: LoginRequest):
    username = request.username
    password = request.password
    data = {
        "grant_type": "password",
        "client_id": keycloak_client_id,
        "client_secret": keycloak_client_secret,
        "username": username,
        "password": password,
        "scope": "openid"
    }
    try:
        response = httpx.post(keycloak_token_url, data=data)
        response.raise_for_status()
        token = response.json()
        return JSONResponse(token)
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@auth_router.get("/logout")
async def logout(token: str = Depends(_get_token)):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = httpx.get(keycloak_logout_uri, headers=headers)
        response.raise_for_status()
        return RedirectResponse(url="/auth/login")
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@auth_router.get("/user")
async def get_user_info(token: str = Depends(_get_token)):
    user = get_user_role(token)
    return JSONResponse(user)

@auth_router.get("/users")
async def get_all_users(_user: dict = Depends(require_role(["employee", "supervisor"]))):
    try:
        access_token = _get_access_token()
        logging.info(access_token)
        url = f"{server_url}/admin/realms/{realm_name}/users"
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # This will raise an error for 4xx/5xx responses
        users = response.json()
        
        filtered_users = []
        for user in users:
            if user["username"] != "admin":
                name = f"{user.get('lastName', '')} {user.get('firstName', '')}".strip()
                filtered_users.append({"id": user["id"], "name": name})
        return JSONResponse(filtered_users)
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {e}")
        raise HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

