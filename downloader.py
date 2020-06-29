# from __future__ import unicode_literals
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import youtube_dl
from pathlib import Path
import os.path


class Downloader:
    def __init__(self, video_url, output, quality=480, only_vid=True):
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
            'ext': 'mp4'
            # Aviable if you have ffmpeg installed
            # Otherwise you can download audio + videos w/o specific res
            # 'format': f'bestvideo[height<={quality[0]}]+bestaudio/best[width<={quality[1]}]'
        }
        if only_vid:
            self.ydl_opts['format'] = f'bestvideo[height<={quality}]'

    def download(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            try:
                # ydl.cache.remove()  # Fixes 403 forbidden error
                ydl.download([self.video_url])
            except youtube_dl.utils.DownloadError as e:
                print(e)

    def trim(self, start_time, end_time, delete_original=False):
        '''
        start_time and end_time in seconds
        start_time and end_time can be in format: 30, 40 or "10:39", "11:40"
        '''
        if(isinstance(start_time, str) and isinstance(end_time, str)):
            start_time = self.__str_to_seconds(start_time)
            end_time = self.__str_to_seconds(end_time)

        new_file_name = self.output.parents[0] / \
            self.__edit_out_filename(self.output.name)
        ffmpeg_extract_subclip(
            str(self.output), start_time, end_time, targetname=str(new_file_name))
        if delete_original:
            self.delete_video()

    def __edit_out_filename(self, filename):
        list_split = filename.split('.')
        list_split.insert(-1, '_trimmed')
        return ''.join(list_split[:-1]) + '.' + list_split[-1]

    def __str_to_seconds(self, to_parse):
        # Exameple input: "10:30" or "10:00" or "10:60"
        minutes, seconds = to_parse.split(':')
        return int(minutes) * 60 + int(seconds)

    def delete_video(self):
        os.remove(self.output)


if __name__ == "__main__":
    # Usage ... Downloader(yt_link, out_name)
    yt_d = Downloader(
        'https://www.youtube.com/watch?v=BtHFQ67J-L8', 'test2.mp4', quality=480, only_vid=True)
    yt_d.download()
    # yt_d.trim("7:56", "13:49", delete_original=False)
    yt_d.trim("2:10", "2:30", delete_original=False)


# # from __future__ import unicode_literals
# from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
# import youtube_dl
# from pathlib import Path
# import os.path


# class Downloader:
#     def __init__(self, video_url, output_name, save_path=None, only_mp3=False, quality=(480, 480)):
#         '''
#         Params:
#         video_url: youtube video url
#         output_name: filename (without extension)
#         save_path: If None, use current working directory
#         quality: (height, width)
#         '''
#         self.video_url = video_url
#         if save_path is None or not os.path.exists(save_path):
#             print('Path doesn\'t exist or save_path is None, using current directory')
#             self.save_path = Path(os.getcwd())
#         else:
#             self.save_path = Path(save_path)
#         self.save_path = self.save_path / output_name
#         self.ydl_opts = {
#             'noplaylist': True,
#             'outtmpl': str(self.save_path),
#             'format': f'bestvideo[height<={quality[0]}]+bestaudio/best[height<={quality[1]}]'
#         }
#         # Doesn't work
#         # if only_mp3:
#         #     self.ydl_opts['postprocessors'] = [{
#         #         'key': 'FFmpegExtractAudio',
#         #         'preferredcodec': 'mp3',
#         #         'preferredquality': '192',
#         #     }]

#     def download(self):
#         with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
#             try:
#                 ydl.cache.remove()  # Fixes 403 forbidden error
#                 ydl.download([self.video_url])
#             except youtube_dl.utils.DownloadError as e:
#                 print(e)

#     def trim(self, start_time, end_time, delete_original=True):
#         '''
#         start_time and end_time in seconds
#         start_time and end_time can be in format: 30, 40 or "10:39", "11:40"
#         '''
#         if(isinstance(start_time, str) and isinstance(end_time, str)):
#             start_time = self.str_to_seconds(start_time)
#             end_time = self.str_to_seconds(end_time)
#         new_file_name = self.save_path.parents[0] / \
#             self.__edit_out_filename(self.save_path.name)
#         ffmpeg_extract_subclip(
#             str(self.save_path), start_time, end_time, targetname=str(new_file_name))
#         if delete_original:
#             self.delete_video()

#     def __edit_out_filename(self, filename):
#         list_split = filename.split('.')
#         list_split.insert(-1, '_trimmed')
#         return ''.join(list_split[:-1]) + '.' + list_split[-1]

#     def delete_video(self):
#         os.remove(self.save_path)

#     def str_to_seconds(self, to_parse):
#         # Exameple input: "10:30" or "10:00" or "10:60"
#         minutes, seconds = to_parse.split(':')
#         return int(minutes) * 60 + int(seconds)


# if __name__ == "__main__":
#     # Usage ... Downloader(yt_link, save_path, out_name)
#     yt_d = Downloader(
#         'https://www.youtube.com/watch?v=B7VyGwPpJp0', 'Driving_in_Buenos_Aires.mp4',
#         save_path='C:/Users/Andy/Desktop/', only_mp3=False, quality=(1920, 1080))
#     yt_d.download()
#     yt_d.trim("7:56", "13:49", delete_original=False)
