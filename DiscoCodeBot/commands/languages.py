from DiscoCodeBot.base_command import Command
from DiscoCodeBot.managers.ui_manager import ListLanguages, PaginatedView
from DiscoCodeBot.registry import CommandRegistry

class LangCommand(Command):
    name = "lang"
    aliases = ["lang", "langs", "language", "languages"]
    permissions = ["user", "developer"]
    description = "Display all executable languages."

    async def execute(self, message, ctx):
        registry = CommandRegistry()
        alts = registry.alts()
        commands = ListLanguages(ctx, alts)
        embeds = await commands.generate_embeds()
        view = PaginatedView(ctx, embeds)
        await message.reply(embed=embeds[0], view=view)