from rich import print
from rich.text import Text
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Prompt
from openai import OpenAI
from pydantic import BaseModel

class Room(BaseModel):
    room_name: str    
    description: str    
    map_graphics: str
    user_action_prompt: str


def get_gpt_room(conversation_history):
    client = OpenAI()
            
    #print(conversation_history)
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=conversation_history,
        response_format=Room,
    )

    output = completion.choices[0].message.parsed
    
    output_dump = f"Room: {output.room_name}, Description: {output.description}, User Action Prompt: {output.user_action_prompt}"
    conversation_history.append({"role": "system", "content": output_dump})

    return output


def main():
    input_string = ""
    
    system_prompt = f"You are designing a text-based adventure video game system, in the style of an interactive fiction game. This is a sci-fi space based video game in the humorous style of the Hitchiker's Guide to the Galaxy and Space Quest, except with all new characters, settings and stories. You use a mix of Unicode and ASCII character-based graphicsto depict the room and its contents. You also write descriptions of the room and its contents in 3 sentences, and prompt the user with possible actions."

    
    conversation_history = []
    conversation_history.append({"role": "system", "content": system_prompt})
    
    user_prompt = f"Start game in a random location"
    conversation_history.append({"role": "user", "content": user_prompt})
    
    while True:
        room = get_gpt_room(conversation_history)
        
        game_map_str = room.map_graphics
        game_map = Text.from_ansi(game_map_str, justify="center")
                
        game_text_str = room.description + "\n\n"
        game_text_str += f"[bold]{room.user_action_prompt}[/]"
            
        game_text = Text.from_markup(game_text_str, justify="left")
        
        
        print()
        status_str = f"Health: 100 | {room.room_name}"
        print(Panel(status_str))
        
        
        cols = Columns([Panel(game_map), Panel(game_text)], equal=True)
        
        print(Panel(cols))

        name = Prompt.ask("[purple]>>> [/purple]")
        conversation_history.append({"role": "user", "content": name})



if __name__ == "__main__":
    main()
    