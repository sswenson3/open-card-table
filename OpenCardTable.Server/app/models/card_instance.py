from pydantic import BaseModel, Field


class CardInstance(BaseModel):
    instance_id: str = Field(min_length=1)
    definition_id: str = Field(min_length=1)
    owner_id: str = Field(min_length=1)
    controller_id: str = Field(min_length=1)
    tapped: bool = False

    def tap(self) -> None:
        self.tapped = True

    def untap(self) -> None:
        self.tapped = False




