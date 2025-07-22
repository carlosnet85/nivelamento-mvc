from typing import Annotated, Any, Dict
from fastapi import Depends

from app.dependencies.deps import get_current_user

user_dependency = Annotated[Dict[str, Any], Depends(get_current_user)]