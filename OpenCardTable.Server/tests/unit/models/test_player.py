import pytest
from pydantic import ValidationError
from app.models.player import Player

def test_player_requires_player_id():
    with pytest.raises(ValidationError):
        Player(display_name="Clockwork Griffin")

def test_player_requires_display_name():
    with pytest.raises(ValidationError):
        Player(player_id ="Clockwork Griffin001")

def test_player_can_be_created():
    player = Player(
        player_id="player-001",
        display_name="Clockwork Griffin",
    )

    assert player.player_id == "player-001"
    assert player.display_name == "Clockwork Griffin"

def test_player_rejects_empty_display_name():
    with pytest.raises(ValidationError):
        Player(
            player_id="fictional-card-001",
            display_name="",
        )

def test_player_rejects_empty_player_id():
    with pytest.raises(ValidationError):
        Player(
            player_id="",
            display_name="fictional-player",
        )