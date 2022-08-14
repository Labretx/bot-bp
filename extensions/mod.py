import hikari
import lightbulb
import datetime
from vol.data import mods

# Create Plugin
plugin = lightbulb.Plugin("Moderators")


# Checks if command user is a moderator
# mods can be set either as a variable or just the role ID of the moderator role
@lightbulb.Check
def check_author_is_mod(ctx: lightbulb.Context) -> bool:
    return ctx.author.id in mods

# Ban command, set to be used by moderators
@plugin.command()
@lightbulb.add_checks(check_author_is_mod)
@lightbulb.option("reason", "Reason for the ban", required=False)
@lightbulb.option("user", "The user to ban.", type=hikari.User)
@lightbulb.command("ban", "Ban a user from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def ban(ctx: lightbulb.SlashContext) -> None:
    """Ban a user from the server with an optional reason."""
    # Has to be used in a server
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    # Restriction so mods don't ban their asses
    if ctx.options.user.id in mods:
        await ctx.respond("You can't ban a moderator!")
        return

    # Create a deferred response as the ban may take longer than 3 seconds
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    # Perform the ban
    await ctx.app.rest.ban_user(ctx.guild_id, ctx.options.user.id, reason=ctx.options.reason or hikari.UNDEFINED)
    # Provide feedback to the moderator
    await ctx.respond(f"{ctx.options.user.mention} has been banned.\n**Reason:** {ctx.options.reason or 'No reason provided.'}")


# Purge command to mass delete up to 100 messages, mods only
@plugin.command()
@lightbulb.add_checks(check_author_is_mod)
@lightbulb.option("count", "The amount of messages to purge.", type=int, max_value=100, min_value=1)
# You may also use pass_options to pass the options directly to the function
@lightbulb.command("purge", "Purge a certain amount of messages from a channel.", pass_options=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx: lightbulb.SlashContext, count: int) -> None:
    """Purge a certain amount of messages from a channel."""
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    # Fetch messages that are not older than 14 days in the channel the command is invoked in
    # Messages older than 14 days cannot be deleted by bots, so this is a necessary precaution
    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at)
        .limit(count)
    )
    if messages:
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
        await ctx.respond(f"Purged {len(messages)} messages.")
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")


# Timeout command for mods only, minutes are used in this command
@plugin.command()
@lightbulb.add_checks(check_author_is_mod)
@lightbulb.option("reason", "Reason for the timeout", required=False)
@lightbulb.option("time", "Time in Minutes", type=int)
@lightbulb.option("user", "User to timeout", type=hikari.User)
@lightbulb.command("timeout", "Timeout a user")
@lightbulb.implements(lightbulb.SlashCommand)
async def timeout(ctx: lightbulb.SlashContext) -> None:
    """Timeout a member for the specified amount of minutes"""
    # Has to be used in a server
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return
    
    # Restriction so mods don't timeout their asses
    if ctx.options.user.id in mods:
        await ctx.respond("You can't timeout a moderator!")
        return

    timeout_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ctx.options.time)
    await ctx.app.rest.edit_member(ctx.guild_id, ctx.options.user.id, communication_disabled_until=timeout_time)
    await ctx.respond(f"{ctx.options.user.mention} has been timed out for **{ctx.options.time} minutes** by {ctx.author}\n**Reason:** {ctx.options.reason or 'No reason provided'}.")


# Kick command for mods
@plugin.command()
@lightbulb.add_checks(check_author_is_mod)
@lightbulb.option("reason", "Reason for the kick", required=False)
@lightbulb.option("user", "User to kick", type=hikari.User)
@lightbulb.command("kick", "Kick a user from the server")
@lightbulb.implements(lightbulb.SlashCommand)
async def kick(ctx: lightbulb.SlashContext) -> None:
    """Kick a user from the server"""
    # Has to be used in a server
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return
    
    # Restriction so mods don't kick their asses
    if ctx.options.user.id in mods:
        await ctx.respond("You can't kick a moderator!")
        return

    # Feedback in chat
    await ctx.app.rest.kick_user(ctx.guild_id, ctx.options.user.id)
    await ctx.respond(f"{ctx.options.user.mention} has been kicked from the server by {ctx.author}\n**Reason:** {ctx.options.reason or 'No reason provided'}.")


# Load/Unload function for debugging
def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)