import pytest
from pydantic import ValidationError

from app.models.CardDefinition import CardDefinition


def test_card_definition_can_be_created():
    card = CardDefinition(
        definition_id="fictional-card-001",
        name="Clockwork Griffin",
    )

    assert card.definition_id == "fictional-card-001"
    assert card.name == "Clockwork Griffin"


def test_card_definition_requires_definition_id():
    with pytest.raises(ValidationError):
        CardDefinition(name="Clockwork Griffin")


def test_card_definition_requires_name():
    with pytest.raises(ValidationError):
        CardDefinition(definition_id="fictional-card-001")

def test_card_definition_rejects_empty_name():
    with pytest.raises(ValidationError):
        CardDefinition(
            definition_id="fictional-card-001",
            name="",
        )

