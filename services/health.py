from fastapi import APIRouter, Query, Path
from datetime import datetime
import socket
from typing import Optional
from models.health import Health

router = APIRouter()

# Health endpoint logic


def make_health(echo: Optional[str], path_echo: Optional[str] = None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo,
    )


@router.get("/health", response_model=Health)
def get_health_no_path(
    echo: str | None = Query(None, description="Optional echo string")
):
    return make_health(echo=echo, path_echo=None)


@router.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)
