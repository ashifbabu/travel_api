from typing import Any, Dict, Optional

class StandardResponse:
    def __init__(self, status: str, data: Optional[Any] = None, errors: Optional[Dict[str, Any]] = None):
        self.status = status
        self.data = data
        self.errors = errors

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "data": self.data,
            "errors": self.errors
        }

def success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "status": "success",
        "data": data
    }

def error_response(error_message: str) -> Dict[str, Any]:
    return {
        "status": "error",
        "errors": [error_message]
    }
