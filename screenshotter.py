# Takes screenshots of all input files and stores them in ./<filename>/
# proper documentation later :lul:

from argparse import ArgumentParser
import vapoursynth as vs
from random import choice, choices
import os
import re

core = vs.core

# TODO: offset for files
parser = ArgumentParser('Take screenshots of the same frame in different video files.')
parser.add_argument('clips', metavar='clips', type=str, nargs='+', help='paths to all video files')
parser.add_argument('--frames', '-f', dest='frames', type=str, nargs='?', help='List of frames (comma-separated)')
parser.add_argument('--num-frames', '-n', dest='num_frames', type=int, nargs='?', help='number of screenshots to take')

args = parser.parse_args()
clip_paths = args.clips
frames = args.frames
num_frames = args.num_frames if args.num_frames is not None else 10


def open_clip(path: str) -> vs.VideoNode:
    if path.endswith('ts'):  # .m2ts and .ts
        clip = core.lsmas.LWLibavSource(path)
    else:
        clip = core.ffms2.Source(path)
    clip = clip.resize.Spline36(format=vs.RGB24, matrix_in_s='709' if clip.height > 576 else '601')
    return clip


if __name__ == '__main__':
    if frames is not None:
        frames = [int(x) for x in frames.split(',')]
    else:
        length = len(open_clip(clip_paths[0]))
        frames = choices(range(length // 10, length // 10 * 9), k=num_frames)
        frames = set([x // 100 for x in frames])
        while len(frames) < num_frames:
            frames.add(choice(range(length // 10, length // 10 * 9)) // 100)
        frames = [x * 100 for x in frames]

    if hasattr(core, 'imwri'):
        imwri = core.imwri
    elif hasattr(core, 'imwrif'):
        imwri = core.imwrif
    else:
        raise AttributeError('Either imwri or imwrif must be installed.')
    for file in clip_paths:
        name = re.split(r'[\\/]', file)[-1].rsplit('.', 1)[0]
        os.mkdir(os.path.join(os.getcwd(), name))
        clip = open_clip(file)
        clip = imwri.Write(clip, 'png', os.path.join(os.getcwd(), name, '%d.png'))
        for frame in frames:
            clip.get_frame(frame)
