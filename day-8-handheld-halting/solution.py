def read_input(inpf):
    mem = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if line:
                line = line.split()
                if len(line) != 2:
                    raise Exception('Invalid op:', line)
                mem.append((line[0], int(line[1])))
    return mem


def part1(inpf):
    mem = read_input(inpf)
    pc = 0
    a = 0
    seen = set()
    while True:
        op, value = mem[pc]
        if pc in seen:
            return a
        seen.add(pc)
        if op == 'nop':
            pc += 1
        elif op == 'acc':
            a += value
            pc += 1
        elif op == 'jmp':
            pc += value
        else:
            raise Exception('Unknown opcode: %s (value=%d)' % (op, value))


def part2(inpf):

    def _detect_loop(mem):
        pc = 0
        a = 0
        seen = set()
        while True:
            if pc < 0 or pc >= len(mem):
                return (False, a)
            op, value = mem[pc]
            if pc in seen:
                return (True, a)
            seen.add(pc)
            if op == 'nop':
                pc += 1
            elif op == 'acc':
                a += value
                pc += 1
            elif op == 'jmp':
                pc += value
            else:
                raise Exception('Unknown opcode: %s (value=%d)' % (op, value))
    
    mem = read_input(inpf)
    for i in range(0, len(mem)):
        op, value = mem[i]
        if op in ['jmp', 'nop']:
            cmem = [v for v in mem]
            cop = 'jmp' if op == 'nop' else 'nop'
            cmem[i] = (cop, value)
            
            loop, acc_value = _detect_loop(cmem)
            if not loop:
                return acc_value



print('Part 1: ', part1('input'))
print('Part 2: ', part2('input'))
