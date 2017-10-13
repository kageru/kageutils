import re


# just a few random python snippets that I used for (((things)))

def split_array(a, n):
    s = len(a) / n
    for c in range(n):
        yield a[round(s * c):round(s * (c + 1))]


def shiftl(x, bits):
    return x << bits if bits >= 0 else x >> -bits


def char_range(start='a', end='z'):
    return [chr(x) for x in range(ord(start), ord(end) + 1)]


def time_to_frame(line: str, fps=24000 / 1001) -> int:
    timestamp = re.match(r'(\d{1,2}:)?\d{1,2}:\d{1,2}', line)
    times = timestamp.group(0).split(':')
    sum = 0
    for t in reversed(times):
        sum += (fps * int(t))
        fps *= 60
    return round(sum)
