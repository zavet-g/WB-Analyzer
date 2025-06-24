from pydantic import ConfigDict

from apps.api.v1.schemas.base_schema import BaseSchema
from apps.api.v1.schemas.log_entry_schema import GetLogEntryOutSchema


class ServerOutSchema(BaseSchema):
    name: str
    description: str

    model_config = {'from_attributes': True}


class ServerWithLogsOutSchema(BaseSchema):
    id: int
    name: str
    ip_address: str
    logs: list[GetLogEntryOutSchema]

    model_config = ConfigDict(from_attributes=True)
