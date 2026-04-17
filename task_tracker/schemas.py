from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=500)


class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
    created_at: str


class TaskPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    done: bool | None = Field(default=None, strict=True)
