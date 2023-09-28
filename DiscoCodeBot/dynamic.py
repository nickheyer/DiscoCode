from DiscoCodeBot.base_command import Command
from DiscoCodeClient.models import Language
from DiscoCodeBot.managers.ui_manager import ReadOutput, OutputBtnView
from channels.db import database_sync_to_async
import requests
import json


@database_sync_to_async
def generate_commands():
    commands = []

    class LangCommand(Command):
        def __init__(self, lang) -> None:
            super().__init__()
            self.lang = lang
            self.name = lang.language
            self.aliases = lang.aliases
            self.requires_input = True
            self.slash_enabled = False
            self.permissions = ["user", "developer"]
            self.description = f"Execute {lang.language} code"
            self.conditions = []
            self.alt_prefix = True

        async def execute(self, message, ctx):
            lang = self.lang

            is_enabled = lang.is_enabled
            if not is_enabled:
                return

            code = ctx.primary

            url = ctx.config.exec_endpoint

            async with message.channel.typing():
              payload = json.dumps(
                  {
                      "language": self.name,
                      "version": lang.version,
                      "files": [{"content": code}],
                  }
              )

              headers = {"Content-Type": "application/json"}
              response = requests.request("POST", url, headers=headers, data=payload)
              resp_json = response.json()

              btn_view = OutputBtnView(ctx, resp_json)
              out_cls = ReadOutput(ctx, resp_json)
              embed = await out_cls.generate_embed()
              await message.reply(embed=embed, view=btn_view)

    for lang in Language.objects.all():
        commands.append(LangCommand(lang))

    return commands
