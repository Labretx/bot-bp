import hikari
import lightbulb

# Create plugin/extension
plugin = lightbulb.Plugin("Errors")

# Error Handler for the bot
@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.SlashCommandErrorEvent) -> None:
    if isinstance(event.exception, lightbulb.errors.MaxConcurrencyLimitReached):
        await event.context.respond("You already have a session of this command running!", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.CommandIsOnCooldown):
        await event.context.respond("This command is currently on cooldown!", flags=hikari.MessageFlag.EPHEMERAL)
    elif isinstance(event.exception, lightbulb.errors.NotOwner):
        await event.context.respond("This command can only be used by the owner of the bot!", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await event.context.respond("Something didn't work as expected. Please contact the developer.", flags=hikari.MessageFlag.EPHEMERAL)
        raise event.exception

# load and unload functions for easy debugging while the bot is running
def load(bot):
    bot.add_plugin(plugin)


def unload(bot):
    bot.remove_plugin(plugin)