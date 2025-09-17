# Sprint Completion Status Report
**Student Name:** Bianco Giovanni
**Sprint Number:** Sprint 0
**Duration:** 12/09/2025 – 14/09/2025
**Report Date:** 14/09/2025
### 1. Sprint Goal 🎯
**Defined Goal:**
1. Clone Professor Ferguson’s Simple Microservices Repository.
2. Create a project that is my version using two different resources.
   a. Copy the structure of Professor Ferguson’s repository
   b. Define two models.
   c. Implement “API first” definition by implementing placeholder routes for
      each resource:
      i. GET /<resource>
      ii. POST /<resource>
      iii. GET /<resource>/{id}
      iv. PUT /<resource>/{id}
      v. DELETE /<resource>/{id}
   d. Annotate models and paths to autogenerate OpenAPI document.
   e. Test OpenAPI document dispatching to methods.


**Outcome:** Achieved

### 2. Completed Work ✅
**Resource0** (course, used in resource1)
```python

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
```
**Resource1**: model of a course conversion between home and host university (in the context of an exchange for a student who studied abroad). It is characterized by 2 courses (the course taken abroad at the host institution and the corresponding home course). It also specifies what is the host institution
```python

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

```


**Resource 2**: destination university in the context of a study abroad program
```python

DestIdType = Annotated[str, StringConstraints(pattern=r"^[A-Z]{3}\d{3}$")]

class DestinationBase(BaseModel):
    '''Model for a university destination for an exchange program'''
    dest_id: DestIdType = Field(
        ...,
        description="Destination ID (3 uppercase letters + 3 digits).",
        json_schema_extra={"example": "ABC123"},
    )
    name: str = Field(
        ...,
        description="Name of the destination.",
        json_schema_extra={"example": "University of Milan"},
    )
    continent: str = Field(
        ...,
        description="Continent where the destination is located.",
        json_schema_extra={"example": "Europe"},
    )
    country: str = Field(
        ...,
        description="Country where the destination is located.",
        json_schema_extra={"example": "Italy"},
    )
    department: str = Field(
        ...,
        description="Department where the student would formally be enrolled.",
        json_schema_extra={
            "example": "School of Computer Science & Engineering"
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
                    "host_institution": "University of Milan",
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
                    "host_institution": "University of Milan",
                },
            ]
        },
    )


```

### Routes
For destinations 
```python 
@router.post("/destinations", response_model=DestinationRead, status_code=201)
def create_destination(destination: DestinationCreate) -> DestinationRead:
    """
    Create a new destination and add it to the in-memory database.
    ID/timestamps are generated by the server (DestinationRead defaults).
    """
    # Build the server-side model (generates id/created_at/updated_at)
    created = DestinationRead(**destination.model_dump())

    # Prevent accidental collisions (extremely unlikely with UUID4, but cheap to check)
    if created.id in destinations:
        raise HTTPException(
            status_code=400, detail="Generated ID collision; retry the request"
        )

    destinations[created.id] = created
    return created


@router.get("/destinations", response_model=List[DestinationRead])
def list_destinations(
    name: Optional[str] = Query(None, description="Filter by destination name"),
    country: Optional[str] = Query(None, description="Filter by country"),
    institution: Optional[str] = Query(None, description="Filter by institution"),
    continent: Optional[str] = Query(None, description="Filter by continent"),
) -> List[DestinationRead]:
    """
    List destinations, with optional filters.
    (Adjust filters to match your DestinationRead fields.)
    """
    results = list(destinations.values())

    if name is not None:
        # Assumes DestinationRead has a 'name' field
        results = [d for d in results if getattr(d, "name", None) == name]

    if country is not None:
        results = [d for d in results if getattr(d, "country", None) == country]

    if institution is not None:
        results = [d for d in results if getattr(d, "name", None) == institution]

    if continent is not None:
        results = [d for d in results if getattr(d, "continent", None) == continent]

    return results


@router.get("/destinations/{destination_id}", response_model=DestinationRead)
def get_destination(destination_id: UUID) -> DestinationRead:
    """Retrieve a destination by its UUID."""
    dest = destinations.get(destination_id)
    if dest is None:
        raise HTTPException(status_code=404, detail="Destination not found")
    return dest


@router.patch("/destinations/{destination_id}", response_model=DestinationRead)
def update_destination(
    destination_id: UUID, update: DestinationUpdate
) -> DestinationRead:
    """Update an existing destination by its UUID."""
    existing = destinations.get(destination_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    # Start from stored dict, then apply only provided fields
    stored = existing.model_dump()
    stored.update(update.model_dump(exclude_unset=True))

    # Refresh updated_at
    stored["updated_at"] = datetime.now(timezone.utc)

    updated = DestinationRead(**stored)
    destinations[destination_id] = updated
    return updated

@router.delete("/destinations/{dest_id}", status_code=204)
def delete_destination(destination_id: UUID) -> None:
    """Delete a destination by its ID."""
    if destination_id not in destinations:
        raise HTTPException(status_code=404, detail="Destination not found")
    del destinations[destination_id]

```
For conversions

```python

@router.post("/conversions", response_model=ConversionRead, status_code=201)
def create_conversion(conversion: ConversionCreate) -> ConversionRead:
    """
    Create a new conversion and add it to the in-memory database.
    ID/timestamps are generated by the server (ConversionRead defaults).
    """
    # Build the server-side model (generates id/created_at/updated_at)
    created = ConversionRead(**conversion.model_dump())

    # Prevent accidental collisions (extremely unlikely with UUID4, but cheap to check)
    if created.id in conversions:
        raise HTTPException(status_code=400, detail="Generated ID collision; retry the request")

    conversions[created.id] = created
    return created


@router.get("/conversions", response_model=List[ConversionRead])
def list_conversions(
    home_course_name: Optional[str] = Query(None, description="Filter by home course name"),
    home_course_id: Optional[int] = Query(None, description="Filter by home course ID"),
    host_institution: Optional[str] = Query(None, description="Filter by host institution"),
) -> List[ConversionRead]:
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
    """Update an existing conversion by its UUID."""
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
def delete_conversion(conversion_id: UUID) -> None:
    """Delete a conversion by its ID."""
    if conversion_id not in conversions:
        raise HTTPException(status_code=404, detail="Conversion not found")
    del conversions[conversion_id]


```


### OpenAPI Document (Partial)
![alt text](<Screenshot 2025-09-14 at 22.19.41.png>)
![alt text](<Screenshot 2025-09-14 at 22.18.45.png>)



Link to Recording of Demo
https://drive.google.com/file/d/1aLGBszbSp8cx1DomkIBRjvf3cS3JZFvO/view?usp=sharing
Link to GitHub Repository
https://github.com/giovanni-bianco-repo/SimpleMicroservices
