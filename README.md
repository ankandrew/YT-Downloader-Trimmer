# YT-Downloader-Trimmer

Simple program to download videos and trim them

### Requirements

Install needed requirements:
```
pip install -r requirements.txt
```

### Usage

The following example download the video as out_filename.mp4 with 480p resolution or else if not aviable. `only_vid=True` specifies video without sound.
```python
yt_d = Downloader(
    'yt-video-link', 'out_filename.mp4', quality=480, only_vid=True
)
```

To start downloading a video

```python
yt_d.download()
```

To trim it you can either pass start and end time in seconds i.e: start_time=20, end_time=70 or in string format like "00:00:20" and "00:00:20" (hh:mm:ss)

```python
yt_d.trim("00:02:10", "00:02:30", delete_original=False)
```

The trimmed filename with be the original one, but conctatenated with `_trimmed`
