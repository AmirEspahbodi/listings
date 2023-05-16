from typing import Optional

from pydantic import BaseModel


class JWTTokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None

class TokenData(BaseModel):
    username: str | None = None
