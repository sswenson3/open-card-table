import pytest

from app.models.card_definition import CardDefinition
from app.catalogs.card_catalog import CardCatalog

#Test our interface CardCatalog,  Implement a subclass ( enforced application of interface) and test it)

def test_card_catalog_can_be_implemented_and_used():
    class DummyCatalog(CardCatalog):
        def get_by_name(self, card_name: str) -> CardDefinition:
            return CardDefinition(definition_id="dummy", name=card_name)
        def add_card(self, card: CardDefinition) -> bool:
            return True

    catalog = DummyCatalog()
    card = catalog.get_by_name("Test Card")
   
    assert isinstance(card, CardDefinition)
    assert card.name == "Test Card"
    assert card.definition_id == "dummy"

#negative test
def test_card_catalog_raises_error_on_invalid_implementation():
    class InvalidCatalog(CardCatalog):
        pass  # Does not implement get_by_name
    with pytest.raises(TypeError):
        catalog = InvalidCatalog() 
        