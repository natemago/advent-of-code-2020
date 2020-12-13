def read_input(inpf):
    instructoins = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            instructoins.append((line[0], int(line[1:])))
    return instructoins


def rotate_90(vec):
    return [
        vec[1],
        -vec[0],
    ]

def rotate_180(vec):
    return [
        -vec[0],
        -vec[1],
    ]


def rotate_270(vec):
    return [
        -vec[1],
        vec[0],
    ]


ROTATIONS = {
    90: rotate_90,
    180: rotate_180,
    270: rotate_270,
    -90: rotate_270,
    -180: rotate_180,
    -270: rotate_90,
}

def part1(inpf):
    instructions = read_input(inpf)

    pos = [0, 0]
    direction = [1, 0]  # facing east

    for inst, value in instructions:
        ppos = pos
        if inst == 'N':
            pos = [pos[0], pos[1] - value]
        elif inst == 'S':
            pos = [pos[0], pos[1] + value]
        elif inst == 'E':
            pos = [pos[0] + value, pos[1]]
        elif inst == 'W':
            pos = [pos[0] - value, pos[1]]
        elif inst == 'L':
            rotation = ROTATIONS.get(value)
            if not rotation:
                raise Exception('Unknown rotation: %s %d' % (inst, value))
            direction = rotation(direction)
        elif inst == 'R':
            rotation = ROTATIONS.get(-value)
            if not rotation:
                raise Exception('Unknown rotation: %s %d' % (inst, value))
            direction = rotation(direction)
        elif inst == 'F':
            pos = [pos[0] + (direction[0] * value), pos[1] + (direction[1] * value)]
        else:
            raise Exception('Dont know what to do: %s %d' % (inst, value))

        #print(inst, value, direction, '|', ppos, ' -> ', pos)
    
    return abs(pos[0]) + abs(pos[1])
    

def part2(inpf):
    instructions = read_input(inpf)

    w_pos = [10, -1]
    s_pos = [0, 0]
    direction = [1, 0]  # facing east

    for inst, value in instructions:
        if inst == 'N':
            w_pos = [w_pos[0], w_pos[1] - value]
        elif inst == 'S':
            w_pos = [w_pos[0], w_pos[1] + value]
        elif inst == 'E':
            w_pos = [w_pos[0] + value, w_pos[1]]
        elif inst == 'W':
            w_pos = [w_pos[0] - value, w_pos[1]]
        elif inst == 'L':
            rotation = ROTATIONS.get(value)
            if not rotation:
                raise Exception('Unknown rotation: %s %d' % (inst, value))
            w_pos = rotation(w_pos)
        elif inst == 'R':
            rotation = ROTATIONS.get(-value)
            if not rotation:
                raise Exception('Unknown rotation: %s %d' % (inst, value))
            w_pos = rotation(w_pos)
        elif inst == 'F':
            s_pos = [s_pos[0] + (w_pos[0] * value), s_pos[1] + (w_pos[1] * value)]
        else:
            raise Exception('Dont know what to do: %s %d' % (inst, value))
    
    return abs(s_pos[0]) + abs(s_pos[1])





print('Part 1:', part1('input'))
print('Part 2:', part2('input'))