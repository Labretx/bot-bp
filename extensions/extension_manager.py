import hikari
import lightbulb

# Create Plugin
plugin = lightbulb.Plugin("Extension_Manager")

# Load/Unload/Reload commands to do exactly that while the bot is running
# Set to be used by the owner of the bot only
# New extensions will be added to choices=[]
@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "the extension to be unloaded", type=str, required=True, choices=["errors"])
@lightbulb.command("unload", "unloads an extension")
@lightbulb.implements(lightbulb.SlashCommand)
async def unload_ext(ctx: lightbulb.SlashContext):
    plugin.bot.unload_extensions(f"extensions.{ctx.options.extension}")
    # Synchronizes slashcommands on unload
    await plugin.bot.sync_application_commands()
    await ctx.respond(f"The {ctx.options.extension} extension got unloaded", flags=hikari.MessageFlag.EPHEMERAL)


@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "the extension to be loaded", type=str, required=True, choices=["errors"])
@lightbulb.command("load", "loads an extension")
@lightbulb.implements(lightbulb.SlashCommand)
async def load_ext(ctx: lightbulb.SlashContext):
    plugin.bot.load_extensions(f"extensions.{ctx.options.extension}")
    await ctx.respond(f"The {ctx.options.extension} extension got loaded", flags=hikari.MessageFlag.EPHEMERAL)


@plugin.command()
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option("extension", "the extension to be reloaded", type=str, required=True, choices=["errors"])
@lightbulb.command("reload", "reloads an extension")
@lightbulb.implements(lightbulb.SlashCommand)
async def reload_ext(ctx: lightbulb.SlashContext):
    plugin.bot.reload_extensions(f"extensions.{ctx.options.extension}")
    # Synchronizes slashcommands on reload
    await plugin.bot.sync_application_commands()
    await ctx.respond(f"The {ctx.options.extension} extension got reloaded", flags=hikari.MessageFlag.EPHEMERAL)


# No unload function in this because then there is no point in having them everywhere
def load(bot):
    bot.add_plugin(plugin)