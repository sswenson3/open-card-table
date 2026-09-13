import pytest
from pydantic import ValidationError

from app.game.zone_container import ZoneContainer
from app.game.zone import  Zone
from app.models.card_instance import CardInstance
from app.models.card_definition import CardDefinition


def test_zone_container_can_be_created():
    library = ZoneContainer(
        zone= Zone.LIBRARY, 
        cards=[],
    )
      
    
    assert library.zone == Zone.LIBRARY
    assert library.cards == []

def test_zone_container_rejects_invalid_zone():
    with pytest.raises(ValidationError):
        ZoneContainer(zone="not-a-zone")

def test_zone_container_can_hold_card_instance():
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )

    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id="player-001",
        controller_id="player-001",
    )

    library = ZoneContainer(
        zone=Zone.LIBRARY,
        cards=[card],
    )





    assert library.cards[0] is card

def test_zone_container_add_card():
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id="player-001",
        controller_id="player-001",
    )
    library = ZoneContainer(
        zone=Zone.LIBRARY,
        cards=[],
    )
    library.add_card(card)
    assert library.cards[0] is card

def test_zone_container_remove_card():
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id="player-001",
        controller_id="player-001",
    )
    library = ZoneContainer(
        zone=Zone.LIBRARY,
        cards=[],
    )
    library.add_card(card)
    library.remove_card(card)
    assert card not in library.cards

def test_zone_container_contains_card():
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id="player-001",
        controller_id="player-001",
    )
    library = ZoneContainer(
        zone=Zone.LIBRARY,
        cards=[],
    )
    library.add_card(card)
    assert library.contains(card) is True