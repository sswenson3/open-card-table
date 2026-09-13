import uuid
from pydantic import BaseModel, Field
from app.models.card_definition import CardDefinition



class CardInstance(BaseModel):
    instance_id: str = Field(min_length=1)
    definition: CardDefinition
    owner_id: str = Field(min_length=1)
    controller_id: str = Field(min_length=1)
    tapped: bool = False


    @classmethod
    def new(cls, definition: CardDefinition, owner_id: str, controller_id: str) -> "CardInstance":
        return cls(
            instance_id=str(uuid.uuid4()),
            definition=definition,
            owner_id=owner_id,
            controller_id=controller_id,
            tapped=False
        )

    def tap(self) -> None:
        self.tapped = True

    def untap(self) -> None:
        self.tapped = False




