from pydantic import BaseModel, Field
from app.models.card_instance import CardInstance
from app.game.zone import Zone

class ZoneContainer(BaseModel):
    # Ordering convention:
    # cards[0] is the top/front of the zone.
    # cards[-1] is the bottom/back of the zone.
    # note operations at the end of a list are O(1), but we can flip our convention later if needed.
    zone: Zone
    
    #player_id = "player-001"
    # indicates player-scoped zone
    #player_id = None
    # indicates shared/global zone

    #player_id:str|None = None

    cards: list[CardInstance] = Field(default_factory=list)




