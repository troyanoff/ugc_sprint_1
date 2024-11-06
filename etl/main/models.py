from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class InsensitiveEnum(Enum):
    @classmethod
    def _missing_(cls, value: str):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"'{value}' is not a valid {cls.__name__}")


class ViewEventType(str, InsensitiveEnum):
    load = "load"
    refresh = "refresh"
    close = "close"


class ClickEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    event_dt: datetime
    clicked_element_id: UUID

    @classmethod
    def get_table_name(cls) -> str:
        return "events.click_events"


class ViewEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    event_dt: datetime
    event_type: ViewEventType

    @classmethod
    def get_table_name(cls) -> str:
        return "events.view_events"


class QualityChangeEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    event_dt: datetime
    movie_id: UUID
    current_quality: int
    chosen_quality: int

    @classmethod
    def get_table_name(cls) -> str:
        return "events.quality_change_events"


class VideoProgressEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    event_dt: datetime
    movie_id: UUID
    seconds: int
    is_stopped: bool

    @classmethod
    def get_table_name(cls) -> str:
        return "events.video_progress_events"


class QueryEvent(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    event_dt: datetime
    is_genre_filtered: bool
    is_rating_filtered: bool
    is_actor_filtered: bool

    @classmethod
    def get_table_name(cls) -> str:
        return "events.query_events"
