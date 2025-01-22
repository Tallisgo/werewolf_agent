from typing import Any
from openai import OpenAI


class OpenAIChat:
    
    def __init__(self, api_key, base_url, model_name, temperature, max_tokens, stream,**kwargs ):
        
        """
        初始化 OpenAIchat 类
        
        :param api_key: OpenAI API 密钥
        :param model: 使用的模型类型，默认是 "gpt-3.5-turbo"
        :param temperature: 生成的随机性，默认为 0.7
        :param max_tokens: 最大生成的 token 数量，默认为 150
        """
        
        self.api_key = api_key
        self.base_url = base_url
        self.client = OpenAI(api_key=  self.api_key,
                             base_url= self.base_url,
                             )
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stream = stream
        
    
    
    def __call__(self, messages, **kwargs: Any):
        """
        实现可调用对象，用于调用 OpenAI API 进行聊天。

        :param messages: 包含聊天消息的列表。
        :param stream: 是否启用流式响应，默认为 None。
        :param kwargs: 其他可选参数。
        :return: OpenAI API 的响应。
        """
        # 将传入的关键字参数合并到 kwargs 中
        kwargs = {**kwargs}

        # 检查 messages 是否为列表类型
        if not isinstance(messages, list):
            # 如果不是列表类型，抛出异常
            raise ValueError(
                "OpenAI `messages` field expected type `list`,"
                f"got `{type(messages)}` instead."
            )

        
        # 更新 kwargs，添加模型名称、消息和流参数
        kwargs.update(
            {
                'model': self.model_name,
                "messages": messages,
                "response_format": {"type": "json_object"},
                # "stream": stream,
            }
        )

        # print(kwargs)
        # 调用 OpenAI API 进行聊天
        response = self.client.chat.completions.create(**kwargs)
        # response = self.client.chat.completions.create(
        #     model = self.model_name,
        #     messages = [{'role': 'system', 'content': 'you are a helpful assistant'}],
        #     temperature = self.temperature,
        #     max_tokens = self.max_tokens,
        # )

        # 将响应转换为字典格式并返回
        return response.model_dump()
    
    def format(self, messages):
        """
        格式化消息列表，将其转换为字符串格式。

        :param messages: 包含聊天消息的列表。
        :return: 格式化后的消息字符串。
        
         The following is an example:
        .. code-block:: python

            prompt1 = model.format(
                [
                    {'role': "system", "content": "You're a helpful assistant"},
                    {'role': "assistant", name: "Bob","content": "Hi, how can I help you?"),
                    {'role': "user", "content": "What's the date today?")
                ]
            )

        The prompt will be as follows:

        .. code-block:: python

            # prompt1
            [
                {
                    "role": "system",
                    "content": "You're a helpful assistant"
                },
                {
                    "role": "user",
                    "content": (
                        "## Conversation History\\n"
                        "Bob: Hi, how can I help you?\\n"
                        "user: What's the date today?"
                    )
                }
            ]



        """
        # 检查 messages 是否为列表类型
        if not isinstance(messages, list):
            # 如果不是列表类型，抛出异常    
            raise ValueError(
                "OpenAI `messages` field expected type `list`,"
                f"got `{type(messages)}` instead."
            )
        
        
        dialogue = []
        
        sys_prompt = None
        
        for i, unit in enumerate(messages):
            if unit['role'] == 'system':
                sys_prompt = unit['content']
                continue
            
            elif len(unit) ==3:
                dialogue.append(f"{unit['name']}: {unit['content']}")
            
            else:
                dialogue.append(f"{unit['role']}: {unit['content']}")

        content_components = []
        
        if len(dialogue) > 0:
            content_components.extend(["## Conversation History"] + dialogue)
        
        messages = [
            {
                "role": "user",
                "content" : "\n".join(content_components),
            },
        ]
        
        
        if sys_prompt is not None:
            messages.insert(0, {"role": "system", "content": sys_prompt})
        
        return messages
        
        