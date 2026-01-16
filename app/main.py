from fastapi import FastAPI
from app.api.auth.views import auth_router
from app.api.auth.mock.views import mock_router
import uvicorn
from app.core.register_handlers import register_exception_handlers
from fastapi.responses import ORJSONResponse


app = FastAPI(
    default_response_class=ORJSONResponse,
)

app.include_router(auth_router)
app.include_router(mock_router)

register_exception_handlers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
