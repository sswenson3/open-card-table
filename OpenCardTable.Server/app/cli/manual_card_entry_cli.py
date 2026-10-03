from app.catalogs.card_definition_interrogator import CardDefinitionInterrogator
from app.models.card_definition import CardDefinition

class ManualCardEntryCLI():
# interrogate a user based on a loaded remplate.   So arguments need a template file to 
# load and interrogate the user for the fields in that template.  
# The template file is a json file that contains a list of fields to be interrogated. 
#  The user will be prompted for each field and the values will be stored in a dictionary.  
# The dictionary will then be used to create a CardDefinition object.

  cards = list[CardDefinition] 
    
  def event_loop(self, template_file:str)-> CardDefinition:
    interrogator = CardDefinitionInterrogator()
    interrogator.load_fields(template_file)
    fields = interrogator.get_fields()
    card_data = {}

    # Prompt user to begin definintion of a new card or enter exit to end the loop.  
    quit = False
    while quit != True :
        input("Press enter to begin defining a new card, or type 'exit' to quit: ")
        if input.lower() == 'exit':
            quit = True
            break

        for field in fields:
            value = input(f"Enter value for {field}: ")
            card_data[field] = value
    card_definition = CardDefinition(**card_data)
    self.cards.append(card_definition)