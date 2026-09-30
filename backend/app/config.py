from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
 database_url:str
 jwt_secret:str
 jwt_expire_minutes:int=60
 refresh_token_expire_days:int=30
 bootstrap_secret:str
 redis_url:str|None=None
 storage_endpoint_url:str|None=None
 storage_bucket:str="sketchitup-documents"
 storage_access_key:str|None=None
 storage_secret_key:str|None=None
 storage_region:str="auto"
 storage_presign_seconds:int=900
 cors_origins:str="http://localhost:5173"
 model_config=SettingsConfigDict(env_file=".env",extra="ignore")
 @property
 def cors_list(self)->list[str]: return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
settings=Settings()
