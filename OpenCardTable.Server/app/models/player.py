from pydantic import BaseModel, Field

class Player(BaseModel):
    player_id:    str = Field(min_length=1)
    display_name: str = Field(min_length=1)





