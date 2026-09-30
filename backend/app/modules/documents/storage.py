from uuid import UUID
import boto3
from botocore.client import Config
from fastapi import HTTPException
from ...config import settings

def _client():
    if not settings.storage_endpoint_url or not settings.storage_access_key or not settings.storage_secret_key:
        raise HTTPException(503,"Document storage is not configured")
    return boto3.client("s3",endpoint_url=settings.storage_endpoint_url,aws_access_key_id=settings.storage_access_key,aws_secret_access_key=settings.storage_secret_key,region_name=settings.storage_region,config=Config(signature_version="s3v4"))

def presigned_upload(key:str,content_type:str|None=None):
    params={"Bucket":settings.storage_bucket,"Key":key}
    if content_type: params["ContentType"]=content_type
    return _client().generate_presigned_url("put_object",Params=params,ExpiresIn=settings.storage_presign_seconds)

def presigned_download(key:str):
    return _client().generate_presigned_url("get_object",Params={"Bucket":settings.storage_bucket,"Key":key},ExpiresIn=settings.storage_presign_seconds)
