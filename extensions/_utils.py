import os,json
from PIL import Image,ImageDraw,ImageFont

def load_settings():
    with open(os.path.join(os.path.dirname(__file__), '../settings.json'), 'r') as f:
        data = json.load(f)
    return data

def save_settings(obj):
    with open(os.path.join(os.path.dirname(__file__), '../settings.json'), 'w') as f:
        f.write(json.dumps(obj))

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

async def edit_server_icon_num(guild, num: int):
    coordinates = [(0, 0), (100, 100)]
    text_anchor = [50, 50]
    text_rgb = (200, 200, 200)
    text_font = ImageFont.truetype(font=os.path.join(os.path.dirname(__file__), '../rsc/TempestApache.otf'), size=36)
    outline_rgb = (88, 101, 242) # Should match discords blue
    fill_rgb = (88, 101, 242) # Should match discords blue
    
    new_icon = bytearray()
    with Image.open(guild.icon_url.read()) as icon:
        draw = ImageDraw.draw(icon)
        draw.ellipse(coordinates, outline=outline_rgb, fill=fill_rgb)
        draw.text(text_anchor, str(num), font=text_font, anchor="mm", fill=text_rgb, align='center')
        icon.save(new_icon, format="PNG")
        await guild.edit(icon=new_icon)

    del new_icon
