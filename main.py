'''
werewolf main code
'''

import random
import json
import os
from typing import List, Dict, Any

import yaml
from model import OpenAIChat
from agent import OpenaiBasedAgent
from configs.role_config import *
from prompt import Prompts
import logging
import numpy as np


roles = ["werewolf", "werewolf", "villager", "villager", "seer", "witch"]

# 设置一个字典存放玩家的信息
players_state = {}

healing, poison = True, True
MAX_WEREWOLF_DISCUSSION_ROUND = 3
MAX_GAME_ROUND = 6
    
# 读取yaml文件
def read_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

# 初始化角色 
def init_roles(roles, configs):

    # 初始化角色
    all_roles = roles.copy()
    random.shuffle(all_roles)
    

    # 初始化llm
    llm = configs['llm']
    
    players = configs['Players']
    # 分配角色
    wolves, villagers = [], []
   
    
    witch = None
    seer = None
    for i , role in enumerate(all_roles):
        # 获取角色的名字
        name = players["Player{}".format(i+1)]['name']
        
        
        # 实例化model
        model = eval(players["Player{}".format(i+1)]['model'])(**llm)
        
        system_prompt = eval(role + '_system_prompt').format(name)
        # 实例化agent
        agent = eval(players["Player{}".format(i+1)]['agent'])(name=name, role = role, system_prompt=system_prompt, model=model, state = True )
        players_state[name] = agent
        
        if role == 'werewolf':
            wolves.append(agent)
        
        else:
            if role == 'seer':
                seer = agent
            elif role == 'witch':
                witch = agent
            villagers.append(agent)    
            
    return villagers, wolves , witch, seer

def combine_name_to_string(agents):
    
    def _get_name(agent):
        return agent.name

    if len(agents) == 1:
        return _get_name(agents[0])
    
    return ', '.join([_get_name(agent) for agent in agents[:-1]]) + ' and ' + _get_name(agents[-1])

def check_alive_players(players_state):

    alive_agents =  [agent for player, agent in players_state.items() if agent.state]
    
    return combine_name_to_string(alive_agents)


def check_winning(wolves, players_state):
    
    alive_players =  [agent for player, agent in players_state.items() if agent.state]
    # 狼人获胜条件
    # 狼人的数量大于等于 villagers的数量
    if len(wolves) *2 >= len(alive_players):
        print("The werewolves have prevailed and taken over the village. Better luck next time!")
        return True
    
    if alive_players and len(wolves) == 0:
        print("The game is over. The werewolves have been defeated, and the village is safe once again! ")
        return True
    return False


def majority_vote(votes: list) -> Any:
    """majority_vote function"""
    votes_valid = [item for item in votes if item != "Abstain"]
    # Count the votes excluding abstentions.
    unit, counts = np.unique(votes_valid, return_counts=True)
    return unit[np.argmax(counts)]

configs = read_yaml_file('configs/config.yaml')

villagers, wolves, witch, seer = init_roles(roles, configs)


 
wolves_messages = []
witch_messages = []
seer_messages = []
day_messages = []

for name, agent in players_state.items():
    print("{}:{}".format(name, agent.role))


while True:
    user_input = input("Are you sure you want to continue? (yes/no):").strip().lower()
    if user_input in ["yes", "y"]:
        break
         
# start game
for _ in range(1, MAX_GAME_ROUND +1):
    
    # night werewolf discussion   
    
    # 根据wolves 数量 选择提示词
    alive_wolves = [ wolf  for wolf in wolves if wolf.state]
    # alive players name
    surviving_players = check_alive_players(players_state)
    
    moderator_to_wolves =  Prompts.to_wolves.format(combine_name_to_string(alive_wolves)) if len(alive_wolves) ==2 else Prompts.to_only_wolves(alive_wolves[0].name)
    
    wolves_messages.append( {'role': 'user', 'name': 'moderator', 'content': moderator_to_wolves } )
    
    instruction_discussion_message = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.wolves_discussion_prompt , indent=4) )} ]
    instruction_vote_message = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.wolves_vote_prompt, indent=4) )} ]
    
    # 开始狼人讨论 狼人讨论完判断是否得出结论
    discussion_over = False
    i = 0
    
    print('it is night:')
    while not discussion_over and i < MAX_WEREWOLF_DISCUSSION_ROUND:
    # for _ in range(MAX_WEREWOLF_DISCUSSION_ROUND):
        print(f"start werewolf discussion {i+1}")
        i +=1
        choose_player_to_dead = None
        
        for wolf in alive_wolves:
            response = wolf.reply(wolves_messages, instruction_discussion_message)['choices'][0]['message']['content'] 
            parsed_response = json.loads(response)
        
            print("{}: {}".format(wolf.name, parsed_response['speak']))
            wolves_messages.append({'role':'assistant', 'name': wolf.name, 'content': parsed_response['speak']})
            discussion_over = parsed_response.get('finish_discussion', False)
        
    # if parsed_response.get('finish_discussion', False):
    
    print("wolves vote time....")    
    # 达成一致， 开始讨论   
    moderator_night_vote = {'role': 'user', 'name':'moderator', 'content': Prompts.to_wolves_vote.format(surviving_players) }
    wolves_messages.append(moderator_night_vote)
    
    agreement = False
    while not agreement:
        for wolf in alive_wolves:
            response = wolf.reply(wolves_messages, instruction_vote_message)['choices'][0]['message']['content']
            parsed_response = json.loads(response)
            
            if choose_player_to_dead is None: 
                choose_player_to_dead = parsed_response['vote']
            elif choose_player_to_dead == parsed_response['vote']:
                agreement = True
    
        
    print('wolves decide to eliminate {}'.format(choose_player_to_dead) )
                       
    # 更新狼人和witch消息
    wolves_messages.append({'role':'user', 'name': 'moderator', 'content': Prompts.to_wolves_res.format(choose_player_to_dead)})
        #                     witch_messages.append( {'role':'user', 'name':'moderator', 'content': Prompts.to_witch_resurrect.format_map( { "witch_name":witch.name, "dead_name": choose_player_to_dead  }) } )
        #                     # 更新玩家状态
        #                     agreement = True
        #                     break
        #             else:
        #                 continue
        
        # else:
        #     continue
        
        # # print(_)
        # print(choose_player_to_dead)
        # if choose_player_to_dead:
        #     break
    
    # witch 使用毒药和解药
    # 需要知道女巫是哪一个
    # 1. healing
    print('--'*20)
    print(" witch time")
    poison_player = None
    if witch.state:
        # 本轮witch 发言
        round_message = None
        if healing and choose_player_to_dead is not None: 
            witch_messages.append( {'role':'user', 'name':'moderator', 'content': Prompts.to_witch_resurrect.format_map( { "witch_name":witch.name, "dead_name": choose_player_to_dead  }) } )
            instruction_heal_message = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.witch_healing_prompt, indent=4) )} ]
    #         print(instruction_heal_message)        
            response = witch.reply(witch_messages, instruction_heal_message)['choices'][0]['message']['content']
            
            parsed_response = json.loads(response)
            print("{}:{} ".format(witch.name, parsed_response) )
            if parsed_response.get('healing', False):
                # 使用解药
                healing = False
                choose_player_to_dead = None
                # 更新女巫消息
                round_message = {'role':'assistant', 'name': witch.name, 'content': Prompts.to_witch_resurrect_yes}
                
            else:
                # 不使用解药
                round_message = {'role':'assistant', 'name': witch.name, 'content': Prompts.to_witch_resurrect_no}
                
        if poison and healing:
            
            # 使用毒药
            instruction_poison_message = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.witch_poison_prompt, indent=4) )} ]
            response = witch.reply(witch_messages, instruction_poison_message)['choices'][0]['message']['content']
            
            parsed_response = json.loads(response)
            
            print("{}:{} ".format(witch.name, parsed_response) )
            if parsed_response.get('poison', False) and parsed_response.get('player_name', False):
                # 使用毒药
                poison = False
                poison_player = parsed_response['player_name']
                # 更新女巫消息
                round_message = {'role':'assistant', 'name': witch.name, 'content': Prompts.to_witch_poison_yes.format(parsed_response['player_name']) }

            else:
                round_message = {'role':'assistant', 'name': witch.name, 'content': Prompts.to_witch_poison_no}
        witch_messages.append(round_message)
    
    print('**'*20)
    print('seer time')
    if seer.state:
        # 预言家发言
        # 预言家会不会查看自己的信息
        seer_messages.append( {'role':'user', 'name':'moderator', 'content': Prompts.to_seer.format(seer.name, check_alive_players(players_state) ) } )
        instruction_seer_message = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.seer_check_prompt, indent=4) )} ]
        response = seer.reply(seer_messages, instruction_seer_message)['choices'][0]['message']['content'] 
        
        parsed_response = json.loads(response)
        
        print("{}:{} ".format(seer.name, parsed_response) )
        if parsed_response.get('player_name', False):
            
            check_player_role = players_state[parsed_response['player_name']].role
            
            seer_messages.append({'role':'assistant', 'name': seer.name, 'content': 'the role of {} is {}'.format(parsed_response['player_name'], check_player_role)})
            

    # update dead player 
    
    dead_player = []
    if choose_player_to_dead:
        players_state[choose_player_to_dead].state = False
        dead_player.append(choose_player_to_dead) 
    
    if poison_player:
        players_state[poison_player].state = False
        dead_player.append(poison_player)
    
    print('dead player:', dead_player)
    # 判断游戏是否结束
    if check_winning(wolves, players_state):
        break
    
    print('The day is coming.... ')
    # daytime discussion
    moderator_check_dead = {'role': 'user', 'name':'moderator', 'content': Prompts.to_all_danger.format(','.join(dead_player)) if len(dead_player) else Prompts.to_all_peace  }
    day_messages.append(moderator_check_dead)
    moderator_day_discussion = {'role': 'user', 'name':'moderator', 'content': Prompts.to_all_discuss }
    instruction_day_discussion = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.survivors_discuss_prompt, indent=4) )} ]
    
    # day_discussion = []
    print('**'*20)
    print('day discussion')
    for player , agent in players_state.items():
        if agent.state:
            
            response = agent.reply(day_messages, instruction_day_discussion)['choices'][0]['message']['content']
            parsed_response = json.loads(response)
            print("{}: {}".format(agent.name, parsed_response['speak']))
            day_messages.append({'role':'assistant', 'name': agent.name, 'content': parsed_response['speak']})
            
    
    # day vote
    day_messages.append({'role':'user', 'name':'moderator', 'content': Prompts.to_all_vote})
    instruction_day_vote = [{'role':'system', 'content':  Prompts.instruction_prompt.format(json.dumps( Prompts.survivors_vote_prompt, indent=4) )} ]

    day_vote = []
    for player , agent in players_state.items():
        if agent.state: 
            
            response = agent.reply(day_messages, instruction_day_vote)['choices'][0]['message']['content']

            parsed_response = json.loads(response)
            day_vote.append(parsed_response.get("vote", None))
                       
    vote_res = majority_vote(day_vote)
    
    players_state[vote_res].state = False
    print('{} gets the most votes'.format(vote_res))
                
    result = {'role':'user', 'name':'moderator', 'content': Prompts.to_all_res.format(vote_res) }            
    
    # result broadcast to all agents
    for player , agent in players_state.items():
        if agent.state: 
            agent.observe(result)
    
    if check_winning(wolves, players_state):
        break
    
    go_on_message = {'role': 'user', 'name':'moderator', 'content': Prompts.to_all_continue}  
    for player , agent in players_state.items():
        if agent.state: 
            agent.observe(result)
            agent.observe(go_on_message)
         
            
    
    
    

        
        
        
        
       
    
    
   