import re


# just a few random python snippets that I used for (((things)))

def split_array(a: list, n: int) -> list:
    "Split the input array into n pieces of similar size"
    s = len(a) / n
    for c in range(n):
        yield a[round(s * c):round(s * (c + 1))]


def shiftl(x: int, bits: int) -> int:
    """
    Why even...? Shifts number to the left by n bits.
    n can be negative, resulting in a right-shift by n bits.
    """
    return x << bits if bits >= 0 else x >> -bits


def char_range(start='a', end='z'):
    """
    Returns a range of chars.
    Mainly intended for latin characters, but other characters are possible, too.
    """
    return [chr(x) for x in range(ord(start), ord(end) + 1)]


def time_to_frame(line: str, fps=24000 / 1001) -> int:
    """
    Converts a timestamp in the format <hours>:<minutes>:<seconds>.<milliseconds> into the corresponding frame number.
    <hours> and <milliseconds> are optional,
    and milliseconds can have arbitrary precision (which means they are no longer milliseconds :thonking: ).
    A parameter for the framerate can be passed if required.
    Valid example inputs: '1:23.456', '01:10:00', '0:00:00.000', '24:30.2'
    """
    timestamp = re.match(r'(\d{1,2}:)?\d{1,2}:\d{1,2}(\.\d{1,3})', line)
    if not timestamp:
        return -1
    times = timestamp.group(0).split(':')
    if '.' in times[-1]:     # milliseconds are specified
        times[-1], ms = times[-1].split('.')
        frame = fps * (int(ms) / 10**len(ms))
    else:
        frame = 0
    for t in reversed(times):
        frame += (fps * int(t))
        fps *= 60
    return round(frame)
