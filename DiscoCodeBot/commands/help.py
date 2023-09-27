from DiscoCodeBot.base_command import Command
from DiscoCodeBot.managers.ui_manager import ListCommands
from DiscoCodeBot.registry import CommandRegistry

class HelpCommand(Command):
    name = "help"
    aliases = ["help"]
    permissions = ["user", "developer", "unregistered"]
    description = "Display all authorized commands."

    async def execute(self, message, ctx):
        registry = CommandRegistry()
        all_commands = registry.all()
        alts = registry.alts()
        commands = ListCommands(ctx, all_commands, alts)
        embed = await commands.generate_embed()
        await message.reply(embed=embed)