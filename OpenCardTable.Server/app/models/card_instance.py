from pydantic import BaseModel, Field
from app.models.card_definition import CardDefinition


class CardInstance(BaseModel):
    instance_id: str = Field(min_length=1)
    definition: CardDefinition
    owner_id: str = Field(min_length=1)
    controller_id: str = Field(min_length=1)
    tapped: bool = False

    def tap(self) -> None:
        self.tapped = True

    def untap(self) -> None:
        self.tapped = False




