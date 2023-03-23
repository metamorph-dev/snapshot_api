from pydantic import BaseModel


class Snapshot(BaseModel):
    id: str
    ready: bool = False
