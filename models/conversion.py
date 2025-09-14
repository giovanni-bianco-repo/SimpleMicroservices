from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Course(BaseModel):
    id: int = Field(
        ..., description="ID of the course", json_schema_extra={"example": 123}
    )
    name: str = Field(
        ...,
        description="Name of the course",
        json_schema_extra={"example": "Introduction to Computer Science"},
    )
    institution_id: str = Field(
        ...,
        description="Identifier for the institution offering the course",
        json_schema_extra={"example": "ABC124"},
    )
    credits: Optional[int] = Field(
        None,
        description="Number of credits for the course",
        json_schema_extra={"example": 3},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 123,
                    "name": "Introduction to Computer Science",
                    "institution_id": "ABC124",
                    "credits": 3,
                }
            ]
        }
    }


class ConversionBase(BaseModel):
    foreign_course: Course = Field(
        ...,
        description="Course taken at the host institution",
        json_schema_extra={
            "example": {
                "id": 123,
                "name": "Introduction to Computer Science",
                "institution_id": "ABC124",
                "credits": 3,
            }
        },
    )
    home_course: Course = Field(
        ...,
        description="Equivalent course at the home institution (e.g., Columbia University)",
        json_schema_extra={
            "example": {
                "id": 456,
                "name": "Data Structures",
                "institution_id": "ABC123",
                "credits": 4,
            }
        },
    )
    host_institution: str = Field(
        ...,
        description="Name of the host institution where the foreign course was taken",
        json_schema_extra={"example": "University of Oxford"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "foreign_course": {
                        "id": 123,
                        "name": "Introduction to Computer Science",
                        "institution_id": "ABC124",
                        "credits": 3,
                    },
                    "home_course": {
                        "id": 456,
                        "name": "Data Structures",
                        "institution_id": "ABC123",
                        "credits": 4,
                    },
                    "host_institution": "University of Oxford",
                }
            ]
        }
    }


class ConversionCreate(ConversionBase):
    """Payload for creating a new conversion (server generates ID and timestamps)."""

    # No extra fields; ID/timestamps are server-generated.
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "foreign_course": {
                        "id": 123,
                        "name": "Introduction to Computer Science",
                        "institution_id": "ABC124",
                        "credits": 3,
                    },
                    "home_course": {
                        "id": 456,
                        "name": "Data Structures",
                        "institution_id": "ABC123",
                        "credits": 4,
                    },
                    "host_institution": "University of Oxfords",
                }
            ]
        }
    }


class ConversionRead(ConversionBase):
    """Server representation returned to clients."""

    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Conversion ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "foreign_course": {
                        "id": 123,
                        "name": "Introduction to Computer Science",
                        "institution_id": "ABC124",
                        "credits": 3,
                    },
                    "home_course": {
                        "id": 456,
                        "name": "Data Structures",
                        "institution_id": "ABC123",
                        "credits": 4,
                    },
                    "host_institution": "University of Oxford",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }


class ConversionUpdate(BaseModel):
    """Partial update; conversion ID is taken from the path, not the body."""

    foreign_course: Optional[Course] = Field(
        None,
        description="Course taken at the host institution",
    )
    home_course: Optional[Course] = Field(
        None,
        description="Equivalent course at the home institution",
    )
    host_institution: Optional[str] = Field(
        None,
        description="Name of the host institution",
        json_schema_extra={"example": "University of Oxford"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "foreign_course": {
                        "id": 123,
                        "name": "Introduction to Computer Science",
                        "institution_id": "ABC124",
                        "credits": 3,
                    },
                    "home_course": {
                        "id": 456,
                        "name": "Data Structures",
                        "institution_id": "ABC123",
                        "credits": 4,
                    },
                }
            ]
        }
    }
