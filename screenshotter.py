# Takes screenshots of all input files and stores them in ./<filename>/
# proper documentation later :lul:

from argparse import ArgumentParser
import vapoursynth as vs
from random import choice, choices
import os
import re

core = vs.core


parser = ArgumentParser('Take screenshots of the same frame in different video files.')
parser.add_argument('clips', metavar='clips', type=str, nargs='+', help='Paths to all video files', required=True)
parser.add_argument('--frames', '-f', dest='frames', type=int, nargs='+',
                    help='List of frames (space-separated), optional')
parser.add_argument('--num-frames', '-n', dest='num_frames', type=int, nargs='?',
                    help='Number of screenshots to take, default=10')
parser.add_argument('--offsets', '-o', dest='offsets', type=str, nargs='?',
                    help='List of offsets for all clips in frames (space-separated). Order must match order of the clips, optional')

args = parser.parse_args()
clip_paths = args.clips
frames = args.frames
num_frames = args.num_frames if args.num_frames is not None else 10
offsets = args.offsets


def open_clip(path: str) -> vs.VideoNode:
    if path.endswith('ts'):  # .m2ts and .ts
        clip = core.lsmas.LWLibavSource(path)
    else:
        clip = core.ffms2.Source(path)
    clip = clip.resize.Spline36(format=vs.RGB24, matrix_in_s='709' if clip.height > 576 else '601')
    return clip


def get_frame_numbers(clip, n):
    length = len(open_clip(clip))
    frames = choices(range(length // 10, length // 10 * 9), k=n)
    frames = set([x // 100 for x in frames])
    while len(frames) < num_frames:
        frames.add(choice(range(length // 10, length // 10 * 9)) // 100)
    return [x * 100 for x in frames]


if __name__ == '__main__':
    if frames is None:
        frames = get_frame_numbers(clip_paths[0], num_frames)
    print('Requesting frames:', *frames)

    if hasattr(core, 'imwri'):
        imwri = core.imwri
    elif hasattr(core, 'imwrif'):
        imwri = core.imwrif
    else:
        raise AttributeError('Either imwri or imwrif must be installed.')
    for file, offs in clip_paths, offsets:
        name = re.split(r'[\\/]', file)[-1].rsplit('.', 1)[0]
        os.mkdir(os.path.join(os.getcwd(), name))
        clip = open_clip(file)
        savepath = os.path.join(os.getcwd(), name)
        clip = imwri.Write(clip, 'png', os.path.join(savepath, '%d.png'))
        for frame in frames:
            print('Writing {:s}/{:d}.png'.format(savepath, frame + offs))
            clip.get_frame(frame + offs)
