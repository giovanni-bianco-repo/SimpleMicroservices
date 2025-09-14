from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from uuid import UUID
from models.address import AddressCreate, AddressRead, AddressUpdate

from typing import Dict

# In-memory database (to be imported from main)
addresses: Dict[UUID, AddressRead] = None

router = APIRouter()


@router.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate) -> AddressRead:
    """Create a new address and add to the in-memory database."""
    if address.id in addresses:
        raise HTTPException(
            status_code=400, detail="Address with this ID already exists"
        )
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]


@router.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
) -> List[AddressRead]:
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results


@router.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID) -> AddressRead:
    """Retrieve an address by its UUID."""
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]


@router.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate) -> AddressRead:
    """Update an existing address by its UUID."""
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]
