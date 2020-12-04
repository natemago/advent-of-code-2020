import re


def read_input(inpf):
    passports = []

    def _parse_passport(buff):
        entries = filter(lambda e: e, map(lambda e: e.strip(), buff.split()))
        passport = {}
        for entry in entries:
            entry = entry.split(':')
            passport[entry[0].strip()] = entry[1].strip()
        return passport

    with open(inpf) as f:
        passp_buff = ''
        for line in f:
            line = line.strip()
            if not line and passp_buff:
                passports.append(passp_buff)
                passp_buff = ''
            else:
                passp_buff += ' ' + line

        if passp_buff:
            passports.append(passp_buff)

    return map(_parse_passport, passports)


def part1(inpf):
    passports = read_input(inpf)
    valid = 0
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for passport in passports:
        is_valid = True
        for field in required:
            if field not in passport or not passport.get(field):
                is_valid = False
                break
        if is_valid:
            valid += 1
    return valid


def part2(inpf):
    passports = read_input(inpf)
    valid = 0
    required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    for passport in passports:
        is_valid = True
        for field in required:
            if field not in passport or not passport.get(field):
                is_valid = False
                break
            value = passport[field]
            if field == 'byr':
                if not (re.match(r'^\d{4}$', value) and '1920' <= value and value <= '2020'):
                    is_valid = False
                    break
            elif field == 'iyr':
                if not (re.match(r'^\d{4}$', value) and '2010' <= value and value <= '2020'):
                    is_valid = False
                    break
            elif field == 'eyr':
                if not (re.match(r'^\d{4}$', value) and '2020' <= value and value <= '2030'):
                    is_valid = False
                    break
            elif field == 'hgt':
                if not re.match(r'^\d+(cm|in)$', value):
                    is_valid = False
                    break
                unit = value[-2:]
                value = int(value[:-2])
                if not ((unit == 'cm' and value >= 150 and value <= 193) or (unit == 'in' and value >= 59 and value <= 76)):
                    is_valid = False
                    break
            elif field == 'hcl':
                if not re.match(r'^#[0-9a-f]{6}$', value):
                    is_valid = False
                    break
            elif field == 'ecl':
                if not value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                    is_valid = False
                    break
            elif field == 'pid':
                if not re.match(r'^\d{9}$', value):
                    is_valid = False
                    break

        if is_valid:
            valid += 1
    return valid


print('Part 1:', part1('input'))
print('Part 2:', part2('input'))