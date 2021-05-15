from youtube_api import YoutubeDataApi
from app.config import YT_TOKEN


class YTApi(YoutubeDataApi):

    def video_title(self, video_id: str) -> str:
        return self.yt.get_video_metadata(video_id)['video_title']


    def get_videos_from_channel(self, channel_id: str) -> list:
        main_playlist_id = self.get_channel_metadata(channel_id=channel_id)['playlist_id_uploads']
        return self.get_videos_from_playlist_id(playlist_id=main_playlist_id)


    def get_last_video_id(self, channel_id):
        main_playlist_id = self.get_channel_metadata(channel_id=channel_id)['playlist_id_uploads']
        all_videos = self.get_videos_from_playlist_id(playlist_id=main_playlist_id)
        return all_videos[0]['video_id']


    def get_channel_id(self, channel_url) -> str:
        pass


    def get_channel_id_by_url(self, chan_url:str) -> str:
        if result_search := self.search(chan_url):
            return result_search[0]['channel_id']


if __name__ == '__main__':
    # ExtremeCode - Channel Id - UCBNlINWfd08qgDkUTaUY4_w
    yt = YTApi(YT_TOKEN)
    url = [
        'https://www.youtube.com/channel/UCBNlINWfd08qgDkUTaUY4_w',
        'https://www.youtube.com/c/ExtremeCode',
        'https://www.youtube.com/channel/UCAJYuvFKA_MlFq6ekkn7WFA'
    ]
    
    result = yt.get_last_video_id('UCBNlINWfd08qgDkUTaUY4_w')
    print(result)
