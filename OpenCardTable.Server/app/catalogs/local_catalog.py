from app.catalogs.card_catalog import CardCatalog
from app.models.card_definition import CardDefinition

class LocalCatalog(CardCatalog):
    """
    A local implementation of the CardCatalog interface that uses an in-memory dictionary
    to store and retrieve CardDefinition objects.
    """
    def __init__(self):
        self._cards = {}

    def add_card(self, card: CardDefinition) -> None:
        """Adds a CardDefinition to the local catalog."""
        self._cards[card.definition_id] = card

    def get_by_name(self, card_name: str) -> CardDefinition:
        """Retrieves a CardDefinition by its name from the local catalog."""
        for card in self._cards.values():
            if card.name == card_name:
                return card
        raise ValueError(f"Card with name '{card_name}' not found in the local catalog.")
        return False
        




