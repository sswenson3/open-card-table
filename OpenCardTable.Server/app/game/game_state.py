
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field
from app.game.zone_container import ZoneContainer
from app.game.zone import Zone
from app.models.card_instance import CardInstance
from app.models.player import Player  

class GameState(BaseModel):
    # The game state is a collection of zones, each containing cards.
    # Each zone is represented by a ZoneContainer.
    game_zones: dict[str, dict[Zone, ZoneContainer]]
    players: list[Player]


    def __init__(self,  players=None, **data):
        super().__init__(
            players=players or [],
            **data
        )

    def initialize_zones(self):
        self.game_zones["shared"] = {
            Zone.BATTLEFIELD: ZoneContainer(zone=Zone.BATTLEFIELD),
            Zone.COMMAND: ZoneContainer(zone=Zone.COMMAND),
        }

        for player in self.players:
            self.game_zones[player.player_id] = {
                Zone.LIBRARY: ZoneContainer(zone=Zone.LIBRARY),
                Zone.HAND: ZoneContainer(zone=Zone.HAND),
                Zone.GRAVEYARD: ZoneContainer(zone=Zone.GRAVEYARD),
                Zone.EXILE: ZoneContainer(zone=Zone.EXILE),
            }

            



    # for each player create a ZoneContainer for each zone type (library, hand,  graveyard, exile)
    # battlefield would be a shared zone, not player specific.  
    # Command zone is also shared.

    # we don't yet have a deck class which presumably would be translated into a library, 
    # the player side would load the deck into their library.  This could be a library zone the
    # player can add cards to.  The library zone would be a ZoneContainer with a 
    # list of CardInstances.  
    # The player would have to provide the CardInstances to the server, 
    # which would then create the ZoneContainer for the library.  
    # The server would not create the CardInstances directly, 
    # but would use the provided data to create them.   

    # Gamestate will have a list of players, and will create each zone and assign to a player.
    # **data would contain deck information provided by players.  
    # Gamestate does not use CardDefinition directly. 

    def get_zone_of(self, card):
        # given a card instance, find which zone it is in
        for player_id, zones in self.game_zones.items():
            for zone, zone_container in zones.items():
                if card in zone_container.cards:
                    return player_id, zone
        return None

    def zone_is_shared(self, zone):
        return zone in self.game_zones["shared"]

    def get_card_owner(self,card):
        # given a card instance, find which player owns it
        for player in self.players:
            if card.owner_id == player.player_id:
                return player
        return None


    def  determine_target_scope (
            self,
            card,
            source_scope,
            target_zone,
            target_player_id=None
        ):

        if self.zone_is_shared(target_zone):
            return "shared"

        if target_player_id is not None:
            return target_player_id

        if source_scope != "shared":
            return source_scope

        return card.owner_id

    #move a card  from one zone to another, do not change owner.
    def move_card(self,card,target_zone, target_player_id=None):
        if card is None:
            raise ValueError("card cannot be None")

        location = self.get_zone_of(card)

        if location is None:
            raise ValueError("card is not in any zone")
 
        #scope is our collection key, it is a player_id or 'shared'
        source_scope, source_zone = location

        target_scope = self.determine_target_scope (
            card,
            source_scope,
            target_zone,
            target_player_id
        )

        source_container = self.game_zones[source_scope][source_zone]
        target_container = self.game_zones[target_scope][target_zone]

        # remove the card from the source container
        source_container.cards.remove(card)

        # add the card to the target container
        target_container.cards.append(card)


        return True
