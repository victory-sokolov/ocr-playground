from pydantic import Base64Bytes, BaseModel


class OcrResponse(BaseModel):
    data: str


class OcrRequest(BaseModel):
    image_data: Base64Bytes
