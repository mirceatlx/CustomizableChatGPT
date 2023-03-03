
import re
from typing import List

import openai
from personalities import *
from modules import *
from utils import *
from utils.token_counter import num_tokens_from_string

class ChatBot:
    def __init__(self, personality: Personality, modules: List[Module], key: str, ignore_warnings: bool = False):
        self.personality = personality
        self.modules = modules
        self.ignore_warnings = ignore_warnings
        self.reset_messages()
        openai.api_key = key
    
    def reset_messages(self):
        self.messages = [
            {
                "role": "system",
                "content": self.build_init_prompt()
            }
        ]

    def build_init_prompt(self) -> str:
        prompt = self.personality.get_prompt()
        for module in self.modules:
            prompt += module.get_prompt() + "\n\n"
        
        if not self.ignore_warnings:
            assert num_tokens_from_string(prompt) > 2048, "The prompt is too long. Please reduce the number of modules you are using."
        print(prompt)
        return prompt

    def calculate_length_of_history(self) -> int:
        length = 0
        for message in self.messages:
            length += num_tokens_from_string(message["content"])
        return length
    
    def answer(self, str : str, role: str = 'user', times: int = 10) -> str:
        if self.calculate_length_of_history() > 10_000:
            self.reset_messages()
        
        self.messages.append({"role": role, "content": str})
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)["choices"][0]["message"]["content"]
            self.messages.append({"role": 'assistant', "content": response})
            print("Response:", response)
            # it should match the regex \w+(.*?\)
            regex = re.compile(r"\w+\(.*?\)")

            # check if regex matches and if it does check for what module it is
            if regex.search(response) and times > 0:
                # get the module name
                query = regex.search(response).group(0)
                query_name = query.split("(")[0]
                query_value = query.split("(")[1][1:-2]
                # get the module
                module = next((module for module in self.modules if query_name in module.get_triggers()), None)

                # if the module exists, get the response
                if module:
                    print(module)
                    system_response = module.get_response(query_value)
                    print("System response:", system_response)
                    return self.answer(system_response, role="system", times=times-1)
                else:
                    print("Model tried to use model that was not found.")
            return response
        except Exception as e:
            print("Error occurred while responding to request:", e)
            return "I'm sorry, I don't know how to respond to that. Something went wrong."