import discord
import io
import json


from DiscoCodeClient.utils import (
    eval_user_roles,
    get_users_in_server,
    get_user
)

from DiscoCodeBot.managers.permission_manager import requires_admin


class ApproveNewUser(discord.ui.View):
    def __init__(self, context, response_object, auth_users, reason):
        self.context = context
        self.config = context.config
        super().__init__(timeout=self.config.session_timeout)
        self.response = response_object
        self.authorized_users = auth_users
        self.prompt = reason
        self.embed = None

    async def on_timeout(self) -> None:
        self.result = "TIMED_OUT"
        await self.generate_embed(timed_out=True)
        await self.reply.edit(embed=self.embed, view=None)
        return await super().on_timeout()

    @discord.ui.button(
        label="Register User",
        style=discord.ButtonStyle.blurple,
        custom_id="register_user",
        row=0,
    )
    async def register_user_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = "REGISTER_USER"
        await self.generate_embed(interaction)
        self.stop()

    @discord.ui.button(
        label="Deny", style=discord.ButtonStyle.gray, custom_id="deny", row=0
    )
    async def select_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = "DENIED"
        await self.generate_embed(interaction)
        self.stop()

    async def generate_embed(self, interaction=False, timed_out=False):
        if not self.authorized_users:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.brand_red()
            )
            embed.description = (
                "Authorization is required for this action, but no admin users exist in this server.\n\n"
                + "Please add/designate an admin user in the web-ui (where you started this bot).\n\n"
                + "If you continue to encounter errors like this, consider submitting a bug-report:\n\n"
                + "*Here*: https://discord.gg/wXs6z922VG\n*or*\n*Here*: https://github.com/nickheyer/DiscoCode/issues/new"
            )
            embed.url = "https://discord.gg/wXs6z922VG"
            self.clear_items()
            self.embed = embed
            self.result = False
            self.stop()
            return embed
        elif timed_out:
            embed = discord.Embed(
                title="Authorization Timed-Out", color=discord.Color.brand_red()
            )
            embed.description = "No responses provided, moving on."
            self.embed = embed
            return embed
        elif not interaction:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.dark_embed()
            )
            embed.description = self.prompt
            self.embed = embed
            return embed
        final_color = None
        final_title = None
        if self.result in ["DENIED"]:
            final_color = discord.Color.brand_red()
            final_title = "Authorization Denied"
        else:
            final_color = discord.Color.brand_green()
            final_title = "Authorization Granted"
        embed = discord.Embed(title=final_title, color=final_color)
        embed.description = (
            f"Decided By: {interaction.user.mention}\nOutcome: {self.result}"
        )
        await interaction.response.edit_message(embed=embed, view=None)

    async def send_response(self):
        await self.generate_embed()
        if self.authorized_users:
            self.reply = await self.response.channel.send(embed=self.embed, view=self)
            return await self.wait()
        self.reply = await self.response.channel.send(embed=self.embed)


class ApproveRequest(discord.ui.View):
    def __init__(self, context, response_object, reason, original_embed):
        self.context = context
        self.config = context.config
        super().__init__(timeout=self.config.session_timeout)
        self.response = response_object
        self.prompt = reason
        self.embed = None
        self.result = None
        self.original_embed = original_embed

    async def async_init(self):
        self.authorized_users = await self.get_admins(self.response)

    async def on_timeout(self) -> None:
        self.result = False
        timeout_embed = await self.generate_embed(timed_out=True)
        await self.response.edit(content=None, embed=timeout_embed, view=None)
        return await super().on_timeout()

    async def get_admins(self, message_object):
        users = await get_users_in_server(message_object.guild.id, ["admin"])
        discord_users = []
        for user in users:
            user = message_object.guild.get_member_named(user)
            if user:
                discord_users.append(user)
        return discord_users

    def get_admin_mentions(self):
        message_template = ""
        for user in self.authorized_users:
            message_template += f"{user.mention}\n"
        return message_template

    @discord.ui.button(
        label="Approve", style=discord.ButtonStyle.green, custom_id="approve", row=0
    )
    async def register_admin_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = True
        await interaction.response.edit_message(
            content=None, view=None, embed=self.original_embed
        )
        self.stop()

    @discord.ui.button(
        label="Deny", style=discord.ButtonStyle.red, custom_id="deny", row=0
    )
    async def select_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = False
        embed = discord.Embed(title="Request Denied", color=discord.Color.brand_red())
        embed.description = f"Decided By: {interaction.user.mention}\nOutcome: Denied"
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        self.stop()

    async def generate_embed(self, interaction=False, timed_out=False):
        if timed_out:
            embed = discord.Embed(
                title="Authorization Timed-Out", color=discord.Color.brand_red()
            )
            embed.description = "No responses provided, moving on."
            self.embed = embed
            return embed
        elif not self.authorized_users:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.brand_red()
            )
            embed.description = (
                "Authorization is required for this action, but no admin users exist in this server.\n\n"
                + "Please add/designate an admin user in the web-ui (where you started this bot).\n\n"
                + "If you continue to encounter errors like this, consider submitting a bug-report:\n\n"
                + "*Here*: https://discord.gg/wXs6z922VG\n*or*\n*Here*: https://github.com/nickheyer/DiscoCode/issues/new"
            )
            embed.url = "https://discord.gg/wXs6z922VG"
            self.clear_items()
            self.embed = embed
            self.result = False
            self.stop()
            return embed
        elif not interaction:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.dark_purple()
            )
            embed.description = self.prompt
            self.embed = embed
            return embed


class ListCommands:
    def __init__(self, context, command_classes, alt_classes):
        self.context = context
        self.config = context.config
        self.prefix = self.config.prefix_keyword
        self.response = context.message
        self.commands = command_classes
        self.alts = alt_classes
        self.user = context.message.author
        self.user_str = str(self.user)
        self.embed = None

    async def generate_embed(self):
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=self.user.color,
        )
        user_roles = set(await eval_user_roles(self.user_str))
        _debug = self.config.is_debug
        if _debug:
          print(f"THE CURRENT ROLES FOR THIS USER: {user_roles}")
          print(f"CURRENT COMANDS FROM CONTEXT: {self.commands}")
        for command_cls in self.commands:
            required_roles = set(command_cls.permissions)
            authorized_roles = required_roles.intersection(user_roles)
            
            if not required_roles or authorized_roles or _debug:
                name = command_cls.name
                aliases = "*, *".join(command_cls.aliases)
                usage = f"{command_cls.aliases[0]}" + (
                    " <input>" if command_cls.requires_input else ""
                )
                description = command_cls.description
                field_text = f"Description: `{description}`\n" if description else ""
                field_text += f"Usage: `{self.prefix} {usage}`"
                if command_cls.slash_enabled:
                    field_text += f"\nSlash: `/{usage}`"
                if _debug and (required_roles and not authorized_roles):
                    field_text += "\nAuthorization: `Not authorized`"
                elif _debug:
                    field_text += "\nAuthorization: `Authorized`"
                embed.add_field(
                    name=f"{name} [*{aliases}*]", value=field_text, inline=False
                )

        if self.alts:
            alt_text = f"Usage:\n```{self.config.alt_prefix}`​`​`<language-name>\n<code-to-execute>\n`​`​`​​\n```"
            embed.add_field(
              name="Code Execution", value=alt_text, inline=False
            )

            lang_text = ''
            for alt_cls in self.alts:
                lang_text += f"*{alt_cls.name}*: {'✔' if alt_cls.lang.is_enabled else '✖'}\n"
                print(alt_cls.name)

            embed.add_field(
                  name='Language Choices', value=lang_text, inline=False
            )

        if _debug:
            information_field = f'Username: `{self.user_str}`\nUser Roles: `{"`, `".join(user_roles)}`\nCommands Registered: `{len(self.commands)}`'
            embed.add_field(name="User Debug Information", value=information_field, inline=False)

        self.embed = embed
        return embed


class JSONButtonView(discord.ui.View):
    def __init__(self, output):
        super().__init__()
        self.output = output

    async def interaction_check(self, interaction: discord.Interaction):
        return True

    @discord.ui.button(label="Generate JSON", custom_id="json_generator")
    async def json_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        file = discord.File(fp=io.BytesIO(json.dumps(self.output, indent=4).encode()), filename="output.json")
        await interaction.response.send_message("Here is your JSON file:", file=file, ephemeral=True)

def trunc(out, max = 1000):
    length = len(out)
    if length > max:
        return f"{out[:max - 3]}..."
    else:
        return out

class ReadOutput:
    def __init__(self, context, output):
        self.context = context
        self.config = context.config
        self.response = context.message
        self.user = context.message.author
        self.output = output
        self.results = output.get('run')
        self.compile_results = output.get('compile', {})
        self.return_code = self.results.get('code', 0)
        self.embed = None

    async def generate_embed(self):
        if self.results.get("stderr"):
            embed_color = discord.Color.red()
        else:
            embed_color = discord.Color.green()

        embed = discord.Embed(
            title="Code Execution",
            description="Results of your code execution",
            color=embed_color,
        )

        embed.add_field(name='Language', value=f'```{self.output.get("language", "N/A")}```', inline=True)
        embed.add_field(name='Version', value=f'```{self.output.get("version", "N/A")}```', inline=True)
        
        if self.compile_results:
            compile_stderr = trunc(self.compile_results.get('stderr', '').strip())
            if compile_stderr:
                embed.add_field(name='Compile Errors/Warnings', value=f'```diff\n-{trunc(compile_stderr)}\n```', inline=False)
                
        if self.results.get("stderr"):
            embed.add_field(name='Run-time Error', value=f'```diff\n-{trunc(self.results.get("stderr", "Error Occurred"))}\n```', inline=False)
        if self.results.get("stdout"):
            embed.add_field(name='Output', value=f'```{trunc(self.results.get("stdout", "No results"))}```', inline=False)

        embed.set_footer(text=f'Requested by {self.user.name}', icon_url=self.user.display_avatar)

        self.embed = embed
        return embed