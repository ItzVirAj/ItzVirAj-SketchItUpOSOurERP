from datetime import datetime,timedelta,timezone
from uuid import UUID
import jwt
from pwdlib import PasswordHash
from ...config import settings
passwords=PasswordHash.recommended()
def hash_password(value:str)->str:return passwords.hash(value)
def verify_password(value:str,hashed:str)->bool:return passwords.verify(value,hashed)
def create_access_token(user_id:UUID,organization_id:UUID|None,roles:list[str])->str:
 now=datetime.now(timezone.utc);return jwt.encode({"sub":str(user_id),"org":str(organization_id) if organization_id else None,"roles":roles,"iat":now,"exp":now+timedelta(minutes=settings.jwt_expire_minutes)},settings.jwt_secret,algorithm="HS256")
def decode_access_token(token:str)->dict:return jwt.decode(token,settings.jwt_secret,algorithms=["HS256"])
