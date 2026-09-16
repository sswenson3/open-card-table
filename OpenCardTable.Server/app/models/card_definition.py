from pydantic import BaseModel, Field
import uuid

class CardDefinition(BaseModel):
    definition_id: str = Field(min_length=1)
    name: str = Field(min_length=1)

    @classmethod
    def new(cls, name:str ) -> "CardDefinition":
        return cls(
            definition_id=str(uuid.uuid4()),
            name=name
        )



