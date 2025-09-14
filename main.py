from __future__ import annotations

from dotenv import load_dotenv

load_dotenv()
import os

port = int(os.environ.get("FASTAPIPORT", 8000))

import os
import socket
from datetime import datetime

from typing import Dict
from fastapi import FastAPI
from uuid import UUID
from models.person import PersonRead
from models.address import AddressRead
from models.conversion import ConversionRead
from models.destination import DestinationRead


# In-memory databases
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
conversions: Dict[UUID, ConversionRead] = {}
destinations: Dict[UUID, DestinationRead] = {}
# FastAPI app
app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# Routers
from services import persons as persons_module
from services import addresses as addresses_module
from services import health as health_module
from services import conversions as conversions_module
from services import destinations as destinations_module

persons_module.persons = persons
addresses_module.addresses = addresses
app.include_router(persons_module.router)
app.include_router(addresses_module.router)
app.include_router(health_module.router)
app.include_router(conversions_module.router)
app.include_router(destinations_module.router)


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}


# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    print(port)

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
