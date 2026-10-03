
from typing import List, Optional
from pydantic import BaseModel
from app.models.card_instance import CardInstance

class Deck(BaseModel):
    cards: List[CardInstance] = []

    def add(self, card: CardInstance) -> None:
        self.cards.append(card)

    def remove(self, card_id: str) -> bool:
        for i, card in enumerate(self.cards):
            if card.id == card_id:
                del self.cards[i]
                return True
        return False

    def find_card_by_name(self, name: str) -> List[CardInstance]:
        return [card for card in self.cards if card.name == name]

    def find_card_by_type(self, type_: str) -> List[CardInstance]:
        return [card for card in self.cards if card.type == type_]

    def find_card_by_cost(self, cost: str) -> List[CardInstance]:
        return [card for card in self.cards if card.cost == cost]

    def find_card_by_color(self, color: str) -> List[CardInstance]:
        return [card for card in self.cards if card.color == color]

    def find_card_by_rarity(self, rarity: str) -> List[CardInstance]:
        return [card for card in self.cards if card.rarity == rarity]
