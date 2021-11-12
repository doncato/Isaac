import os,json

def load_settings():
    with open(os.path.join(os.path.dirname(__file__), '../settings.json'), 'r') as f:
        data = json.load(f)
    return data

async def change_trailing_channel_num(guild, channel_id: int, increase=True):
        channel = guild.get_channel(id)
        if channel != None:
            name = channel.name.split(' ')
            try:
                if increase:
                    new_name = name[:-1] + " " + str(int(name[-1]) + 1)
                else:
                    new_name = name[:-1] + " " + str(int(name[-1]) - 1)
            except:
                return False
            else:
                await channel.edit(name=new_name)
                return True
        else:
            return False

async def edit_trailing_channel_num(guild, channel_id: int, num: int):
        channel = guild.get_channel(id)
        if channel != None:
            name = channel.name.split(' ')
            new_name = name[:-1] + " " + num
            await channel.edit(name=new_name)
            return True
        else:
            return False