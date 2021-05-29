from youtube_api import YoutubeDataApi
from app.config import YT_TOKEN, END_OF_QUOTA
import re
import requests
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
)

class YTApi(YoutubeDataApi):

    def video_title(self, video_id: str) -> str:
        try:
            metadata = self.get_video_metadata(video_id)
            return metadata['video_title']
        except requests.exceptions.HTTPError as e:
            logging.error(f'{e} - The number of requests has ended')
            return END_OF_QUOTA

    def get_channel_name(self, channel_id):
        try:
            metadata = self.get_channel_metadata(channel_id)
            return metadata['title']
        except requests.exceptions.HTTPError as e:
            logging.error(f'{e} - The number of requests has ended')
            return END_OF_QUOTA

    def get_last_video_id(self, channel_id):
        try:
            main_playlist_id = self.get_channel_metadata(channel_id=channel_id)['playlist_id_uploads']
            all_videos = self.get_videos_from_playlist_id(playlist_id=main_playlist_id)
            return all_videos[0]['video_id']
        except requests.exceptions.HTTPError as e:
            logging.error(f'{e} - The number of requests has ended')
            return END_OF_QUOTA

    def get_channel_id_by_url(self, channel_url: str) -> str:
        try:
            channel_id = re.split('/+', channel_url)[-1]
            if self.get_channel_metadata(channel_id):
                return channel_id
            if channel_info := self.search(channel_id):
                return channel_info[0]['channel_id']
        except requests.exceptions.HTTPError as e:
            logging.error(f'{e} - The number of requests has ended')
            return END_OF_QUOTA


if __name__ == '__main__':
    yt = YTApi(YT_TOKEN)
    result = yt.get_channel_id_by_url(
        'https://www.youtube.com/c/ArchakovBlog'
    )
    print(result)
