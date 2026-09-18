


class MTGCardDefinitionInterrogator:
    """
    This class is a data container for interrogating a Magic: The Gathering card definition. It 
    provides methods and data for getting field data from a user interface. 
    """
    _fields = {}

    def __init__(self, card_definition):
        pass

    def get_fields(self):
        return self._fields

    def add_field( self, field_name:str, field_value:str):
        self._fields.append((field_name)
    
    def load_fields( self, filename:str ):
        pass
        
    def interrogate(self):
        # Implement logic to interrogate the card definition
        # For example, extract relevant information from the card definition
        # and return it in a structured format.
        pass
