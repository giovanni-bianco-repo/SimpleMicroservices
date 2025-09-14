from __future__ import annotations

from typing import Optional, List, Annotated
from datetime import datetime

from uuid import UUID, uuid4
from pydantic import BaseModel, Field, StringConstraints
from models.conversion import (
    ConversionBase,
)  # assuming this has foreign_course/home_course/etc.

# Destination ID: 3 uppercase letters + 3 digits (e.g., ABC123)
DestIdType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}\d{3}$")]


class DestinationBase(BaseModel):
    """Model for am university destination for an exchange program"""

    dest_id: DestIdType = Field(
        ...,
        description="Destination ID (3 uppercase letters + 3 digits).",
        json_schema_extra={"example": "ABC123"},
    )
    name: str = Field(
        ...,
        description="Name of the destination.",
        json_schema_extra={"example": "University of Washington"},
    )
    continent: str = Field(
        ...,
        description="Continent where the destination is located.",
        json_schema_extra={"example": "North America"},
    )
    country: str = Field(
        ...,
        description="Country where the destination is located.",
        json_schema_extra={"example": "United States"},
    )
    department: str = Field(
        ...,
        description="Department where the student would formally be enrolled.",
        json_schema_extra={
            "example": "Paul G. Allen School of Computer Science & Engineering"
        },
    )
    conversions: Optional[List[ConversionBase]] = Field(
        None,
        description=(
            "List of course conversions. Each item should map a foreign course to a home course "
            "(e.g., fields like foreign_course, home_course, host_institution per ConversionBase). "
            "Optional if no courses have been converted yet."
        ),
        json_schema_extra={
            "example": [
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
                },
                {
                    "foreign_course": {
                        "id": 789,
                        "name": "Algorithms",
                        "institution_id": "ABC124",
                        "credits": 3,
                    },
                    "home_course": {
                        "id": 101,
                        "name": "Operating Systems",
                        "institution_id": "ABC123",
                        "credits": 4,
                    },
                    "host_institution": "University of Cambridge",
                },
            ]
        },
    )


class DestinationCreate(DestinationBase):
    """Creation payload; dest_id is provided by the client."""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "dest_id": "ABC123",
                    "name": "University of Washington",
                    "continent": "North America",
                    "country": "United States",
                    "department": "Paul G. Allen School of Computer Science & Engineering",
                    "conversions": [
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
                        },
                        {
                            "foreign_course": {
                                "id": 789,
                                "name": "Algorithms",
                                "institution_id": "ABC124",
                                "credits": 3,
                            },
                            "home_course": {
                                "id": 101,
                                "name": "Operating Systems",
                                "institution_id": "ABC123",
                                "credits": 4,
                            },
                            "host_institution": "University of Cambridge",
                        },
                    ],
                }
            ]
        }
    }


class DestinationUpdate(BaseModel):
    """Update payload; all fields optional."""

    dest_id: Optional[DestIdType] = Field(
        None,
        description="Destination ID (3 uppercase letters + 3 digits).",
        json_schema_extra={"example": "ABC123"},
    )
    name: Optional[str] = Field(
        None,
        description="Name of the destination.",
        json_schema_extra={"example": "University of Washington"},
    )
    continent: Optional[str] = Field(
        None,
        description="Continent where the destination is located.",
        json_schema_extra={"example": "North America"},
    )
    country: Optional[str] = Field(
        None,
        description="Country where the destination is located.",
        json_schema_extra={"example": "United States"},
    )
    department: Optional[str] = Field(
        None,
        description="Department where the student would formally be enrolled.",
        json_schema_extra={
            "example": "Paul G. Allen School of Computer Science & Engineering"
        },
    )
    conversions: Optional[List[ConversionBase]] = Field(
        None,
        description=(
            "List of course conversions. Each item should follow ConversionBase "
            "(mapping a foreign course to a home course)."
        ),
        json_schema_extra={
            "example": [
                {
                    "foreign_course": {
                        "id": 222,
                        "name": "Databases",
                        "institution_id": "ABC124",
                        "credits": 6,
                    },
                    "home_course": {
                        "id": 333,
                        "name": "Intro to Databases",
                        "institution_id": "ABC123",
                        "credits": 6,
                    },
                    "host_institution": "University of Edinburgh",
                }
            ]
        },
    )


class DestinationRead(DestinationBase):
    """Read-only view of a Destination."""

    id: UUID = Field(
        default_factory=uuid4,
        description="Unique identifier for the destination (UUID).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    dest_id: DestIdType = Field(
        ...,
        description="Destination ID (3 uppercase letters + 3 digits).",
        json_schema_extra={"example": "ABC123"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "dest_id": "ABC123",
                    "name": "University of Washington",
                    "continent": "North America",
                    "country": "United States",
                    "department": "Paul G. Allen School of Computer Science & Engineering",
                    "conversions": [
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
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
