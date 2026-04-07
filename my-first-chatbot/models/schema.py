from pydantic import BaseModel
from typing import List

class Summary(BaseModel):
    summary: str
    keywords: List[str]