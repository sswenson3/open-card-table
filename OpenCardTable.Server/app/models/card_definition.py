from pydantic import BaseModel, Field

class CardDefinition(BaseModel):
    definition_id: str = Field(min_length=1)
    name: str = Field(min_length=1)





