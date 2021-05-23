# event_listener.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 10/07/21

import os,discord,json,random,time
from discord.ext import commands


class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = os.path.join(os.path.dirname(__file__), '../settings.json')
        self.greek_alphabet = ['Alpha','Beta','Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']

    def load_settings(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        return data

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = guild.system_channel
        send_welcome = self.load_settings()['settings']["send_ban_msg"]
        send = str(send_welcome.get(str(guild.id)))
        if str(send) != "." and send != None:
            await channel.send(embed=discord.Embed(title=f'{user.name} got Banned!', color=discord.Color.blue(), description=send))
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = guild.system_channel
        send_welcome = self.load_settings()['settings']["send_unban_msg"]
        send = send_welcome.get(str(guild.id))
        if str(send) != "." and send != None:
            await channel.send(embed=discord.Embed(title=f'{user.name} got Unbanned', color=discord.Color.blue(), description=send))
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        send_welcome = self.load_settings()['settings']["send_welcome_msg"]
        send = send_welcome.get(str(member.guild.id))
        if str(send) != "." and send != None:
            await channel.send(embed=discord.Embed(title=f'{member.name} just joined!', color=discord.Color.blue(), description=send))
    
    # Autoroles, will check settings and try to add a role upon a reaction by the user on set message.
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member != self.bot.user:
            settings = self.load_settings()["autoroles"].get(str(payload.guild_id))
            if settings != None:
                emoji = settings.get(str(payload.message_id))
                if emoji != None:
                    role = emoji.get(payload.emoji.name)
                    if role != None:
                        role_id = int(role.replace('<','').replace('>','').replace('@','').replace('&',''))
                        role_ = self.bot.get_guild(payload.guild_id).get_role(role_id)
                        await payload.member.add_roles(role_)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        user = await self.bot.get_guild(payload.guild_id).fetch_member(payload.user_id)
        if user != self.bot.user:
            settings = self.load_settings()["autoroles"].get(str(payload.guild_id))
            if settings != None:
                emoji = settings.get(str(payload.message_id))
                if emoji != None:
                    role = emoji.get(payload.emoji.name)
                    if role != None:
                        role_id = int(role.replace('<','').replace('>','').replace('@','').replace('&',''))
                        role_ = self.bot.get_guild(payload.guild_id).get_role(role_id)
                        await user.remove_roles(role_)

    # Control the bitrate for VC management
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member != self.bot.user:
            if after.channel != None and after.channel.name.startswith('µ') and after.channel.user_limit <= 3 and after.channel.user_limit != 0:
                channel_name = None
                username = member.nick
                if username == None:
                    username = member.name
                for a in member.activities:
                    if type(a) == discord.activity.Activity or type(a) == discord.activity.Game:
                        channel_name = f'{a.name}-{username}-µ'
                        break
                if channel_name == None:
                    channel_name = f'{random.choice(self.greek_alphabet)}-{random.randint(10,99)}-{username}-µ'
                new_channel = await after.channel.clone(name=channel_name)
                await new_channel.edit(bitrate=8_000)
                await new_channel.edit(user_limit=0)
                await member.move_to(new_channel)          
            if after.channel != None and after.channel.name.endswith('µ'):
                if len(after.channel.members) > 1 and after.channel.bitrate < 56_000:
                    await after.channel.edit(bitrate=56_000)
            if before.channel != None and before.channel.name.endswith('µ'):
                if len(before.channel.members) == 0:
                    time.sleep(1)
                    await before.channel.delete()
                elif len(before.channel.members) == 1:
                    await before.channel.edit(bitrate=8_000)

def setup(bot):
    bot.remove_cog(events)
    bot.add_cog(events(bot))