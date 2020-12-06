def read_input(inpf):
    groups = []
    with open(inpf) as f:
        buff = []
        for line in f:
            line = line.strip()
            if line:
                buff.append(line)
            else:
                if buff:
                    groups.append(buff)
                buff = []
        if buff:
            groups.append(buff)
    return groups


def part1(inpf):
    return sum(map(lambda grp: len(set([c for buff in grp for c in buff])), read_input(inpf)))


def part2(inpf):
    total = 0
    for group in read_input(inpf):
        s = set([c for c in group[0]])
        for buff in group[1:]:
            s = s.intersection([c for c in buff])
        total += len(s)
    return total

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))