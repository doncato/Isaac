# command_system.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 10/07/21

import os,discord,json
import _utils
from discord.ext import commands


class system(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = os.path.join(os.path.dirname(__file__), '../settings.json')
        self.docpath = os.path.join(os.path.dirname(__file__), '../src/docs.md')
        self.logpath = os.path.join(os.path.dirname(__file__), '../src/isaac.log')
    
    @commands.command(name='autoroles', brief='Set autoroles for the server!')
    @commands.has_permissions(administrator=True)
    async def autoroles(self, ctx, action="show", message_id=0, emoji='', role_id=0, channel_id=0):
        og_set = _utils.load_settings()
        settings = og_set['autoroles']

        if action.lower() == "show":
            stringify = []
            if settings.get(str(ctx.guild.id)) != None:
                for m_id in settings[str(ctx.guild.id)].keys():
                    for emoji in settings[str(ctx.guild.id)][m_id].keys():
                        stringify.append(f'{m_id}: {emoji} -> {settings[str(ctx.guild.id)][m_id][emoji]}')
                await ctx.send(embed=discord.Embed(title='Autoroles Settings', color=(ctx.guild.get_member_named(str(self.bot.user))).color, description="\n".join(stringify)))
            else:
                await ctx.send(embed=discord.Embed(title='Autoroles', color=(ctx.guild.get_member_named(str(self.bot.user))).color, description="n/a"))

        elif action.lower() == "add":
            if settings.get(str(ctx.guild.id)) == None:
                settings.update({str(ctx.guild.id): {}})
            local_settings = settings.get(str(ctx.guild.id))

            if local_settings.get(str(message_id)) != None:
                local_settings[str(message_id)][str(emoji)] = str(role_id)
            else:                
                local_settings.update({str(message_id): {str(emoji): str(role_id)}})

            with open(self.filepath, 'w') as f:
                f.write(json.dumps(og_set))

            msg = await ctx.guild.get_channel(channel_id).fetch_message(message_id)
            try:
                await msg.add_reaction(emoji)
            finally:
                await ctx.message.add_reaction('✅')

        elif action.lower().startswith("rem") or action.lower().startswith("del"):
            if settings.get(str(message_id)) != None:
                if settings[str(message_id)].get(str(emoji)) != None:
                    settings[str(message_id)].pop(str(emoji))
                    
                    with open(self.filepath, 'w') as f:
                        f.write(json.dumps(og_set))
                    await ctx.message.add_reaction('✅')
                else:
                    await ctx.message.add_reaction('❌')
            else:
                await ctx.message.add_reaction('❌')

    @commands.command(name='manager_vc', brief='Returns a help for vc management')
    async def vcmanage(self, ctx):
        await ctx.send(embed=discord.Embed(title='Voice Channels', color=(ctx.guild.get_member_named(str(self.bot.user))).color, description='The bot can create and delete voice chats automatically. Voice chats that start with \'µ\' in their name will spawn a new vc on connection by a user, and move that user in that vc. Channels that end with \'µ\' are mainly used by the bot, and mark temporary channels, which will be deleted if all users left. Note: The Create-vc channel has to have a userlimit between 1 and 3 (enpoints included)'))

    @commands.command(name="refresh-counter", brief="Refresh the member and voice state counter")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 30)
    async def refresh(self, ctx):
        voice_count_channel = _utils.load_settings()['settings']["voice_count_channel_id"]
        member_count_channel = _utils.load_settings()['settings']["member_count_channel_id"]
        voice_count = voice_count_channel.get(str(ctx.guild.id))
        member_count = member_count_channel.get(str(ctx.guild.id))
        c = 0
        v = 0
        for m in ctx.guild.members:
            if not m.bot:
                c += 1
            if m.voice is not None:
                v += 1
        if str(voice_count) != "." and voice_count != None:
            try:
                v_id = int(voice_count)
            except:
                pass
            else:
                _utils.edit_trailing_channel_num(ctx.guild, v_id, v)
        if str(member_count) != "." and member_count != None:
            try:
                m_id = int(member_count)
            except:
                pass
            else:
                _utils.edit_trailing_channel_num(ctx.guild, m_id, c)
    
    @commands.command(name='set', brief='Set a setting for the settings', help='By leaving fields empty you can get the current settings')
    @commands.has_permissions(administrator=True)
    async def setting(self, ctx, setting=None, value=None):
        txt = None
        settings = _utils.load_settings()
        option = settings["settings"].get(setting)
        if setting == None:
            txt = f'Available settings are:\n{", ".join(settings["settings"].keys())}'
        elif option == None:
            txt = 'Setting not found!'
        elif value == None:
            txt = f'Current setting on this server is: {option.get(str(ctx.guild.id))}'
        else:
            option[str(ctx.guild.id)] = value
            with open(self.filepath, 'w') as f:
                f.write(json.dumps(settings))
            await ctx.message.add_reaction('✅')
        if txt != None:
            await ctx.send(embed=discord.Embed(title='Settings', color=(ctx.guild.get_member_named(str(self.bot.user))).color, description=txt))

    @commands.command(name='get-docs', brief='Retreive the documentation for Isaac')
    @commands.cooldown(1, 300)
    async def docs(self, ctx):
        await ctx.send(file=discord.File(self.docpath))

    @commands.command(name='get-logs', brief='Retreive the log file of Isaac')
    @commands.is_owner()
    @commands.cooldown(1, 30)
    async def logs(self, ctx):
        await ctx.send(file=discord.File(self.logpath))

class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='mu', aliases=['mute'], brief='Server Mute a user', help='Toggle server mute for each user mentioned, and for each rolemember of a mentioned role')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(3, 10)
    async def mu(self, ctx, *users):
        member = ctx.message.mentions
        roles = ctx.message.role_mentions
        if len(member) == 0 and len(roles) == 0:
            raise discord.InvalidArgument('No Users provided')
        else:
            for r in roles:
                for u in r.members:
                    member.append(u)
            for m in member:
                if m == None:
                    continue
                elif m.voice.mute:
                    await m.edit(mute=False, reason=f'Request for unmute by {ctx.author}')
                else:
                    await m.edit(mute=True, reason=f'Request for mute by {ctx.author}')

    @commands.command(name='de', aliases=['deaf'], brief='Server Deaf a user', help='Toggle server deaf for each user mentioned, and for each rolemember of a mentioned role')
    @commands.has_permissions(administrator=True)
    @commands.cooldown(3, 10)
    async def de(self, ctx, *users):
        member = ctx.message.mentions
        roles = ctx.message.role_mentions
        if len(member) == 0 and len(roles) == 0:
            raise discord.InvalidArgument('No Users provided')
        else:
            for r in roles:
                for u in r.members:
                    member.append(u)
            for m in member:
                if m == None:
                    continue
                elif m.voice.deaf:
                    await m.edit(deafen=False, reason=f'Request for un-deaf by {ctx.author}')
                else:
                    await m.edit(deafen=True, reason=f'Request for deaf by {ctx.author}')

def setup(bot):
    bot.remove_cog(system)
    bot.remove_cog(admin)
    bot.add_cog(system(bot))
    bot.add_cog(admin(bot))