from typing import Any, Dict, List, Union


class StandardResponse:
    def __init__(
        self,
        status: str,
        data: Any,
        errors: Union[str, List[str]],
    ):
        self.status = status
        self.data = data
        self.errors = errors

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "data": self.data, "errors": self.errors}


def success_response(data: Any) -> Dict[str, Any]:
    return {"status": "success", "data": data}


def error_response(error: Union[str, List[str]]) -> Dict[str, Any]:
    if isinstance(error, str):
        errors = [error]
    else:
        errors = error
    return {"status": "error", "errors": errors}
