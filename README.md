# kageutils
A collection of scripts and thing that I have written.   
Nothing to see here; move along.

## kageutils.py
A few very short methods that might be useful in other python projects. Feel free to import or just copy-paste them.

## encode-screenshotter.py
Takes screenshots of all specified input files and stores them in './<filename>/<frame_number>.png'.  
Probably useful for encoders to compare source and encode or different versions of the same video.
#### Usage
Get 10 random screenshots (the same frames) from both videos and save them in `./video1/` and `./video2/`:
```
$ python encode-screenshotter.py /path/to/first/video1.mkv /path/to/another/video2.m2ts
```
Get screenshots of the specified frames and offset the first clip by 24 frames:
```
$ python encode-screenshotter.py video1.mkv video2.mkv -o 24 0 -f 1000 2500 5000 8000
```
This will save the frames [1024, 2524, 5024, 8024] from video1 and [1000, 2500, 5000, 8000] from video2.