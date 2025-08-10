import json
from typing import Any, cast

import models
from pydantic import BaseModel


class PydanticSerializer(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump() | {"__type__": type(obj).__name__}

        return json.JSONEncoder.default(self, obj)


def pydantic_decoder(obj: dict[str, Any]) -> Any:
    if "__type__" in obj:
        cls = getattr(models, obj["__type__"], None)
        if isinstance(cls, type) and issubclass(cls, BaseModel):
            model_cls: type[BaseModel] = cls
            # Prefer Pydantic v2 API if available
            if hasattr(model_cls, "model_validate"):
                return model_cls.model_validate(obj)  # type: ignore[attr-defined]
            # Fallback for Pydantic v1
            return cast(Any, model_cls).parse_obj(obj)
    return obj


# Encoder function
def pydantic_dumps(obj: Any) -> str:
    return json.dumps(obj, cls=PydanticSerializer, sort_keys=True, default=str)


# Decoder function
def pydantic_loads(obj: str) -> Any:
    return json.loads(obj, object_hook=pydantic_decoder)
