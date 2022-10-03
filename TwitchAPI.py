from email import header
import json
import requests
import schedule

file  = open("twitch_token.txt", 'r')
client_secret = file.readline()
file = file.close()

client_id = 'uhwxt9tkd8mc3e8oxo9r9sauh81jod'
API_Token = ''

params = {
    'client_secret' : client_secret,
    'grant_type' : 'client_credentials',
    'client_id' : client_id,
}

def job():
    API_Token = requests.post('https://id.twitch.tv/oauth2/token', params=params)
    API_Token = API_Token.json()
    API_Token = API_Token.get('access_token')
schedule.every(4500000).seconds.do(job)

API_Token = requests.post('https://id.twitch.tv/oauth2/token', params=params)
API_Token = API_Token.json()
API_Token = API_Token.get('access_token')

headers = {
    'Authorization': 'Bearer ' + API_Token,
    'Client-Id': client_id,
}

def Live_or_Not(streamer):
    is_live = requests.get('https://api.twitch.tv/helix/search/channels', params={'query': streamer}, headers=headers)
    is_live = is_live.json()
    is_live = is_live.get('data')[0].get('is_live')
    is_live = int(is_live)

    live_option = ["휴뱅중", "뱅온중"]
    is_live = live_option[is_live]
    return is_live

def Periodic_Live_Check(streamer):
    is_live = requests.get('https://api.twitch.tv/helix/search/channels', params={'query': streamer}, headers=headers)
    is_live = is_live.json()
    title = is_live.get('data')[0].get('title')
    thumbnail_url = is_live.get('data')[0].get('thumbnail_url')


    for data in is_live['data']:
        if data['broadcaster_login'] == streamer:
            return data['is_live'], title, thumbnail_url
    return False

# if __name__ == '__main__':  #이 파일 전용 테스트 코드
#     Periodic_Live_Check('woowakgood')
