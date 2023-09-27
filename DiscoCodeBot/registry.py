import discord

class CommandRegistry:
    _instance = None

    def __new__(cls, tree=None):
        if not isinstance(cls._instance, cls):
            cls._instance = super(CommandRegistry, cls).__new__(cls)
            cls._instance.init(tree)
        return cls._instance

    def init(self, tree):
        self.commands = {}
        self.alt_commands = {}
        self.tree = tree

    def register(self, command_cls_list=[], alt=False):
        for command_cls in command_cls_list:
            command = command_cls
            print(f'REGISTERING COMMAND: {command.name}')

            for alias in command.aliases:
                print(f'REGISTERING ALIAS: {alias} / {command}')
                if not alt:
                    self.commands[alias] = command
                else:
                    self.alt_commands[alias] = command
              
            if command.slash_enabled:
                self._update_slash_command(command)

    def _update_slash_command(self, cmd):
        command = discord.app_commands.Command(
            name=cmd.name,
            description=cmd.description,
            callback=self.cb_factory(cmd.requires_input),
            guild_ids=None,
        )
        self.tree.add_command(command, override=True)

    def cb_factory(self, requires_input: bool):
        if requires_input:
            async def stub_callback_with_arg(interaction: discord.Interaction, input: str):
                pass
            return stub_callback_with_arg
        else:
            async def stub_callback(interaction: discord.Interaction):
                pass
            return stub_callback

    def get(self, name):
        command = self.commands.get(name)
        if not command:
            command = self.alt_commands.get(name)
        return command

    def all(self):
        if not self.commands:
            return []
        commands_ret = self.commands.values()
        return list(set(commands_ret))
    
    def alts(self):
        if not self.alt_commands:
            return []
        commands_ret = self.alt_commands.values()
        return list(set(commands_ret))