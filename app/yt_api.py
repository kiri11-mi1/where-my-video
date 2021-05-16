from youtube_api import YoutubeDataApi
from app.config import YT_TOKEN
import re
import requests


class YTApi(YoutubeDataApi):


    def video_title(self, video_id: str) -> str:
        return self.get_video_metadata(video_id)['video_title']


    def get_channel_name(self, channel_id):
        return self.get_channel_metadata(channel_id)['title']


    def get_last_video_id(self, channel_id):
        try:
            main_playlist_id = self.get_channel_metadata(channel_id=channel_id)['playlist_id_uploads']
            all_videos = self.get_videos_from_playlist_id(playlist_id=main_playlist_id)
            return all_videos[0]['video_id']
        except requests.exceptions.HTTPError:
            return None


    def get_channel_id_by_url(self, channel_url:str) -> str:
        channel_id = re.split('/+', channel_url)[-1]
        if self.get_channel_metadata(channel_id):
            return channel_id


if __name__ == '__main__':
    # response = requests.get(
    #     url = f'https://www.googleapis.com/youtube/v3/channels?part=snippetforUsername=ExtremeCode&key={YT_TOKEN}',
    #     # params = {
    #     #     'part': 'snippetforUsername=ExtremeCode',
    #     #     'key': YT_TOKEN
    #     # }
    # ).json()
    # print(response)
    # ExtremeCode - Channel Id - UCBNlINWfd08qgDkUTaUY4_w
    yt = YTApi(YT_TOKEN)
    result = yt.get_video_metadata('G6rrIxY9q0')
    # result = yt.search('https://www.youtube.com/channel/UCBNlINWfd08qgDkUTaUY4_w')

    # url = [
    #     'https://www.youtube.com/channel/UCBNlINWfd08qgDkUTaUY4_w',
    #     'https://www.youtube.com/c/ExtremeCode',
    #     'https://www.youtube.com/channel/UCAJYuvFKA_MlFq6ekkn7WFA'
    # ]
    
    
    # # result = yt.get_last_video_id('UCBNlINWfd08qgDkUTaUY4_w')
    # result = yt.get_channel_metadata(channel_id='ExtremeCode')
    # result = yt.get_channel_id('https://www.youtube.com/channel/UCqqISS-PyCnhjbpXqhclvaQ')
    # result = yt.get_last_video_id('UCBNlINWfd08qgDkUTaUY4_w')
    print(result)
    # UCD5_waDcGBhof9xuA1qovTQ
    # UCPJXxmrw1NRmOwdZtLM694g
