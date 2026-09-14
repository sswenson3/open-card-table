import pytest
from pydantic import ValidationError
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from app.game.zone_container import ZoneContainer
from app.game.zone import Zone
from app.game.game_state import GameState
from app.models.card_definition import CardDefinition
from app.models.card_instance import CardInstance
from app.models.player import Player  

# helper functions
def card_count(game_state):
        return sum (
            len(zone_container.cards)
            for zones in game_state.game_zones.values()
            for zone_container in zones.values()
        )


# tests
# create gamestate
def test_game_state_can_be_created():
    player1 = Player(player_id="player-001", display_name="Alice")
    player2 = Player(player_id="player-002", display_name="Bob")
    game_state = GameState(players=[player1, player2], game_zones={})
    game_state.initialize_zones()
    assert len(game_state.players) == 2
    assert "shared" in game_state.game_zones
    assert player1.player_id in game_state.game_zones
    assert player2.player_id in game_state.game_zones


# create a card instance in a zone
def test_game_state_can_add_card_to_zone():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the player's library zone
    game_state.place_card(card,Zone.LIBRARY)
    # Verify that the card is in the library zone
    assert game_state.game_zones[player1.player_id][Zone.LIBRARY].cards[0] is card

# create a card instance in a zone
def test_game_state_can_find_card_zone():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the player's library zone
    # game_state.game_zones[player1.player_id][Zone.LIBRARY].cards.append(card)
    game_state.place_card(card,Zone.LIBRARY)

    # Verify that the card is in the library zone
    assert game_state.get_zone_of(card) == ("player-001",Zone.LIBRARY)

def test_move_card_player_to_player_same_scope():
 
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the player's library zone
    game_state.place_card(card,Zone.LIBRARY)

    card_count_before = card_count(game_state)

    # Move the card from library to hand
    game_state.move_card(card, Zone.HAND)
    card_count_after = card_count(game_state)

    #verify that the card is in the hand zone
    assert game_state.get_zone_of(card) == ("player-001",Zone.HAND)
    assert card_count_before == card_count_after
 

def test_move_card_player_to_shared():
    
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the player's library zone
    game_state.place_card(card,Zone.LIBRARY)
    card_count_before = card_count(game_state)

    game_state.move_card(card, Zone.BATTLEFIELD)
    card_count_after = card_count(game_state)

    
    assert game_state.get_zone_of(card) == ("shared",Zone.BATTLEFIELD)
    assert card_count_before == card_count_after
    assert card is game_state.game_zones["shared"][Zone.BATTLEFIELD].cards[0]

def test_move_card_shared_to_player():
   
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the BAttlefield  zone
    game_state.place_card(card,Zone.BATTLEFIELD,"shared")
    card_count_before = card_count(game_state)
    game_state.move_card(card, Zone.GRAVEYARD)
    card_count_after = card_count(game_state)

    assert game_state.get_zone_of(card) == (player1.player_id,Zone.GRAVEYARD)
    assert card is game_state.game_zones[player1.player_id][Zone.GRAVEYARD].cards[0]
    assert card_count_before == card_count_after


def test_move_card_player_to_different_player():
    
    player1 = Player(player_id="player-001", display_name="Alice")
    player2 = Player(player_id="player-002", display_name="Bob")
    game_state = GameState(players=[player1, player2], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the BAttlefield  zone
    game_state.place_card(card,Zone.BATTLEFIELD,"shared")
    card_count_before = card_count(game_state)
    game_state.move_card(card, Zone.GRAVEYARD,player2.player_id)
    card_count_after = card_count(game_state)
    assert game_state.get_zone_of(card) == (player2.player_id,Zone.GRAVEYARD)
    assert card is game_state.game_zones[player2.player_id][Zone.GRAVEYARD].cards[0]
    assert card_count_before == card_count_after



def test_move_card_shared_to_shared():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    # Add the card to the player's library zone
    game_state.place_card(card,Zone.BATTLEFIELD,"shared")

    game_state.move_card(card, Zone.COMMAND)

    assert game_state.get_zone_of(card) == ("shared",Zone.COMMAND)

def test_game_state_move_none_card_raises():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()

    with pytest.raises(ValueError):
        game_state.move_card(None, Zone.GRAVEYARD)

def test_game_state_move_card_not_in_any_zone_raises():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
    )
    
    with pytest.raises(ValueError):
        game_state.move_card(card, Zone.GRAVEYARD)


def test_game_state_can_tap_a_card():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
        tapped=False
    )
    # Add the card to the player's library zone
    game_state.place_card(card,Zone.LIBRARY)

    game_state.tap_card(card)

    assert card.tapped is True

def test_game_state_can_untap_a_card():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance(
        instance_id="instance-001",
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id,
        tapped=True
    )
    # Add the card to the player's library zone
    game_state.place_card(card,Zone.LIBRARY)

    game_state.untap_card(card)

    assert card.tapped is False


def test_game_state_place_card():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card instance
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card= CardInstance.new(
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id
        )
    instance = card.instance_id

    # Place the card into the player's library zone
    game_state.place_card(card,Zone.LIBRARY)
    # Verify that the card is in the library zone
    assert game_state.get_zone_of(card) == ("player-001",Zone.LIBRARY) and\
        game_state.game_zones[player1.player_id][Zone.LIBRARY].cards[0].instance_id == instance
    assert game_state.game_zones[player1.player_id][Zone.LIBRARY].cards[0] is card

def test_game_state_multiple_card_instances_are_unique():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card definition
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    # Create two card instances from the same definition
    card1 = CardInstance.new(
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id
        )
    card2 = CardInstance.new(
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id
        )
    # Place both cards into the player's library zone
    game_state.place_card(card1,Zone.LIBRARY)
    game_state.place_card(card2,Zone.LIBRARY)
    # Verify that both cards are in the library zone and have unique instance_ids
    assert game_state.get_zone_of(card1) == ("player-001",Zone.LIBRARY)
    assert game_state.get_zone_of(card2) == ("player-001",Zone.LIBRARY)
    assert card1.instance_id != card2.instance_id
    assert card1 is not card2
        
def test_game_state_card_instance_not_in_multiple_zones():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card definition
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    # Create a card instance
    card = CardInstance.new(
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id
        )
    # Place the card into the player's library zone
    game_state.place_card(card,Zone.LIBRARY)
    # Attempt to place the same card into the player's hand zone
    with pytest.raises(ValueError):

        game_state.place_card(card,Zone.HAND)

def test_game_state_card_owner_notchanged_by_move():
    player1 = Player(player_id="player-001", display_name="Alice")
    
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    # Create a card definition
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    # Create a card instance
    card = CardInstance.new(
        definition=definition,
        owner_id=player1.player_id,
        controller_id=player1.player_id
        )
    # Place the card into the player's library zone
    game_state.place_card(card,Zone.LIBRARY)
    owner_before = card.owner_id
    # Move the card to the battlefield (shared zone)
    game_state.move_card(card,Zone.BATTLEFIELD)
    assert card.owner_id == owner_before
    
def test_game_state_card_instance_not_in_multiple_zones():
    player1 = Player(player_id="player-001", display_name="Alice")
    game_state = GameState(players=[player1], game_zones={})
    game_state.initialize_zones()
    definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )
    card = CardInstance.new(
        
        definition=definition,
        owner_id="player-001",
        controller_id="player-001",
    )
    
    game_state.place_card(card, Zone.LIBRARY, player1.player_id)

    with pytest.raises(ValueError):
        game_state.place_card(card, Zone.HAND, player1.player_id)
    assert game_state.get_zone_of(card) == ("player-001", Zone.LIBRARY)
