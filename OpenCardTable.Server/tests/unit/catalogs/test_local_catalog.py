import pytest
from app.catalogs.local_catalog import LocalCatalog
from app.models.card_definition import CardDefinition


#test instatiation
def test_local_catalog_can_be_instantiated():
    catalog = LocalCatalog()
    assert isinstance(catalog, LocalCatalog)

#test add a card
def test_local_catalog_can_add_card():
    catalog = LocalCatalog()
    card = CardDefinition(definition_id="001", name="Test Card")
    
    catalog.add_card(card)
    retrieved_card = catalog.get_by_name("Test Card")
    assert retrieved_card is card

#test get a card that does not exist
def test_local_catalog_get_by_name_raises_error_for_nonexistent_card():
    catalog = LocalCatalog()
    with pytest.raises(ValueError):
        catalog.get_by_name("Nonexistent Card")
        
#test get a card that does exist
def test_local_catalog_get_by_name_returns_card():
    catalog = LocalCatalog()
    card = CardDefinition(definition_id="002", name="Existing Card")
    catalog.add_card(card)
    
    retrieved_card = catalog.get_by_name("Existing Card")
    assert retrieved_card is card