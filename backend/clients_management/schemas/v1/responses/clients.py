from typing import List

from pydantic import Field

from .standard import StandardResponse
from schemas.client import Client


class ClientsResponse(StandardResponse):
    """TODO: docstring"""

    clients: List[Client] = Field()
