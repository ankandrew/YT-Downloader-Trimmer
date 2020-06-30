# YT-Downloader-Trimmer

### Requirements

Install needed requirements:
```
pip install -r requirements.txt
```

### Usage

```python

# Usage ... Downloader(yt_link, out_name)
yt_d = Downloader(
    'https://www.youtube.com/watch?v=BtHFQ67J-L8', 'test2.mp4', quality=480, only_vid=True
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
