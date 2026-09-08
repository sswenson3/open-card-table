import pytest
from pydantic import ValidationError
from app.models.card_instance import CardInstance
from app.game.zone import Zone

def test_card_instance_requires_instance_id():
    with pytest.raises(ValidationError):
          CardInstance(
            definition_id="definition-001",
            owner_id="player-001",
            controller_id="player-001",
            zone=Zone.LIBRARY,
        )

def test_card_instance_requires_definition_id():
    with pytest.raises(ValidationError):
         CardInstance(
            instance_id="instance-001",
            
            owner_id="player-001",
            controller_id="player-001",
            zone=Zone.LIBRARY,
        )

def test_card_instance_requires_owner_id():
    with pytest.raises(ValidationError):
          CardInstance(
            instance_id="instance-001",
            definition_id="definition-001",
            controller_id="player-001",
            zone=Zone.LIBRARY,
        )

def test_card_instance_requires_controller_id():
    with pytest.raises(ValidationError):
         CardInstance(
            instance_id="instance-001",
            definition_id="definition-001",
            owner_id="player-001",
            zone=Zone.LIBRARY,
        )

def test_card_instance_can_be_created_tapped():
    card = CardInstance(
        instance_id="instance-001",
        definition_id="fictional-card-001",
        owner_id="player-001",
        controller_id="player-001",
        zone=Zone.BATTLEFIELD,
        tapped=True,
    )

    assert card.tapped is True

def test_card_instance_is_untapped_by_default():
    card = CardInstance(
        instance_id="instance-001",
        definition_id="fictional-card-001",
        owner_id="player-001",
        controller_id="player-001",
        zone=Zone.BATTLEFIELD,
    )

    assert card.tapped is False