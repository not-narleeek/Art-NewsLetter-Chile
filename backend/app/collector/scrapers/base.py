from abc import ABC, abstractmethod
from typing import List
from app.schemas.event import EventCreate

class BaseScraper(ABC):
    @abstractmethod
    async def extract(self) -> List[EventCreate]:
        """
        Extracts events from the source and returns a list of EventCreate objects.
        """
        pass
