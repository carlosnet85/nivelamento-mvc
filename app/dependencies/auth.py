from typing import Annotated, Any, Dict
from fastapi import Depends

from app.dependencies.deps import get_current_user, get_current_user_from_cookie

user_dependency = Annotated[Dict[str, Any], Depends(get_current_user)]
user_dependency_cookie = Annotated[Dict[str, Any], Depends(get_current_user_from_cookie)]