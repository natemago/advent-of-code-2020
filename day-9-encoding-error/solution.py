def read_input(inpf):
    with open(inpf) as f:
        return [int(line.strip()) for line in f]

def get_sums(preamble):
    sums = set()
    for i in range(0, len(preamble) - 1):
        for j in range(i+1, len(preamble)):
            sums.add(preamble[i] + preamble[j])
    return sums

def part1(inpf, psize=25):
    numbers = read_input(inpf)
    for i in range(psize, len(numbers)):
        num = numbers[i]
        preamble = numbers[i-psize:i]
        sums = get_sums(preamble)
        if num not in sums:
            return num


def part2(inpf):
    target = part1(inpf)
    numbers = read_input(inpf)
    for i in range(0, len(numbers)):
        s = 0
        for j in range(i, len(numbers)):
            s += numbers[j]
            if s == target and j-i > 1:
                cset = numbers[i:j+1]
                return min(cset) + max(cset)



print('Part 1:', part1('input', 25))
print('Part 2:', part2('input'))