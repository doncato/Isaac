# owner_mail.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 10/07/21

import os,discord,json
from discord.ext import commands
import extensions._utils as _utils

class mail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = os.path.join(os.path.dirname(__file__), '../settings.json')
        self.quick_reacts = {
            '✅': [0, 'The Bot-Owner has completed your submission, the bot will be improved soon!'],
            '🔇': [0, 'The Bot-Owner has declined your submission, make sure you have put enough information to your submission! Maybe the bug is also already known.'],
            '🔈': [1, 'The Bot-Owner has acknowledged your submission.\nPriority: Low'],
            '🔉': [2, 'The Bot-Owner has acknowledged your submission.\nPriority: Medium'],
            '🔊': [3, 'The Bot-Owner has acknowledged your submission.\nPriority: High'],
        }

    async def send_dm(self, recipient_id: int, message):
        user = self.bot.get_user(recipient_id)
        channel = user.dm_channel
        if channel == None:
            channel = await user.create_dm()
        return await channel.send(embed=message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id != self.bot.user.id:
            settings = _utils.load_settings()
            bugs = settings["bugs"]
            message = payload.message_id
            owner = self.bot.get_user(self.bot.owner_id)
            channel = owner.dm_channel
            if channel == None:
                channel = await owner.create_dm()

            entry = bugs.get(str(message))
            if entry != None:
                level = self.quick_reacts.get(payload.emoji.name)
                user = entry[0]
                if level != None:
                    msg = await channel.fetch_message(message)
                    if level[0] == 0:
                        bugs.pop(str(message))
                        await msg.delete()
                    else:
                        bugs[str(message)] = [user, level[0]]
                    with open(self.filepath, 'w') as f:
                        f.write(json.dumps(settings))
                    response = discord.Embed(title=f'Bug-Status-Update from {owner}', color=discord.Color.from_rgb(255,0,0), description=level[1])
                    response.set_thumbnail(url=owner.avatar_url)
                    await self.send_dm(user, response)
    
    @commands.command(name='buglist', brief='Show currently open bugs')
    @commands.is_owner()
    @commands.cooldown(1, '30')
    async def buglist(self, ctx):
        owner = self.bot.get_user(self.bot.owner_id)
        channel = owner.dm_channel
        if channel == None:
            channel = await owner.create_dm()
        bugs = _utils.load_settings()["bugs"]
        high = []
        medium = []
        low = []
        for b in bugs.keys():
            if bugs[b][1] == 3:
                high.append(b)
            elif bugs[b][1] == 2:
                medium.append(b)
            elif bugs[b][1] == 1:
                low.append(b)

        high_content = []
        for u in high:
            ms = await channel.fetch_message(u)
            high_content.append(ms.jump_url)
        med_content = []
        for u in medium:
            ms = await channel.fetch_message(u)
            med_content.append(ms.jump_url)
        low_content = []
        for u in high:
            ms = await channel.fetch_message(u)
            low_content.append(ms.jump_url)


        mess = discord.Embed(title='Currently known bugs', color=discord.Color.from_rgb(255, 0, 0), description='Isaac has the following known bugs:')
        mess.set_thumbnail(url=self.bot.user.avatar_url)
        if high_content == []:
            high_content = '.'
        if med_content == []:
            med_content = '.'
        if low_content == []:
            low_content = '.'
        mess.add_field(name='High Priority:', value='\n'.join(high_content), inline=False)
        mess.add_field(name='Medium Priority:', value='\n'.join(med_content), inline=False)
        mess.add_field(name='Low Priority:', value='\n'.join(low_content), inline=False)
        await ctx.send(embed=mess)

    @commands.command(name='bug', brief='Submit a bug', help=f'Submit a bug report to the bot developer, try to give as much information as possible! (Attachments and links within the Normal/Non-Nitro limits are possible)! (This will decrease the time of a fix!)')
    @commands.cooldown(1, '300')
    async def bug(self, ctx, *description):
        desc = ' '.join(description)        
        settings = _utils.load_settings()
        bugs = settings["bugs"]

        msg = discord.Embed(title=f'Bug!', color=discord.Color.from_rgb(255, 0, 0), description=f'You have a new bug submitted by *{ctx.author}*!')
        msg.set_thumbnail(url=ctx.author.avatar_url)
        msg.add_field(name='Description:', value=desc)
        attaches = []
        for a in ctx.message.attachments:
            attaches.append(a.url)
        if attaches != []:
            attachments = '\n'.join(attaches)
        else:
            attachments = None
        msg.add_field(name='Attachments:', value=attachments, inline=False)
        msg.set_footer(text='React below to set a quick response')
        
        bug = await self.send_dm(self.bot.owner_id, msg)
        bugs[str(bug.id)] = [ctx.author.id, None]
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(settings))

        for e in self.quick_reacts.keys():
            await bug.add_reaction(e)

        await ctx.message.add_reaction('✅')

def setup(bot):
    bot.remove_cog(mail)
    bot.add_cog(mail(bot))