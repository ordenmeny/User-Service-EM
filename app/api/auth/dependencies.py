from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

TokenDep = Annotated[str, Depends(oauth2_scheme)]

FormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
