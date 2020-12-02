def load_input(inpf):
    numbers = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if line:
                numbers.append(int(line))
    return numbers


def part1(inpf):
    nums = load_input(inpf)
    for i in range(0, len(nums) - 1):
        for j in range(i+1, len(nums)):
            a = nums[i]
            b = nums[j]
            if a + b == 2020:
                return a*b


def part2(inpf):
    nums = load_input(inpf)
    for i in range(0, len(nums) - 2):
        for j in range(i+1, len(nums) - 1):
            for k in range(j+1, len(nums)):
                a = nums[i]
                b = nums[j]
                c = nums[k]
                if a + b + c == 2020:
                    return a*b*c

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))