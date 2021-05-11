from youtube_api import YoutubeDataApi
from app.config import YT_TOKEN
import os


class YTApi:
    def __init__(self, token):
        self.yt = YoutubeDataApi(token)


    def video_title(self, video_id):
        return self.yt.get_video_metadata(video_id)['video_title']


    def get_videos_from_channel(self, channel_id):
        main_playlist_id = self.yt.get_channel_metadata(channel_id=channel_id)['playlist_id_uploads']
        return self.yt.get_videos_from_playlist_id(playlist_id=main_playlist_id)


    def get_channel_id(self, channel_url):
        pass


yt = YoutubeDataApi(YT_TOKEN)
