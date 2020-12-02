import re

def read_input(inpf):
    entries = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = re.search(r'(?P<min>\d+)-(?P<max>\d+)\s+(?P<char>.):\s+(?P<pass>[^\s]+)', line)
            if m:
                entries.append((
                    int(m.group('min')),
                    int(m.group('max')),
                    m.group('char'),
                    m.group('pass')
                ))
    return entries


def count_leters(s):
    r = {}
    for c in s:
        r[c] = r.get(c, 0) + 1
    return r


def part1(inpf):
    count = 0
    for mn, mx, ch, passswd in read_input(inpf):
        c = count_leters(passswd)
        if c.get(ch, 0) >= mn and c.get(ch, 0) <= mx:
            count += 1
    return count


def part2(inpf):
    count = 0
    for mn, mx, ch, passswd in read_input(inpf):
        mn -= 1
        mx -= 1
        correct = 0
        if mn >= 0 and mn < len(passswd) and passswd[mn] == ch: 
            correct += 1
        if mx >= 0 and mx < len(passswd) and passswd[mx] == ch:
            correct += 1
        if correct == 1:
            count += 1
    return count

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))