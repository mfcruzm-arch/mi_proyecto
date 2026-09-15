import os

if os.path.exists('solution.py'):
    from solution import File, MediaFile, VideoFile
else:
    from main import File, MediaFile, VideoFile  # type:ignore


def test_inheritance():
    assert issubclass(File, object)
    assert issubclass(MediaFile, File)
    assert issubclass(VideoFile, MediaFile)


def test_str():
    mp4 = VideoFile('/home/python/vanrossum.mp4', 'h264', (23.5454, 31.4343), 487, (1920, 1080))
    mp4.add_content('audio/ogg')
    mp4.add_content('video/webm')
    assert (
        mp4.info
        == """/home/python/vanrossum.mp4 [size=19B]
Codec: h264
Geolocalization: (23.5454, 31.4343)
Duration: 487s
Dimensions: (1920, 1080)"""
    )
