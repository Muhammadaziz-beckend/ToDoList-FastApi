from pydantic import BaseModel, Field
from typing import Optional


class TaskBase(BaseModel):
    titel: str
    description: str


class TaskUpdate(BaseModel):
    titel: Optional[str] = Field(None, exclude=True)
    description: Optional[str] = Field(None, exclude=True)

    def dict(self, *args, **kwargs):
        if self.description is None:
            kwargs['exclude'] = {'description'}
        return super().dict(*args, **kwargs)


class TaskCrete(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
