from DiscoCodeBot.base_command import Command

class TestCommand(Command):
    name = "test"
    permissions = ["owner", "developer"]
    aliases = ["test"]
    description = "Confirm bot is on and listening"

    async def execute(self, message, ctx):
        await message.channel.send('Testing!')