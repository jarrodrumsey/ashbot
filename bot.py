import discord
from command import BotCommands

class BotClient(discord.Client):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mapping of commands to functions
        command_module = BotCommands();
        self.commands = command_module.commands;

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        # Don't respond to messages sent by the bot itself
        if message.author == self.user:
            return
    
        for command, func in self.commands.items():
            if message.content.startswith(command):
                await func(message);
                break;


