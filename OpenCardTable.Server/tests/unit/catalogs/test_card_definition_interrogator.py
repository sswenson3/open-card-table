import pytest

from app.catalogs.card_definition_interrogator import CardDefinitionInterrogator

def test_card_definition_interrogator_can_be_instantiated():
    interrogator = CardDefinitionInterrogator()
    assert isinstance(interrogator, CardDefinitionInterrogator)

def test_card_definition_interrogator_load_fields():
    interrogator = CardDefinitionInterrogator()
    filename = "./OpenCardTable.Server/tests/unit/catalogs/test_data/mtg_template.json"
    interrogator.load_fields(filename)


    
    assert isinstance(interrogator._fields, dict)
    fields = interrogator.get_fields()
    assert "name" in fields
    assert "mana_cost" in fields
    assert "type_line"in fields
    assert "oracle_text" in fields
    assert "image_url" in fields