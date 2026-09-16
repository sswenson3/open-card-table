from abc import ABC, abstractmethod
from app.models.card_definition import CardDefinition

class CardCatalog(ABC):
    """
     Defines the interface for resolving CardDefinition objects
     from a card catalog source.
    """   
    @abstractmethod
    def get_by_name(self,card_name: str)-> CardDefinition:
        ...
    @abstractmethod
    def add_card(self,card:CardDefinition)-> None:
        ...
 




