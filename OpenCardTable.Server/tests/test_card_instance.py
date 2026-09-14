import pytest
from pydantic import ValidationError
from app.models.card_instance import CardInstance
from app.models.card_definition import CardDefinition

#"global"  resources for tests
card_definition= CardDefinition(
    definition_id="fictional-card-001",
    name="Clockwork Griffin"
    )


def test_card_instance_requires_instance_id():
    with pytest.raises(ValidationError):
          CardInstance(
            definition = card_definition,
            owner_id="player-001",
            controller_id="player-001",
        
        )

def test_card_instance_requires_definition():
    with pytest.raises(ValidationError):
         CardInstance(
            instance_id="instance-001",
            
            owner_id="player-001",
            controller_id="player-001",
        
        )

def test_card_instance_requires_owner_id():
    with pytest.raises(ValidationError):
          CardInstance(
            instance_id="instance-001",
            definition = card_definition,
            controller_id="player-001",
        
        )

def test_card_instance_requires_controller_id():
    with pytest.raises(ValidationError):
         CardInstance(
            instance_id="instance-001",
            definition = card_definition,
            owner_id="player-001",
        
        )

def test_card_instance_can_be_created_tapped():
    card = CardInstance(
        instance_id="instance-001",
        definition = card_definition,
        owner_id="player-001",
        controller_id="player-001",
        
        tapped=True,
    )

    assert card.tapped is True

def test_card_instance_is_untapped_by_default():
    card = CardInstance(
        instance_id="instance-001",
        definition = card_definition,
        owner_id="player-001",
        controller_id="player-001",
        
    )

    assert card.tapped is False


def test_multiple_card_instances_can_share_one_definition():
    card1 = CardInstance(
        instance_id="instance-001",
        definition=card_definition,
        owner_id="player-001",
        controller_id="player-001",
    )

    card2 = CardInstance(
        instance_id="instance-002",
        definition=card_definition,
        owner_id="player-001",
        controller_id="player-001",
    )

    assert card1 is not card2
    assert card1.instance_id != card2.instance_id
    assert card1.definition is card2.definition

def test_card_instance_new_has_unique_ids():  
    cards = {} 
    for _ in range(1000):
       card = CardInstance.new(card_definition,"player-001","player-001")
       cards[card.instance_id] = card
    assert len(cards) == 1000
