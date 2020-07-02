from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import youtube_dl
from pathlib import Path
import os.path


class Downloader:
    def __init__(self, video_url, output, quality=480, only_vid=True, only_mp3=False):
        '''
        Params:
        video_url: youtube video url
        output_name: filename (without extension)
        quality: height
        '''
        self.video_url = video_url
        self.output = Path(output)
        self.ydl_opts = {
            'noplaylist': True,
            'outtmpl': output,
            # Aviable if you have ffmpeg installed
            # Otherwise you can download audio + videos w/o specific res
            # 'format': f'bestvideo[height<={quality[0]}]+bestaudio/best[width<={quality[1]}]'
        }
        if not only_mp3:
            if only_vid:
                self.ydl_opts['format'] = f'bestvideo[height<={quality}]'
                self.ydl_opts['ext'] = 'mp4'
        else:
            self.ydl_opts['format'] = 'bestaudio'
            self.ydl_opts['ext'] = 'mp3'

    def download(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                # ydl.cache.remove()  # Fixes 403 forbidden error
                ydl.download([self.video_url])
            except youtube_dl.utils.DownloadError as e:
                print(e)

    def trim(self, start_time, end_time, delete_original=False, out_name=None):
        '''
        start_time and end_time in seconds
        start_time and end_time can be in format: 30, 40 or "10:39", "11:40"
        '''
        if(isinstance(start_time, str) and isinstance(end_time, str)):
            start_time = self.__str_to_seconds(start_time)
            end_time = self.__str_to_seconds(end_time)
        if out_name is None:
            new_file_name = self.output.parents[0] / \
                self.__edit_out_filename(self.output.name)
        else:
            new_file_name = self.output.parents[0] / out_name
        ffmpeg_extract_subclip(
            str(self.output), start_time, end_time, targetname=str(new_file_name))
        if delete_original:
            self.delete_video()

    def __edit_out_filename(self, filename):
        list_split = filename.split('.')
        list_split.insert(-1, '_trimmed')
        return ''.join(list_split[:-1]) + '.' + list_split[-1]

    def __str_to_seconds(self, to_parse):
        # Exameple input: "00:10:30" or "00:10:00" or "00:10:60"
        hours, minutes, seconds = to_parse.split(':')
        return int(hours) * 60**2 + int(minutes) * 60 + int(seconds)

    def delete_video(self):
        os.remove(self.output)
