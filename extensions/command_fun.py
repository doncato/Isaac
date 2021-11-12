# command_fun.py / IsaacII Discord Bot
# Author: https://github.com/doncato
# Created on: 10/07/21

import os,discord,json,time,random,requests
from datetime import datetime,timedelta
from discord.ext import commands

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
