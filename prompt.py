
import json


class Prompts:
    
    """Prompts class"""
    
    to_wolves = (
        "{}, discuss with your teammates and reach an agreement to eliminate a player."
        # "Please response in json format:"
        # "\"thought\": \"your thought\", \"speak\": \"your speak\", \"finish_discussion\": \"whether the discussion reached an agreement or not (true/false)\""
        
    )
    
    to_only_wolves = (
        "{}, you are the only werewolf, think carefully and choose a player to eliminate"
    )
    
    instruction_prompt =  (
        "You should respond a json object similar to {} "
    )
    
    wolves_discussion_prompt = {
        "thought": "what you thought",
        "speak": "what you speak",
        "finish_discussion": "whether the discussion reached an agreement or not (true/false), if only one werewolf, set true",
    }
    
    to_wolves_vote = "The alive player are {}, which player do you vote to kill?"
    
    wolves_vote_prompt = {
        "thought": "what you thought",
        "vote": "player name",
    }
    
    to_wolves_res = "The player with the most votes is {}."

    to_witch_resurrect = (
        "{witch_name}, you're the witch. Tonight {dead_name} is eliminated. "
        "Would you like to resurrect {dead_name}?"
    )
    
    witch_healing_prompt = {
        "thought": "what you thought",
        "healing": "whether you want to healing or not (true/false)",
    }
    
    to_witch_resurrect_no = "The witch has chosen not to resurrect the player."
    to_witch_resurrect_yes = "The witch has chosen to resurrect the player."
    
    
    to_witch_poison = (
        "Would you like to eliminate one player? If yes, "
        "specify the player_name."
    )
    
    
    witch_poison_prompt = {
        "thought": "what you thought",
        "poison": "whether you want to poison or not (true/false)",
        "player_name": "player name",
    }
    
    to_witch_poison_no = "The witch has chosen not to eliminate a player."

    to_witch_poison_yes = "The witch has chosen to eliminate {}, {} is dead."
    
    
    to_seer = (
        "{}, you're the seer. Please choose a player from {} to check "
        "tonight?"
    )
    
    seer_check_prompt = {
        "thought": "what you thought",
        "player_name": "player name you want to check tonight",
    }
    
    
    to_all_danger = (
        "The day is coming, all the players open your eyes. Last night, "
        "the following player(s) has been eliminated: {}."
    )

    to_all_peace = (
        "The day is coming, all the players open your eyes. Last night is "
        "peaceful, no player is eliminated."
    )
    
    to_all_discuss = (
        "Now the alive players are {}. Given the game rules and your role, "
        "based on the situation and the information you gain, to vote a "
        "player eliminated among alive players and to win the game, what do "
        "you want to say to others? You can decide whether to reveal your "
        "role."
    )
    
    survivors_discuss_prompt = {
        "thought": "what you thought",
        "speak": "what you speak",
    }
    
    
    to_all_vote = (
        "Given the game rules and your role, based on the situation and the"
        " information you gain, to win the game, it's time to vote one player"
        " eliminated among the alive players. Which player do you vote to "
        "kill?"
    )
    
    
    survivors_vote_prompt = {
        "thought": "what you thought",
        "vote": "player name",
    }
    
    
    to_all_res = "{} has been voted out."

    to_all_wolf_win = (
        "The werewolves have prevailed and taken over the village. Better "
        "luck next time!"
    )

    to_all_village_win = (
        "The game is over. The werewolves have been defeated, and the village "
        "is safe once again!"
    )

    to_all_continue = "The game goes on."
