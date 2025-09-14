from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from models.person import PersonCreate, PersonRead, PersonUpdate

from typing import Dict

# In-memory database (to be imported from main)
persons: Dict[UUID, PersonRead] = None

router = APIRouter()


@router.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate) -> PersonRead:
    """Create a new person and add to the in-memory database."""
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read


@router.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(
        None, description="Filter by date of birth (YYYY-MM-DD)"
    ),
    city: Optional[str] = Query(
        None, description="Filter by city of at least one address"
    ),
    country: Optional[str] = Query(
        None, description="Filter by country of at least one address"
    ),
) -> List[PersonRead]:
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [
            p for p in results if any(addr.country == country for addr in p.addresses)
        ]
    return results


@router.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID) -> PersonRead:
    """Retrieve a person by their UUID."""
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]


@router.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate) -> PersonRead:
    """Update an existing person by their UUID."""
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]
