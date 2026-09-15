import pytest
from pydantic import ValidationError
from app.game.game_state import GameState    
from app.models.card_definition import CardDefinition
from app.models.card_instance import CardInstance
from app.models.player import Player
from app.game.zone import Zone

#test resources 
def card_count(game_state):
        return sum (
            len(zone_container.cards)
            for zones in game_state.game_zones.values()
            for zone_container in zones.values()
        )

definition = CardDefinition(
        definition_id="definition-001",
        name="Clockwork Griffin",
    )

definition2 = CardDefinition(
        definition_id="definition-002",
        name="Clockwork Hypogriff",
    )
cards = []
for i in range (20):
    instance = CardInstance.new(
        
        definition=definition,
        owner_id="player-001",
        controller_id="player-001",
    )
    cards.append(instance)


player = Player(
    player_id="player-001",
    display_name="Alice",
)



#tests

def test_add_cards_to_player_library():
    game_state = GameState(players=[player])
    game_state.initialize_zones()

    instance_list = {}

    for card in cards:
        game_state.place_card(card, Zone.LIBRARY, player.player_id )
        instance_list[card.instance_id] = card
    
    #verify the card instances are unique
    assert len(instance_list) == len(cards)

    # Verify that the cards are in the player's library
    assert len(game_state.game_zones[player.player_id][Zone.LIBRARY].cards) == len(cards)

    # move one card to hand
    owner_before = cards[0].owner_id
    game_state.move_card(cards[0],Zone.HAND, player.player_id)

    # move another card to battlefield
    game_state.move_card(cards[1], Zone.BATTLEFIELD)

    # Verify that the cards are in the correct zones
    assert owner_before == game_state.get_card_owner(cards[0]).player_id
    assert game_state.game_zones[player.player_id][Zone.HAND].contains(cards[0])
    assert game_state.game_zones["shared"][Zone.BATTLEFIELD].contains(cards[1])

    #no lossses  
    assert len(cards) == card_count(game_state)

    game_state.tap_card(cards[1])
    assert game_state.is_tapped(cards[1]) is True
    
    #owner unchanged
    assert game_state.get_card_owner(cards[1]).player_id == owner_before


   