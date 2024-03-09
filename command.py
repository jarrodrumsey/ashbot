from translate import TranslateCommand
from kanban import KanbanModule
from rolls import RollsModule

class BotCommands:
      
    def __init__(self):         
        
        cSc = '!';   #   Command Start Character
        
        self.commands = {
            cSc+'hello': self.hello_command,
            cSc+'reminder': self.reminder_command,
            cSc+'poll': self.poll_command,
            cSc+'link': self.link_command,
            cSc+'translate': self.translate_command,
            cSc+'kanban': self.kanban_command,
            cSc+'roll': self.roll_command
        }
            
    # Define command functions (can also be moved to a separate module)
    async def hello_command(self, message):
        await message.channel.send('Hello!')

    async def reminder_command(self, message):
        await message.channel.send('Birthday!')

    async def poll_command(self, message):
        await message.channel.send('Poll added!')

    async def link_command(self, message):
        await message.channel.send('Retrieving links!')

    async def translate_command(self, message):

        translate_module = TranslateCommand();

        content = message.content.split();
        if len(content) < 3:
            await message.channel.send("Usage: `!translate @user [language]`");
            return
        
        _, user, language = content;
        
        if language.lower() not in translate_module.valid_languages:
            await message.channel.send("Given language was not found, please spell it correctly.");
            return
        
        await message.channel.send("Translating last message of user to provided language.");

    async def kanban_command(self, message):
        
        module = KanbanModule();
        
        module.execute(message)

        await message.channel.send('Kanban! - ' + message.content)

    # A command to make dice rolls and create preset rolls for use in real-world or online tabletop games.
    async def roll_command(self, message):
        
        module = RollsModule();
        
        output = module.execute(message)

        await message.channel.send(output)