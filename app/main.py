from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter
from app.api.v1.endpoints import auth, jilla, member, news, user


router = APIRouter()
app = FastAPI(root_path="/",
              title="Yogakshema Sabha API",
              description="YKS",
              version="0.0.1a")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Yogakshema Sabha API",
        version="0.0.1a",
        description="YKS",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    

    for path in openapi_schema.get("paths", {}):
        for method in openapi_schema["paths"][path]:
            if "security" not in openapi_schema["paths"][path][method]:
                openapi_schema["paths"][path][method]["security"] = []
            openapi_schema["paths"][path][method]["security"].append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

origins = [
    "http://localhost:4200",
    "https://msla-admin.digistratz.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins (like your React app)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(auth.router)
app.include_router(jilla.router)
app.include_router(news.router)
app.include_router(member.router)
