# event_listener.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 10/07/21

import os,discord,random,time
from discord.ext import commands
import _utils

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = os.path.join(os.path.dirname(__file__), '../settings.json')
        self.greek_alphabet = ['Alpha','Beta','Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Check if the user is connected to a vc first
        if after.voice == None:
            return
        # If user was online and is offline or idle now...
        if (before.status == discord.Status.online or before.status == discord.Status.dnd) and (after.status == discord.Status.offline or after.status == discord.Status.idle):
            # ...and not already muted...
            if not after.voice.mute:
                # ...mute that user
                await after.edit(mute=True, reason="User not active")

        # If user was offline or idle and is online or dnd now...
        elif (before.status == discord.Status.offline or before.status == discord.Status.idle) and (after.status == discord.Status.online or after.status == discord.Status.dnd):
            # ...check* who was the one muting the user...
            async for e in after.guild.audit_logs(limit=250, action=discord.AuditLogAction.member_update):
                if e.target == after and e.after.mute:
                    # ...if it was the bot itself unmute him
                    if e.user.id == self.bot.user.id:
                        await after.edit(mute=False, reason="User active again")
                    break

        # *The check is implemented to avoid a user being muted by a mod being able to unmute himself, by changing his presence from on>idle>on

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        channel = guild.system_channel
        send_welcome = _utils.load_settings()['settings']["send_ban_msg"]
        send = str(send_welcome.get(str(guild.id)))
        if str(send) != "." and send != None:
            await channel.send(embed=discord.Embed(title=f'{user.name} got Banned!', color=discord.Color.blue(), description=send))
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        channel = guild.system_channel
        send_welcome = _utils.load_settings()['settings']["send_unban_msg"]
        send = send_welcome.get(str(guild.id))
        if str(send) != "." and send != None:
            await channel.send(embed=discord.Embed(title=f'{user.name} got Unbanned', color=discord.Color.blue(), description=send))
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Send welcome Message
        channel = member.guild.system_channel
        send_welcome = _utils.load_settings()['settings']["send_welcome_msg"]
        count_channel = _utils.load_settings()['settings']["member_count_channel_id"]
        send = send_welcome.get(str(member.guild.id))
        count = count_channel.get(str(member.guild.id))
        if str(send) != "." and send != None:
            await channel.send(embed=discord.Embed(title=f'{member.name} just joined!', color=discord.Color.blue(), description=send))
        # Member counter
        if str(count) != "." and count != None and not member.bot:
            try:
                id = int(count)
            except:
                pass
            else:
                await _utils.change_trailing_channel_num(member.guild, id)
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Member counter
        count_channel = _utils.load_settings()['settings']["member_count_channel_id"]
        count = count_channel.get(str(member.guild.id))
        if str(count) != "." and count != None and not member.bot:
            try:
                id = int(count)
            except:
                pass
            else:
                await _utils.change_trailing_channel_num(member.guild, id, False)

    # Autoroles, will check settings and try to add a role upon a reaction by the user on set message.
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member != self.bot.user:
            settings = _utils.load_settings()["autoroles"].get(str(payload.guild_id))
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
            settings = _utils.load_settings()["autoroles"].get(str(payload.guild_id))
            if settings != None:
                emoji = settings.get(str(payload.message_id))
                if emoji != None:
                    role = emoji.get(payload.emoji.name)
                    if role != None:
                        role_id = int(role.replace('<','').replace('>','').replace('@','').replace('&',''))
                        role_ = self.bot.get_guild(payload.guild_id).get_role(role_id)
                        await user.remove_roles(role_)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Control the bitrate for VC management
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
            # When a member joins a new voice channel, and didn't move
            if before.channel is None and after.channel != None:
                count_channel = _utils.load_settings()['settings']["voice_count_channel_id"]
                count = count_channel.get(str(member.guild.id))
                if str(count) != "." and count != None and not member.bot:
                    try:
                        id = int(count)
                    except:
                        pass
                    else:
                        await _utils.change_trailing_channel_num(member.guild, id)
                
            # When a member leaves a voice channel
            if after.channel is None and before.channel != None:
                count_channel = _utils.load_settings()['settings']["voice_count_channel_id"]
                count = count_channel.get(str(member.guild.id))
                if str(count) != "." and count != None and not member.bot:
                    try:
                        id = int(count)
                    except:
                        pass
                    else:
                        await _utils.change_trailing_channel_num(member.guild, id, False)

def setup(bot):
    bot.remove_cog(events)
    bot.add_cog(events(bot))
