def read_input(inpf):
    messages = []
    rules = {}

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ':' in line:
                # parse rule
                line = line.split(':')
                rule_id = line[0]
                rule = line[1].strip()
                if '"' in rule:
                    rules[rule_id] = (rule[1:-1], None, None)
                elif '|' in rule:
                    alternatives = rule.split('|')
                    alt_1 = alternatives[0].split()
                    alt_2 = alternatives[1].split()
                    rules[rule_id] = (None, alt_1, alt_2)
                else:
                    rule = rule.split()
                    rules[rule_id] = (None, rule, None)
            else:
                messages.append(line)
    return rules, messages

class Node:

    def __init__(self, rule_id, exact=None):
        self.rid = rule_id
        self.exact = exact
        self.alt1 = []
        self.alt2 = []
    
    def to_str(self, seen):
        if self.exact:
            return self.exact
        if seen and self.rid in seen:
            return '#' + self.rid
        if seen is not None:
            seen.add(self.rid)

        alt1str = ''
        for c in self.alt1:
            alt1str += c.to_str(seen)
        
        alt2str = ''
        for c in (self.alt2 or []):
            alt2str += c.to_str(seen)

        if alt2str:
            return '((%s)|(%s))' % (alt1str, alt2str)
        return '%s' % alt1str
    

    def part2_regex(self):
        if self.exact:
            return self.exact

        alt1str = ''
        for c in self.alt1:
            alt1str += c.part2_regex()
        
        alt2str = ''
        for c in (self.alt2 or []):
            if self.rid == '8':
                if c.rid == '8':
                    continue
                else:
                    alt2str += '(' + c.part2_regex() + ')+'
            elif self.rid == '11':
                continue
            else:
                alt2str += c.part2_regex()

        if self.rid == '11':
            alt2str = []
            g1 = self.alt2[0].part2_regex()
            g2 = self.alt2[2].part2_regex()
            for i in range(0, 10):
                alt2str.append('((%s){%d}(%s){%d})' % (g1, i+1, g2, i+1))
            
            alt2str = '|'.join(alt2str)


        if alt2str:
            return '((%s)|(%s))' % (alt1str, alt2str)
        return '%s' % alt1str

    def _match_exact(self, value):
        result = self.exact if value.startswith(self.exact) else None
        self.print(' ::[x]', value,  '->', result)
        return result


    def print(self, *args, **kwargs):
        #print(' (%3s)' % self.rid, *args, **kwargs)
        pass

    def _match(self, value, recur=0):
        if self.exact:
            return self._match_exact(value)

        ralt1 = self._match_alt(self.alt1, value)
        ralt2 = self._match_alt(self.alt2, value)

        if len(ralt1 or '') > len(ralt2 or ''):
            return ralt1
        return ralt2

    def _match_alt(self, alts, value, recur=0):
        if not alts:
            self.print(' '*recur, ' ::[a] no alts, None')
            return None
        result = ''
        for a in alts:
            if not value:
                return None
            matched = a._match(value, recur+5)
            if matched is None:
                return None
            value = value[len(matched):]
            result += matched
        self.print(' '*recur, ' ::[a]', value, '->', result)
        return result
        

    def match(self, value):
        result = self._match(value)
        return result == value


def rules_tree(rules):
    nodes = {}
    for rule, values in rules.items():
        nodes[rule] = Node(rule, values[0])
    
    for rule, values in rules.items():
        node = nodes[rule]
        _, alt1, alt2 = values

        for a in (alt1 or []):
            node.alt1.append(nodes[a])

        for a in (alt2 or []):
            node.alt2.append(nodes[a])
    
    return nodes['0']



def part1(inpf):
    rules, messages = read_input(inpf)
    tree = rules_tree(rules)

    print(tree.to_str(None))

    count = 0
    for message in messages:
        if tree.match(message):
             count += 1
    
    return count



def part2(inpf):
    rules, messages = read_input(inpf)

    rules['8'] = (None, ['42'], ['42', '8'])
    rules['11'] = (None, ['42', '31'], ['42', '11', '31'])

    tree = rules_tree(rules)

    import re
    regex = tree.part2_regex()
    #print(regex)

    count = 0
    for message in messages:
        if re.match('^' + regex + '$', message):
            print(message)
            count += 1
    return count


print('Part 1: ', part1('input'))
print('Part 2: ', part2('input'))