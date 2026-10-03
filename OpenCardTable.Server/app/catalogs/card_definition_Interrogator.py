import json


class CardDefinitionInterrogator:
    """
    This class is a data container for interrogating card definition. It 
    provides methods and data for loading a card definition game specific fields to 
    be interrogated in a user interface.

    These fields will  be used/added to a card definition object and stored in a card catalog.
    """
    _fields = {}

    def __init__(self):
        pass

    def get_fields(self):
        return self._fields["fields"] if "fields" in self._fields else []

    def add_field( self, field_name:str, field_value:str):
        self._fields.append(field_name)
    
    def load_fields( self, filename:str ):
        #loads fields from a file,  for example a json file,  and populates the _fields dictionary
        self._fields = json.load(open(filename))
        
  
