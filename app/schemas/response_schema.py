from pydantic import BaseModel, Field, field_validator

class ValidationResponse(BaseModel):
    score: float = Field(..., ge=0, le=10)
    summary: str = Field(..., min_length=1)
    strengths: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)
    market_notes: str | None = Field(None)

    @field_validator("strengths", "risks", "competitors")
    @classmethod
    def limit_list_length(cls, v):
        if len(v) > 10:
            raise ValueError("List cannot have more than 10 items.")
        return v