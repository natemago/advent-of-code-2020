import re
def read_input(inpf):
    validation_classes = {}
    my_ticket = []
    nearby_tickets = []

    curr_reading = 'validation'

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('your ticket'):
                curr_reading = 'my-ticket'
                continue
            if line.startswith('nearby tickets'):
                curr_reading = 'nearby'
                continue

            if curr_reading == 'validation':
                m = re.match(r'^(?P<name>[\w\s]+):\s(?P<r11>\d+)-(?P<r12>\d+)\s+or\s+(?P<r21>\d+)-(?P<r22>\d+)$', line)
                if not m:
                    raise Exception('Not a validation class? ' + line)
                validation_classes[m.group('name')] = [(int(m.group('r11')), int(m.group('r12'))), (int(m.group('r21')), int(m.group('r22')))]
            elif curr_reading == 'my-ticket':
                my_ticket = [int(n.strip()) for n in line.split(',')]
            elif curr_reading == 'nearby':
                nearby_tickets.append([int(n.strip()) for n in line.split(',')])
    
    return {
        'rules': validation_classes,
        'my-ticket': my_ticket,
        'nearby': nearby_tickets,
    }


def generate_validation_rules(rules):
    result = []

    def _validation(a, b):

        def _check_rule(value):
            result = value >= a and value <= b
            #print('  ', value, 'between', a, 'and', b, ':', result)
            return result

        return _check_rule

    for rule_name, ranges in rules.items():
        result.append((rule_name, [_validation(*r) for r in ranges]))

    return result


def part1(inpf):
    data = read_input(inpf)
    validations = generate_validation_rules(data['rules'])

    result = 0
    for ticket in data['nearby']:
        for value in ticket:
            valid = False
            for rule, validfns in validations:
                for vfn in validfns:
                    if vfn(value):
                        valid = True
                        break

            if not valid:
                result += value
    return result



def is_ticket_valid(rules, ticket):
    for value in ticket:
        is_valid = False
        for rule, validfns in rules:
            for validfn in validfns:
                if validfn(value):
                    is_valid = True

        if not is_valid:
            return False
    return True


def check_if_rule_apply(rule_validations, tickets, column):
    for i in range(0, len(tickets)):
        value = tickets[i][column]
        valid = False
        for vfn in rule_validations:
            if vfn(value):
                valid = True
                break
        if not valid:
            return False
    return True


def part2(inpf):
    data = read_input(inpf)
    rules = data['rules']
    validations = generate_validation_rules(rules)

    tickets = list(filter(lambda ticket: is_ticket_valid(validations, ticket), data['nearby']))

    possible_locations = {}

    for rule, rule_validations in validations:
        for column in range(0, len(tickets[0])):
            if check_if_rule_apply(rule_validations, tickets, column):
                possible_locations[rule] = possible_locations.get(rule, []) + [column]

    final_locations = {}
    while possible_locations:
        
        for rule, locations in possible_locations.items():
            rule_unique = set(locations)
            for orule, olocations in possible_locations.items():
                if rule == orule:
                    continue
                if not rule_unique:
                    continue
                rule_unique = rule_unique.difference(set(olocations))
            if len(rule_unique) == 1:
                final_locations[rule] = list(rule_unique)[0]
                del possible_locations[rule]
                break
    print('Final locations:', final_locations)
    result = 1
    for rule, location in final_locations.items():
        if rule.startswith('departure'):
            result *= data['my-ticket'][location]
    return result



print('Part 1:', part1('input'))
print('Part 2:', part2('input'))