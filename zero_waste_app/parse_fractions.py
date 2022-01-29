import re

FRACTIONS = {
    0x2152: 0.1,  # 1/10
    0x2151: 0.11111111,  # 1/9
    0x215B: 0.125,  # 1/8
    0x2150: 0.14285714,  # 1/7
    0x2159: 0.16666667,  # 1/6
    0x2155: 0.2,  # 1/5
    0x00BC: 0.25,  # 1/4
    0x2153: 0.33333333,  # 1/3
    0x215C: 0.375,  # 3/8
    0x2156: 0.4,  # 2/5
    0x00BD: 0.5,  # 1/2
    0x2157: 0.6,  # 3/5
    0x215D: 0.625,  # 5/8
    0x2154: 0.66666667,  # 2/3
    0x00BE: 0.75,  # 3/4
    0x2158: 0.8,  # 4/5
    0x215A: 0.83333333,  # 5/6
    0x215E: 0.875,  # 7/8
}

RX = r'(?u)(%s)' % '|'.join(map(chr, FRACTIONS))


def parse_problematic_numbers(tekst):
    to_change = re.findall(RX, tekst)
    if to_change:
        return FRACTIONS[ord(to_change[0])]
    else:
        return tekst.replace(',', '.', 1)
