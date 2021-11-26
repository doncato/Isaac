import os,json,requests
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO,StringIO

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
    if num < 0:
        num = 0
    elif num > 9:
        num = "+"
    current_icon = BytesIO(await guild.icon_url.read())
    # These are the settings for the positions and stuff
    with Image.open(current_icon) as f:
        size = f.size
    coordinates = [(int(0.1*size[0]), int(0.1*size[1])), (int(0.4*size[0]), int(0.4*size[1]))]
    text_anchor = [int(0.25*size[0]), int(0.25*size[1])]
    text_rgb = (200, 200, 200)
    text_font = ImageFont.truetype(font=os.path.join(os.path.dirname(__file__), '../rsc/TempestApache.otf'), size=int(0.4*size[0]))
    outline_rgb = (88, 101, 242) # Should match discords blue
    fill_rgb = (88, 101, 242) # Should match discords blue
    
    with Image.open(current_icon) as icon:
        draw = ImageDraw.Draw(icon)
        draw.ellipse(coordinates, outline=outline_rgb, fill=fill_rgb)
        draw.text(text_anchor, str(num), font=text_font, anchor="mm", fill=text_rgb, align='center')
        current_icon.seek(0)
        icon.save(current_icon, format="PNG")
        current_icon.seek(0)

    await guild.edit(icon=current_icon.read())

    del current_icon
    del icon
