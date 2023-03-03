# A discord bot that uses ChatBot

import discord
from discord import app_commands
from dotenv import load_dotenv
from chat import ChatBot
from personalities import *
from modules import *
import asyncio
from threading import Thread

class DiscordBot():
    def __init__(self, chatbot: ChatBot, key: str, intents=discord.Intents.default()):
        super().__init__()
        self.chatbot = chatbot
        self.key = key
        self.intents = intents
        intents.message_content = True
        self.client = discord.Client(intents=self.intents)
        self.tree = app_commands.CommandTree(self.client)


        @self.tree.command(name="chat", description="Chat with Weldie")
        async def chat(interaction: discord.Interaction, string: str):
            await interaction.response.send_message(self.chatbot.answer(string))
                           
        @self.client.event
        async def on_ready():
            await self.tree.sync()
            print("Ready!")

    def run(self):
        Thread(target=lambda: self.client.run(self.key)).start()