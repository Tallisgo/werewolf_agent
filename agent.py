'''
agent base class
'''
from typing import List, Dict, Any
from model import OpenAIChat

class OpenaiBasedAgent:
    def __init__(self, name, role,system_prompt: str, model: OpenAIChat, state):
        
        self.system_prompt = system_prompt
        self.name = name
        self.role = role
        self.model = model
        self.memory = []
        self.state = state
        

    def reply(self, message, instruction_message = None) -> str:
        
        # append message to memory
        # if message is str append
        # if message is list 追加
        
        
        if isinstance(message, list):
            self.memory.extend(message)
        if isinstance(message, str):
            self.memory.append(message)
        
        if self.system_prompt is None:
            prompt = []
        else:
            prompt = [{'role': 'system', 'content': self.system_prompt}]
        prompt.extend(self.model.format(
            self.memory)
        )
        
        if instruction_message:
            prompt.extend(instruction_message)
        
        # call llm 
        # if response not in format, call llm again until response in format
        raw_response = self.model(prompt)
        
        return raw_response
    
    
    
    def observe(self, x):
        
        if isinstance(x, str):
            self.memory.append(x)
        
        elif isinstance(x, list):
            self.memory.extend(x)