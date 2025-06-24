from datetime import datetime

from apps.api.v1.schemas.base_schema import BaseSchema


class GetLogEntryOutSchema(BaseSchema):
    timestamp: datetime
    remote_addr: str
    method: str
    uri: str
    http_version: str
    status: int
    size: int
    referrer: str | None = None
    user_agent: str | None = None

    model_config = {'from_attributes': True}
