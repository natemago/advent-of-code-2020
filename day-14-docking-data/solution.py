import re

def read_input(inpf):
    program = []

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith('mask'):
                line = line.split(' = ')
                program.append(parse_mask(line[1]))
            else:
                match = re.match(r'^mem\[(?P<addr>\d+)\]\s+=\s+(?P<value>\d+)$', line)
                if not match:
                    raise Exception('Why not?' + line)
                program.append(('mem', {
                    'address': int(match.group('addr')),
                    'value': int(match.group('value'))
                }))


    return program

def parse_mask(mask):

    masks = []
    floating = []
    override = []
    M = 0xFFFFFFFFF
    n = len(mask) - 1
    for i in range(0, len(mask)):
        c = mask[i]
        if c == '1':
            masks.append(('or', 0x1<<n))
            override.append(n)
        elif c == '0':
            masks.append(('and', M^(0x1<<n)))
        else:
            floating.append(n)
        n -= 1
   
    
    def _apply_mask(value):
        v = value
        for op, m in masks:
            if op == 'and':
                value = value & m
            else:
                value = value | m
        return value
    
    return ('mask', {
        'mask': mask,
        'apply': _apply_mask,
        'masks': masks,
        'floating': floating,
        'override': override, 
    })


class TheChip:

    def __init__(self, program):
        self.program = program
        self.mask = None
        self.mask_data = None
        self.mem = {}
    
    def execute(self):
        for op, data in self.program:
            if op == 'mem':
                if not self.mask:
                    raise Exception('No mask?')
                value = self.mask(data['value'])
                self.mem[data['address']] = value
            elif op == 'mask':
                self.mask = data['apply']

    def execute_v2(self):
        for op, data in self.program:
            if op == 'mem':
                if not self.mask:
                    raise Exception('No mask?')
                value = data['value']
                for address in self.decode_addresses(data['address']):
                    self.mem[address] = value

            elif op == 'mask':
                self.mask = data['apply']
                self.mask_data = data
    
    def decode_addresses(self, address):
        M = 0xFFFFFFFFF
        addresses = []
        floating_bits = self.mask_data['floating']
        override = self.mask_data['override']
        

        for combination in combinations(floating_bits):
            curr_address = address
            for bit, value in combination:
                if value:
                    curr_address = curr_address | (0x1<<bit)
                else:
                    curr_address = curr_address & (M^(0x1<<bit))

            for bit in override:
                curr_address = curr_address | (0x1<<bit)
            
            addresses.append(curr_address)

        return addresses


def combinations(bits):
    def _combinations(bits, rest):
        if not bits:
            return rest
        b = bits[-1]
        nxt = []
        for v in (0, 1):
            for r in rest:
                nxt.append([(b, v)] + r)
        return _combinations(bits[0:-1], nxt)
    return _combinations(bits, [[]])


def part1(inpf):
    program = read_input(inpf)
    chip = TheChip(program)
    chip.execute()
    return sum(chip.mem.values())


def part2(inpf):
    program = read_input(inpf)
    chip = TheChip(program)
    chip.execute_v2()
    return sum(chip.mem.values())


print('Part 1:', part1('input'))
print('Part 2:', part2('input'))
