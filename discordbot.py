import discord
from discord.ext import commands, tasks
from TwitchAPI import Live_or_Not, Periodic_Live_Check
from datetime import timedelta
from pytz import timezone


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)   #Create class 13 to 15 lines set intents error

f = open("discord_token.txt", 'r')
discord_token = f.readline()
f = f.close()

shortcut_links = {
    "woowakgood":"https://www.twitch.tv/woowakgood", 
    "vo_ine":"https://www.twitch.tv/vo_ine",
    "jingburger":"https://www.twitch.tv/jingburger",
    "lilpaaaaaa":"https://www.twitch.tv/lilpaaaaaa", 
    "cotton__123":"https://www.twitch.tv/cotton__123", 
    "gosegugosegu":"https://www.twitch.tv/gosegugosegu", 
    "viichan6":"https://www.twitch.tv/viichan6"
}
personal_color = {
    "woowakgood":0x008d62, 
    "vo_ine":0x8A2BE2,
    "jingburger":0xf0a957,
    "lilpaaaaaa":0x000080, 
    "cotton__123":0x800080, 
    "gosegugosegu":0x467ec6, 
    "viichan6":0x85ac20
}
streamers = {
    "woowakgood":"우왁굳", 
    "vo_ine":"아이네",
    "jingburger":"징버거",
    "lilpaaaaaa":"릴파", 
    "cotton__123":"주르르", 
    "gosegugosegu":"고세구", 
    "viichan6":"비챤"
}
live_compare = {
    "woowakgood":False, 
    "vo_ine":False, 
    "jingburger":False, 
    "lilpaaaaaa":False, 
    "cotton__123":False, 
    "gosegugosegu":False, 
    "viichan6":False
}

discord_channels = []

@client.event
async def on_ready():
    change_status.start()
    print(f'Ready!')

@client.event
async def on_message(message):
    if message.author == client.user:      #The bot checks all the words in the messages, when it returns its own message and only receives the user's message
        return
    elif message.content.startswith('/register bot'):
        discord_channels.append(message.channel.id)
        await message.channel.send('registered the channel')
    elif message.content.startswith('/delete bot'):
        discord_channels.remove(message.channel.id)
        await message.channel.send('got rid of the bot')
    elif message.content.startswith('/start bot'):
        when_live.start()

    elif message.content.startswith('/stream condition'):
        global live_list
        live_list = ''
        for streamer_id, streamer in streamers.items():
            is_live = Live_or_Not(streamer_id)
            embed = discord.Embed(title="streamers")
            if live_compare[streamer_id]:
                live_list += f"{streamer}: [{is_live}]("+shortcut_links[streamer_id]+")\n"
            else:
                live_list += f"{streamer}: {is_live}\n"
        embed.description = live_list
        await message.channel.send(embed=embed)

@tasks.loop(seconds=30)
async def when_live():
    for channel in discord_channels:
        channel = client.get_channel(channel)
        for streamer_id, streamer in streamers.items():
            is_live, title, thumbnail_url = Periodic_Live_Check(streamer_id)
            if is_live:
                if is_live != live_compare.get(streamer_id):
                    live_compare[streamer_id] = True
                    embed = discord.Embed(title=streamer+" shortcut", url=shortcut_links[streamer_id], color=personal_color[streamer_id])
                    embed.description = title
                    embed.set_image(url=thumbnail_url)
                    await channel.send("@everyone " + streamer + " on air!", embed=embed)
            else:
                if is_live != live_compare.get(streamer_id):
                    live_compare[streamer_id] = False
                    await channel.send("@everyone " + streamer + " off air!")

client.run(discord_token)
