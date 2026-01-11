from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

TokenDep = Annotated[str, Depends(oauth2_scheme)]