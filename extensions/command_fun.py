# command_fun.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 10/07/21

import os,discord,json,time,random,requests
from datetime import datetime,timedelta
from discord.ext import commands

# Image glitcher
import glitch_this,io,requests
from PIL import Image

# API Keys
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.realpath('./'), '.env'))
API_Apex = os.getenv('API_APEX')
# Games



class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = os.path.join(os.path.dirname(__file__), '../settings.json')
        self.voice_lines = os.path.join(os.path.dirname(__file__), '../src/voice_lines.json')
        self.vc_default = 50

        self.latin_alphabet = ['a','b','c','d','e','f','g','h','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.greek_alphabet = ['Alpha','Beta','Gamma', 'Delta', 'Epsilon', 'Zeta', 'Eta', 'Theta', 'Iota', 'Kappa', 'Lambda', 'Mu', 'Nu', 'Xi', 'Omicron', 'Pi', 'Rho', 'Sigma', 'Tau', 'Upsilon', 'Phi', 'Chi', 'Psi', 'Omega']
        self.phonetic_alphabet = ['Alfa', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'India', 'Juliett', 'Kilo', 'Lima', 'Mike', 'November', 'Oscar', 'Papa', 'Quebec', 'Romeo', 'Sierra', 'Tango', 'Uniform', 'Victor', 'Whiskey', 'Xray', 'Yankee', 'Zulu']
        self.alphs = {'latin': self.latin_alphabet, 'greek': self.greek_alphabet, 'phonetic': self.phonetic_alphabet}

    def load_settings(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        return data

    @commands.command(name='judge', brief='judge a user', help='Get some basic information about a given user such as roles, nickname, ...')
    async def judge(self, ctx, *user):
        member = ctx.message.mentions
        
        if len(member) == 0:
            raise discord.InvalidArgument('I need a mentioned member to work with')

        elif member[0] == self.bot.user:
            await ctx.send(embed=discord.Embed(title='Nice Try', color=discord.Color.dark_blue(), description=f'What are you expecting?'))
        else:
            member = member[0]
            embed=discord.Embed(title=member.display_name, color=member.color, description='So first things first first, this is the profile picture, how cringe.')
            embed.set_thumbnail(url=member.avatar_url)
            if member.bot:
                bot_stat = 'Wait? That\'s a bot, why am I doing this?'
            else:
                bot_stat = 'Ah yes, this is human flesh'

            embed.add_field(name='Blood?', value=bot_stat)
            if member.display_name == member.name:
                name_stat = 'Oh simplicity I see, not even a unique nickname?'
            else:
                name_stat = 'We are so special aren\'t we? Just a general name wasn\'t enough but this one also needs another nickname.'
            name_stat = name_stat + f'\nBtw Discriminator is {member.discriminator}, how interesting'
            embed.add_field(name=f'{member.display_name} / {member.name}#{member.discriminator}', value=name_stat)

            flags_stat = []
            if member.public_flags.staff == True or member.public_flags.system == True:
                flags_stat.append('Wait, an actual Discord Staff? Those are rare ones!')
            if member.public_flags.hypesquad == True or member.public_flags.hypesquad_bravery == True or member.public_flags.hypesquad_brilliance == True or member.public_flags.hypesquad_balance == True:
                flags_stat.append('I found something…\nOhh wait this is just some hypesquad member so nothing special')
            if member.public_flags.verified_bot_developer:
                flags_stat.append('A verified bot developer, stay away from my code!')
            if member.public_flags.value == 0:
                flags_stat.append('Not a single flag in sight, thanks for making my job easy.')
            else:
                flags_stat.append('\nSo this user has the following flags:')
                flags_stat.append(', '.join(member.public_flags.all()))
            embed.add_field(name='Flags', value='\n'.join(flags_stat), inline=False)

            roles = []
            for r in member.roles:
                roles.append(r.name)
            roles_stat = f'Let\'s see if anyone cared enough to give this one roles...\n{", ".join(roles)}'
            embed.add_field(name='Roles', value=roles_stat, inline=False)

            await ctx.send(embed=embed)

    @commands.command(name='rename-madness', aliases=['rename'], brief='Rename every user', help=\
        'Give a couple of words, or different schemes to assign as nicknames for the server member\nPossible schemes are: reset[reset all names], binary, hexadecimal, fuck[you need to provide a word for that], latin-, greek- and phoenetic alphabet')
    @commands.cooldown(1, 60)
    @commands.has_permissions(manage_nicknames=True)
    async def rename(self, ctx, scheme='custom', *words):
        size = len(ctx.guild.members)
        if scheme.lower().startswith('cus'):
            if len(words) >= size:
                new_names = words
            else:
                raise discord.InvalidArgument('Too few words provided')
        elif scheme.lower().startswith('num'):
            new_names = []
            for i in range(1, size+1):
                new_names.append(str(i))
        elif scheme.lower().startswith('res'):
            new_names = []
            for i in range(1, size+1):
                new_names.append(None)
        elif scheme.lower().startswith('bin'):
            new_names = []
            for i in range(1, size+1):
                new_names.append(str(bin(i).replace('0b', '')))
        elif scheme.lower().startswith('hex'):
            new_names = []
            for i in range(1, size+1):
                new_names.append(str(hex(i).replace('0x', '')))
        elif scheme.lower().startswith('fuc'):
            new_names = []
            for i in range(1, size+1):
                new_names.append(str(words[0]*i))
        else:
            try:
                lib_list = self.alphs[scheme]
            except KeyError:
                raise discord.InvalidArgument('Couldn\'t get Scheme')
            else:
                if len(lib_list) >= size:
                    new_names = lib_list
                else:
                    raise discord.InvalidArgument('Too few words in Library')

        nicks = list(new_names)
        forbidden = []
        for m in ctx.guild.members:
            if m.id == self.bot.user.id:
                pass
            else:
                name = nicks[0]
                try:
                    await m.edit(nick=name, reason=f'{ctx.author} requested rename-madness')
                except:
                    forbidden.append(m.name)
                else:
                    nicks.remove(name)
        await ctx.send(embed=discord.Embed(
            title='New Nicknames!', color=(ctx.guild.get_member_named(str(self.bot.user))).color, 
            description=f'I happily just changed everyones nicknames!\nYou can thank {ctx.author.mention} for this.\nUnfornutaly the following users coudn\'t be renamed:\n{", ".join(forbidden)}'))

    @commands.command(name='vc', aliases=['voice'], brief='Voice chat integration', help=\
        'join -> join a vc; leave -> leave a vc; stop -> stop current playback; play -> play something')
    async def vc(self, ctx, command='join', category='', *track):
        txt = None
        user = ctx.message.author
        
        if command.lower() == 'join' or command.lower() == 'move':
            voice_channel = user.voice.channel 
            if voice_channel != None:
                if ctx.guild.voice_client != None:
                    await ctx.guild.voice_client.disconnect()
                    await voice_channel.connect()
                    txt = f'I just moved to *{voice_channel.name}* along with *{user.name}*'
                else:
                    await voice_channel.connect()
                    txt = f'I just joined *{voice_channel.name}* along with *{user.name}*'
            else:
                txt = f'Couldn\'t connect to Voice Channel'

        elif command.lower() == 'leave' or command.lower().startswith('dis'):
            if ctx.guild.voice_client != None:
                settings = self.load_settings()["settings"]["vc_vol"]
                vc_volume = settings.get(str(ctx.guild.id))
                if vc_volume == None:
                    vc_volume = vc_default
                volume = int(vc_volume)/100

                ctx.guild.voice_client.stop()
                audio = discord.FFmpegPCMAudio(source='https://www.myinstants.com/media/sounds/preview_4.mp3', options=f'-filter:a "volume={volume}"')
                ctx.guild.voice_client.play(audio)
                while ctx.guild.voice_client.is_playing():
                    time.sleep(0.5)
                await ctx.guild.voice_client.disconnect()
                # I'm not sure if this works correctly, but if it does,
                # it cleans up remaining voice_clients
                if ctx.guild.voice_client != None:
                    ctx.guild.voice_client.cleanup()
                txt = 'Disconnected from Voice Channel'
        
        elif command.lower().startswith('p'):
            argument = category.lower()
            modifier = (' '.join(track)).lower()
            
            with open(self.voice_lines) as f:
                data=f.read()
            lines = json.loads(data)

            quotes = None
            link = None
            search = None
            if len(argument) > 0:
                for e in lines.keys():
                    found = e.find(argument)
                    if found >= 0 and search != found:
                        search = found
                        quotes = lines[e]
                        if len(modifier) > 0:
                            for e in quotes.keys():
                                if e.find(modifier) >= 0:
                                    link = quotes[e]
                                    break
                            if link == None:
                                continue
                            else:
                                break
                        else:
                            break

            if quotes == None:
                quotes = lines[random.choice(list(lines.keys()))]
            if link == None:
                link = quotes[random.choice(list(quotes.keys()))]

            settings = self.load_settings()["settings"]["vc_vol"]
            vc_volume = settings.get(str(ctx.guild.id))
            if vc_volume == None:
                vc_volume = vc_default

            volume = int(vc_volume)/100
            audio = discord.FFmpegPCMAudio(source=link, options=f'-filter:a "volume={volume}"')
            ctx.guild.voice_client.stop()
            ctx.guild.voice_client.play(audio)

        elif command.lower().startswith('st'):
            ctx.guild.voice_client.stop()

        elif command.lower().startswith('vol'):
            settings = load_settings()
            vc_volume = settings["settings"]["vc_vol"].get(str(ctx.guild.id))

            if category == '':
                txt = f'Current volume is: {vc_volume}'
            elif category == '.' or category == '*' or category == '0':
                settings["settings"]["vc_vol"][str(ctx.guild.id)] = str(vc_default)
                with open(filepath, 'w') as f:
                    f.write(json.dumps(settings))

                txt = f'Volume set to {vc_default}'
            else:
                try:
                    new_vol = int(category)
                except:
                    txt = 'Need an Integer to set as Volume'
                else:
                    if new_vol > 0 and new_vol <= 120:
                        settings["settings"]["vc_vol"][str(ctx.guild.id)] = str(new_vol)
                        with open(filepath, 'w') as f:
                            f.write(json.dumps(settings))

                        txt = f'Volume set to {new_vol}'
                    else:
                        txt = 'Volume must be in between 1 and 120 (%)'

        if txt != None:
            await ctx.send(embed=discord.Embed(title='Voice Chat', color=(ctx.guild.get_member_named(str(self.bot.user))).color, description=txt))

    @commands.command(name="glitch", aliases=['gl'], brief='Get a glitched version of anyones PFP', help=\
        'Receive a glitched version of a PFP, Amount has to be in between 1 and 100 (both included)')
    @commands.cooldown(1, 45)
    async def glitch(self, ctx, user=None, amount=100, file_format='png', amount_change=10):
        member = ctx.message.mentions
        if len(member) == 0:
            member = ctx.message.author
        else:
            member = member[0]

        #Arg Processing
        amt = amount/10
        if amount_change != 0:
            amt_chg = amount_change/10
        else:
            amt_chg = 0
        if file_format.lower() == 'gif':
            file_format = True
        else:
            file_format = False

        glitcher = glitch_this.glitch_this.ImageGlitcher()
        src = Image.open(io.BytesIO(requests.get(member.avatar_url).content))

        img = glitcher.glitch_image(src, glitch_amount=amt, gif=file_format, color_offset=True, glitch_change=amt_chg, cycle=True, frames=18)

        if file_format == False:
            with io.BytesIO() as img_bin:
                img.save(img_bin, format='PNG')
                img_bin.seek(0)
                await ctx.send(file=discord.File(fp=img_bin, filename=f'{member.name}.png'))
        else:
            img_res, *imgs = img
            with io.BytesIO() as img_bin:
                img_res.save(img_bin, format='GIF', append_images=imgs, save_all=True, duration=80, loop=0)
                img_bin.seek(0)
                await ctx.send(file=discord.File(fp=img_bin, filename=f'{member.name}.gif'))

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = os.path.join(os.path.dirname(__file__), '../settings.json')

    def load_settings(self):
        with open(self.filepath, 'r') as f:
            data = json.load(f)
        return data

    @commands.command(name="apex", aliases=["Apex", "APEX"], brief='Get information about Apex', help=\
        'Get different information about Apex Legends you can use [status,map,news,player] as action, with status you need to provide server and region, you can choose multiple by seperating each with a comma without a space, use * for every result')
    @commands.cooldown(1, 2.5)
    async def apex(self, ctx, action='status', server='mozambiquehere', region='*', *arguments):
        title = 'Apex'
        cont = []
        mode = None
        desc = None
        embed = discord.Embed(title=title, color=discord.Color.from_rgb(205, 51, 51))
        embed.set_thumbnail(url='https://apknite.com/wp-content/uploads/2019/02/apex-logo-1.png')

        if action.lower().startswith('stat'):
            mode = 'Server Status'
            embed.set_footer(text='Please Note that I have no influence on the displayed content')
            embed.add_field(name='Source:', value='https://apexlegendsstatus.com', inline=False)
            resp = requests.get(f'https://api.mozambiquehe.re/servers?auth={API_Apex}')
            if resp.status_code == 200:
                servers = server.split(',')
                regions = region.split(',')
                response = resp.json()
                search = []
                for key in response.keys():
                    for arg in servers:
                        ind1 = key.lower().find(arg.lower())
                        if ind1 != -1 or arg == '*':
                            for e in response[key].keys():
                                for a in regions:
                                    ind2 = e.lower().find(a.lower())
                                    if ind2 != -1 or a == '*':
                                        cont.append(f"{key} : {e}? {response[key][e]['Status']} - {response[key][e]['ResponseTime']}ms!")
                if len(cont) == 0:
                    cont.append(f"Not Found : Not Found? N/A - -1ms!")
            else:
                desc = f'Server returned an error!\nStatus: {resp.status_code}'

        elif action.lower().startswith('map'):
            resp = requests.get(f'https://api.mozambiquehe.re/maprotation?auth={API_Apex}')
            if resp.status_code == 200:
                utc_offset = self.load_settings()['settings']['utc_offset'].get(str(ctx.guild.id))
                try:
                    utc_offset = int(utc_offset)
                except ValueError:
                    utc_offset = 0

                response = resp.json()
                mCurrent = response['current']
                mNext = response['next']
                embed.add_field(name=f"Current: {mCurrent['map']}", value=f"Remaining: {mCurrent['remainingTimer']}\nDuration: {mCurrent['DurationInMinutes']}min")
                embed.add_field(name=f"Next: {mNext['map']}", value=f"Starts: {(datetime.fromtimestamp(mNext['start']) + timedelta(hours=utc_offset)).strftime('%X')}\nDuration: {mNext['DurationInMinutes']}min")

            else:
                mode = 'Map status'
                desc = f'Server returned an error!\nStatus: {resp.status_code}'

        elif action.lower().startswith('news'):
            mode = 'Apex News'
            resp = requests.get(f'https://api.mozambiquehe.re/news?lang=en-us&auth={API_Apex}')
            if resp.status_code == 200:
                args = list(arguments).copy().insert(0, server).insert(1, region)
                article = None
                response = resp.json()
                if len(args) == 0:
                    article = random.choice(response)
                else:
                    for e in response:
                        for a in args:
                            ser = e['title'].lower().find(a.lower())
                            if ser != -1:
                                article = e
                                break
                    if article == None:
                        desc = None

                embed.set_image(url=article['img'])
                desc = f"*{article['title']}*\n\n{article['short_desc']}"
                embed.set_footer(text=f"Read more: {article['link']}")
            else:
                desc = f'Server returned an error!\nStatus: {resp.status_code}'

        elif action.lower().startswith('play'):
            mode = 'Player Info'
            if len(args) != 0:
                resp = requests.get(f'https://api.mozambiquehe.re/bridge?platform=PC&player={args[0]}&auth={API_Apex}')
                if resp.status_code == 200:
                    response = resp.json()
                    if response.get('Error') != None:
                        desc = 'Player not found! Note: You can only check the accounts of player who already played ranked!'
                    else:
                        mode = None
                        userInfo = response['global']
                        legend = response['legends']['selected']
                        badges = legend['gameInfo']['badges']
                        if response['realtime']['isOnline'] == 0:
                            playerisonline = 'Offline'
                        else:
                            playerisonline = 'Online'
                        embed.set_image(url=response['legends']['selected']['ImgAssets']['banner'])
                        embed.add_field(name=userInfo['name'], value=f"Level: {userInfo['level']} ({userInfo['toNextLevelPercent']}%)\nRank: {userInfo['rank']['rankName']}\nStatus: {playerisonline}")
                        embed.add_field(name=legend['LegendName'], value=f"{badges[0]['name']}\n{badges[1]['name']}\n{badges[2]['name']}")

                else:
                    desc = f'Server returned an error!\nStatus: {resp.status_code}'
            else:
                desc = 'Need an username to work with'

        if len(cont) != 0 and desc == None:
            desc = '\n'.join(cont)
        elif desc == None:
            desc = 'No results'
        if mode != None:
            embed.insert_field_at(0,name=mode,value=desc)
        await ctx.send(embed=embed)

def setup(bot):
    bot.remove_cog(utility)
    bot.remove_cog(games)
    bot.add_cog(utility(bot))
    bot.add_cog(games(bot))
