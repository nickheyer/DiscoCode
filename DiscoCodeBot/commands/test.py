from DiscoCodeBot.base_command import Command
from DiscoCodeBot.managers.ui_manager import ListCommands
from DiscoCodeBot.registry import CommandRegistry

class TestCommand(Command):
    name = "test"
    aliases = ["test"]
    permissions = ["admin"]
    description = "Test that bot is recognizing commands."

    async def execute(self, message, ctx):
        raise Exception('TEST ERROR')