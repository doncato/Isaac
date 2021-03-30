# bot.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 27/01/20
bot_ver = '2.4.4'
ver_rel = '30/03/21'

#

# General Imports:
import os,sys,inspect,logging
# Discord and standard stuff
import importlib,discord,random,datetime,math,time
# Needed to add two lists together
from operator import add
# Network, URL Handling and I/O Streams
import json,requests,io
# To load Keys from .env files
from dotenv import load_dotenv
# Further discord imports
from discord.ext import commands
from discord.utils import get

# Logger handler
from logging.handlers import RotatingFileHandler
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(filename=os.path.join(os.path.dirname(__file__),'src/isaac.log'), encoding='utf-8', mode='a', backupCount=2, maxBytes=5*1024*1024)
handler.setFormatter(logging.Formatter('%(asctime)s--%(levelname)s: %(message)s'))
logger.addHandler(handler)

# Receive discord API KEY from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_KEY')

# List of possible Command Prefixes
prefix = ['µ ','u ','Mu ',]
# ID of Bot owner
bot_id = 630793998516224010

# Setting up intents to make some precise guild/user checks
intents = discord.Intents.default()
intents.members = True
intents.dm_reactions = True
intents.presences = True
# Set the bot class together
bot = commands.Bot(command_prefix=prefix, intents=intents, owner_id=bot_id)

# The bot can show it's runtime, this is set as the startpoint
uptime = datetime.datetime.now().replace(microsecond=0)

class core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load(self):
        """
        (None) -> None

        Tries to (Re)Load all extensions that are python files and existent in a folder called 'extensions'.
        If the import fails at one file, no further files are imported
        """
        dir_list = os.path.join(os.path.dirname(__file__), 'extensions')
        files = os.listdir(dir_list)
        for f in files:
            fn = f.split('.')
            f_ = fn[0]
            if fn[-1] == 'py' and f != __file__.split('/')[-1]:
                if bot.extensions.get(f'extensions.{f_}') == None:
                    self.bot.load_extension(f'extensions.{f_}')
                else:
                    self.bot.reload_extension(f'extensions.{f_}')
    #'''
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        This block handles all errors that occur in any command (not events!) and sends a message in the chat.
        """
        if isinstance(error, commands.MissingPermissions):
            txt = (f'Seems like you have insufficient permissions\n//{error}//')
        elif isinstance(error, commands.CommandOnCooldown):
            txt = (f'Relax, I didn\'t think you were that impatient\n//Wait another {math.ceil(error.retry_after)} seconds//')
        else:
            txt = (f'Well that didn\' work, I got an Error msg for you tho...\n//{error}//')
        error_msg = embed=discord.Embed(title='Whoopsie UwU', color=(ctx.guild.get_member_named(str(bot.user))).color, description=txt)
        error_msg.set_footer(text='Are you experiencing bugs?\nPlease report them by using the bug command: µ bug <your bug here> or informing the bot owner\nFurther information: µ help bug')
        await ctx.send(embed=error_msg)
    #'''

    @commands.Cog.listener()
    async def on_ready(self):
        """
        This block changes the presence as soon as the bot is ready.
        """
        await self.bot.change_presence(status=discord.Status.dnd)
        #self.load()

    @commands.command(name='load', aliases=['reload', 'rl'], brief='Reload all extensions', help=\
        'This command (Re)Loads all python files that are in the extensions directory, if the operation succeeds, the bot reacts with a green check mark,\
        this is not done by default and has to be executed after a restart by the user')
    @commands.is_owner()
    async def reload(self, ctx):
        self.load()
        await ctx.message.add_reaction('✅')

   
    @commands.command(name='stat', aliases=['info', 'status', 'stats'], brief='Get Bot information')
    async def info(self, ctx):
        now = datetime.datetime.now().replace(microsecond=0)
        bot_member = ctx.guild.get_member_named(str(bot.user))
        message = discord.Embed(title='Infos:', color=bot_member.color, description=f'Latency: {round(bot.latency, 3)*1000} ms\nRuntime: {(now - uptime)}\nVer.: {bot_ver}\nVer. Rel.: {ver_rel}\n\nGitHub: https://github.com/doncato/Isaac')
        message.set_thumbnail(url=bot_member.avatar_url)
        message.set_footer(text=f'By {bot.get_user(bot.owner_id)}')
        await ctx.send(embed=message)

bot.add_cog(core(bot))

bot.run(TOKEN)