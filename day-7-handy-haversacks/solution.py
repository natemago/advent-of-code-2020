import re

def read_input(inpf):
    bags = {}

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if line:
                line = line.split('contain')
                holder = re.match(r'^(?P<holder>[\w\s]+)\s+bags$', line[0].strip())
                if not holder:
                    raise Exception('Why not?:' + line)
                holder = holder.group('holder')
                bags[holder] = {}
                if line[1].strip() != 'no other bags.':
                    for contains in line[1].strip().split(','):
                        m = re.search(r'(?P<how_many>\d+)\s+(?P<bag_type>[\w\s]+)\s+bags?', contains.strip())
                        if not m:
                            raise Exception('Why not contain this?: ' + line[1] + ' :: ' + contains)
                        bags[holder][m.group('bag_type')] = int(m.group('how_many'))

    return bags

class V:

    def __init__(self, name):
        self.name = name
        self.in_edges = []
        self.out_edges = []
        self.payload=  {}

class E:

    def __init__(self, a, b, w=None):
        self.a = a
        self.b = b
        self.w = w

    def __eq__(self, o):
        if isinstance(o, E):
            return self.a == o.a and self.b == o.b and self.w == o.w
        return False

class G:

    def __init__(self):
        self.vertices = {}
        self.edges = []

    def add_v(self, v):
        self.vertices[v.name] = v
    
    def get_v(self, name):
        v = self.vertices[name]
        if not v:
            raise Exception('No such vertex: ' + name)
        return v
    
    def add_edge(self, a_name, b_name, weight):
        a = self.get_v(a_name)
        b = self.get_v(b_name)
        edge = E(a, b, weight)
        if edge in self.edges:
            raise Exception('Edge already added: ' + edge)
        a.out_edges.append(edge)
        b.in_edges.append(edge)
        self.edges.append(edge)
        return edge


def build_graph(bags):
    graph = G()

    for bag_type in bags.keys():
        graph.add_v(V(bag_type))
    
    for a_name, contains in bags.items():
        for b_name, weight in contains.items():
            graph.add_edge(a_name, b_name, weight)

    return graph


def part1(inpf):
    bags = read_input(inpf)
    graph = build_graph(bags)

    def _visit(vertex):
        if vertex.payload.get('marked'):
            return
        vertex.payload['marked'] = True
        for edge in vertex.in_edges:
            _visit(edge.a)
    
    shiny_gold_bag = graph.get_v('shiny gold')
    _visit(shiny_gold_bag)

    return len(list(filter(lambda v: v.payload.get('marked'), graph.vertices.values()))) - 1


def part2(inpf):
    bags = read_input(inpf)
    graph = build_graph(bags)

    def _count_required(vertex):
        total = 1  # This one

        for edge in vertex.out_edges:
            total += edge.w * _count_required(edge.b)

        return total
    
    shiny_gold_bag = graph.get_v('shiny gold')
    
    return _count_required(shiny_gold_bag) - 1  # not counting the shiny gold bag


print('Part 1:', part1('input'))
print('Part 2:', part2('input'))