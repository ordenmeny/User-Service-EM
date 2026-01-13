from fastapi import FastAPI
from app.api.auth.views import auth_router
import uvicorn
from app.core.register_handlers import register_exception_handler


app = FastAPI()
app.include_router(auth_router)

register_exception_handler(app)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
