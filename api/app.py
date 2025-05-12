import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak import KeycloakOpenID
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KC_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL")
KC_REALM_NAME = os.getenv("KEYCLOAK_REALM")
KC_CLIENT_IDENTIFIER = os.getenv("KEYCLOAK_CLIENT_ID")
REQUIRED_ROLE = os.getenv("KEYCLOAK_ALLOWED_ROLE")

kc_auth = KeycloakOpenID(
    server_url=KC_SERVER_URL,
    client_id=KC_CLIENT_IDENTIFIER,
    realm_name=KC_REALM_NAME
)

async def check_permissions(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    auth_token = token.credentials
    try:
        payload = kc_auth.decode_token(auth_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Token неверен или истек")
    user_roles = payload.get("realm_access", {}).get("roles", [])
    if REQUIRED_ROLE not in user_roles:
        raise HTTPException(status_code=403, detail="Доступ запрещен с этим токеном")
    return True

@app.get("/reports")
async def fetch_reports(_=Depends(check_permissions)):
    return {"message": "Удачно"}
