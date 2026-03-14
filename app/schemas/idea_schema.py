from pydantic import BaseModel, Field, field_validator
import re

class IdeaInput(BaseModel):
    idea: str = Field(..., min_length=10, max_length=1000)

    @field_validator("idea")
    @classmethod
    def sanitize_idea(cls, v):
        v = v.strip()
        if re.search(r"<.*?>|javascript:|eval\(", v, re.IGNORECASE):
            raise ValueError("Invalid characters detected in idea.")
        return v

class IdeaWithContext(IdeaInput):
    pass