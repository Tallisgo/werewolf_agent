<h1 style="font-family: 'Courier New', monospace; color: #ADD8E6;">Werewolf: Multi Agents</h1>




## Introduction

### what is werewolf
Werewolf is a game where the players are divided into two teams: the werewolves and the villagers. The werewolves are the bad guys and the villagers are the good guys. The werewolves want to kill the villagers and the villagers want to survive. Witch and seer have special powers.

Game is divided into two phases: day and night. In the day phase, the werewolves and the villagers can vote to kill a player. In the night phase, the werewolves and the villagers can use their special powers.

Note that not all messages are broadcasted to all players. For example, the werewolves can only see the werewolves.


### Advantages

This project implements the key components of the agent from scratch and helps you know internal principles of an agent. You only need to install `openai`.

1. what's the input and output of `openai`;

2. how to get structured output format from `openai`;




## Installion

* install `openai`

```bash
pip install openai
```



## Quick start

* prepare model configs in `config.yaml`\ `llm`, note that now only support openai api

you can choose `siliconflow` or any other company.


```python

name: "LLM name"  
model_name: "model name"  
api_key: "api key"  # API 密钥
base_url: "api endpoint"  
temperature: 0.8  
max_tokens: 150  
stream: False  
```




* start the game

```python
python main.py
```


## Next steps

* add user agent;

* add tools;

* design message class;



## References

1. [agentscope](https://github.com/modelscope/agentscope)

2. [siliconflow](https://cloud.siliconflow.cn/models)