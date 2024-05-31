# pylint: disable=not-callable

import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class DateTimeModelMixin:
    created_at: datetime.datetime = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: datetime.datetime = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class DateTimeSchemaMixin:
    created_at: datetime.datetime
    updated_at: datetime.datetime
