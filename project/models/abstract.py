import json
from typing import Any, Dict, Optional, Set
from werkzeug import Response
from werkzeug.exceptions import HTTPException


class SerializationError(HTTPException):
    code = 422
    description = "Failed to serialize response"
    extra: Dict[str, Any] = {}

    def __init__(
        self,
        description: Optional[str] = None,
        response: Optional[Response] = None,
        extra: Dict[str, Any] = None
    ) -> None:
        if extra is not None:
            self.extra = extra

        super().__init__(description, response)


class SerializableModel():
    """
        Tries to return JSON serialized version of the models.
        If a field cannot be serialized, returns a custom exception (with HTTP feature).
    """
    non_serializable_fields: Set[str] = set()
    id: Optional[int] = None

    def __init__(self, *args, **kwargs) -> None:
        for field, value in kwargs.items():
            setattr(self, field, value)

    def serialize(self, *args, **kwargs) -> str:
        '''
            Return a serialized version of the model instance.
            Provide args to store in a list called args_list
            Provide kwargs to store as key: value
        '''
        dict_self: Dict[str, Any] = {}

        for field, value in vars(self).items():
            if self._assert_serializable(field):
                dict_self.setdefault(
                    field,
                    self._to_json_serializable(value),
                )

        if len(kwargs) > 0:
            dict_self.update(kwargs)

        if len(args) > 0:
            dict_self["args_list"] = list(args)

        json_self = json.dumps(dict_self)

        return json_self

    def _assert_serializable(self, field_name: str) -> bool:
        if field_name in self.non_serializable_fields:
            return False
        if field_name.startswith("_"):
            return False

        return True

    def _to_json_serializable(self, to_serialize: Any) -> Any:
        failed_to_serialize = False
        try:
            json.dumps(to_serialize)
        except (ValueError, TypeError):
            failed_to_serialize = True

        if failed_to_serialize:
            try:
                return str(to_serialize)
            except Exception as exc:
                raise SerializationError(
                    "Error serializing a model to JSON",
                    extra={
                        "model_name": type(self).__name__,
                        "model_id": self.id,
                    }
                )
        else:
            return to_serialize
