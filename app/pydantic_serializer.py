import json

import models
from pydantic import BaseModel


class PydanticSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump() | {"__type__": type(obj).__name__}

        return json.JSONEncoder.default(self, obj)


def pydantic_decoder(obj):
    if "__type__" in obj:
        if obj["__type__"] in dir(models):
            cls = getattr(models, obj["__type__"])
            return cls.parse_obj(obj)
    return obj


# Encoder function
def pydantic_dumps(obj):
    return json.dumps(obj, cls=PydanticSerializer, sort_keys=True, default=str)


# Decoder function
def pydantic_loads(obj):
    return json.loads(obj, object_hook=pydantic_decoder)
