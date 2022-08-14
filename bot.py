import imp
# Importing discord modules
from vol.data import token as t, bot_guilds as g
import hikari
import lightbulb
import miru

# Set intents
intents = hikari.Intents.ALL

# Create bot and pass in the token, servers and intents
# Load miru module into bot (for buttons and menues)
bot = lightbulb.BotApp(token=t, default_enabled_guilds=g, intents=intents)
miru.load(bot)

# Info when bot has started and is ready
@bot.listen(hikari.StartedEvent)
async def on_rdy(event):
    print("Bot is ready")


bot.run()