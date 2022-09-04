import discord
from discord.ext import commands, tasks
from TwitchAPI import Live_or_Not, Periodic_Live_Check
from datetime import timedelta
from pytz import timezone


f = open("discord_token.txt", 'r')
discord_token = f.readline()
f = f.close()


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)   #클래스 생성 13~15줄은 intents오류 설정

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

ls = []

@client.event
async def on_ready():
    change_status.start()
    print(f'Ready Kinga!')

@client.event
async def on_message(message):
    if message.author == client.user:      #봇은 메세지들의 모든 단어들을 체크하는데, 이때 자신의 메세지는 리턴하여 무시하고 사용자의 메세지만 받는다
        return
    elif message.content.startswith('/뱅'):
        global live_list
        live_list = ''
        for streamer_id, streamer in streamers.items():
            is_live = Live_or_Not(streamer_id)
            live_list += f'{streamer}: {is_live}\n'

        await message.channel.send("```" + live_list + "```")

    elif message.content.startswith('/봇등록'):
        ls.append(message.channel.id)
        await message.channel.send('채널을 등록했어염')
    elif message.content.startswith('/봇제거'):
        ls.remove(message.channel.id)
        await message.channel.send('봇을 제거했어요')
    elif message.content.startswith('/봇시작'):
        when_live.start()


@tasks.loop(seconds=2)
async def when_live():
    for channel in ls:
        channel = client.get_channel(channel)
        print(channel)
        for streamer_id, streamer in streamers.items():
            is_live = Periodic_Live_Check(streamer_id)
            if is_live:
                if is_live != live_compare.get(streamer_id):
                    live_compare[streamer_id] = True
                    await channel.send("@everyone " + streamer + " 뱅온!")
            else:
                if is_live != live_compare.get(streamer_id):
                    live_compare[streamer_id] = False
                    await channel.send("@everyone " + streamer + " 뱅종!")

@tasks.loop(seconds=255)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='RE:WIND'))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='겨울봄'))

client.run(discord_token)