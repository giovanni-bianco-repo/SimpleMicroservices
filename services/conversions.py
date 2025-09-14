from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
from uuid import UUID

from models.conversion import ConversionCreate, ConversionRead, ConversionUpdate

router = APIRouter()

# In-memory "DB"
conversions: Dict[UUID, ConversionRead] = {}


@router.post("/conversions", response_model=ConversionRead, status_code=201)
def create_conversion(conversion: ConversionCreate) -> ConversionRead:
    """Create a new conversion."""
    # Build the server-side model (generates id/created_at/updated_at)
    created = ConversionRead(**conversion.model_dump())

    # Prevent accidental collisions (extremely unlikely with UUID4, but cheap to check)
    if created.id in conversions:
        raise HTTPException(
            status_code=400, detail="Generated ID collision; retry the request"
        )

    conversions[created.id] = created
    return created


@router.get("/conversions", response_model=List[ConversionRead])
def list_conversions(
    home_course_name: Optional[str] = Query(
        None, description="Filter by home course name"
    ),
    home_course_id: Optional[int] = Query(None, description="Filter by home course ID"),
    host_institution: Optional[str] = Query(
        None, description="Filter by host institution"
    ),
) -> List[ConversionRead]:
    """List all conversions."""
    results = list(conversions.values())

    if home_course_name is not None:
        results = [c for c in results if c.home_course.name == home_course_name]

    if home_course_id is not None:
        results = [c for c in results if c.home_course.id == home_course_id]

    if host_institution is not None:
        results = [c for c in results if c.host_institution == host_institution]

    return results


@router.get("/conversions/{conversion_id}", response_model=ConversionRead)
def get_conversion(conversion_id: UUID) -> ConversionRead:
    """Retrieve a conversion by its UUID."""
    conv = conversions.get(conversion_id)
    if conv is None:
        raise HTTPException(status_code=404, detail="Conversion not found")
    return conv


@router.patch("/conversions/{conversion_id}", response_model=ConversionRead)
def update_conversion(conversion_id: UUID, update: ConversionUpdate) -> ConversionRead:
    """Update an existing conversion."""
    existing = conversions.get(conversion_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Conversion not found")

    # Start from stored dict, then apply only provided fields
    stored = existing.model_dump()
    stored.update(update.model_dump(exclude_unset=True))

    # Refresh updated_at
    stored["updated_at"] = datetime.now(timezone.utc)

    updated = ConversionRead(**stored)
    conversions[conversion_id] = updated
    return updated


@router.delete("/conversions/{conversion_id}", status_code=204)
def delete_conversion(conversion_id: str) -> None:
    """Delete a conversion by its ID."""
    if conversion_id not in conversions:
        raise HTTPException(status_code=404, detail="Conversion not found")
    del conversions[conversion_id]
