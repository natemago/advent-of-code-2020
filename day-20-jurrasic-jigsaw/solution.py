def read_input(inpf):
    images = {}

    with open(inpf) as f:
        image_id = None
        image = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('tile'):
                if image and image_id is not None:
                    images[image_id] = image
                image_id = line.split()[1][:-1]
                image = []
            else:
                image.append(line)
        
        if image:
            images[image_id] = image

    return images


def get_edges(data):
    return [
        data[0],
        ''.join([c[-1] for c in data]),
        data[-1],
        ''.join([c[0] for c in data]),
    ]

def rot(data):
    result = []
    for x in range(0, len(data[0])):
        row = ''
        for y in range(0, len(data)):
            row += data[y][x]
        result.append(row)

    return result

def flip(data):
    result = []
    for row in data:
        result.append(''.join(list(reversed(row))))
    return result

def to_num(edge):
    n = 0

    for i in range(0, len(edge)):
        if edge[i] == '#':
            n += 2**(len(edge) - i - 1)

    return n


class Tile:

    def __init__(self, id, data):
        self.id = id
        self.data = data
        self.direction = 0
        self.flipped = False
        self.edges = []
        for _ in range(0, 4):
            self.edges.append([edge for edge in get_edges(data)])
            data = rot(data)
        self.fedges = []
        data = flip(data)
        for _ in range(0, 4):
            self.fedges.append([edge for edge in get_edges(data)])
            data = rot(data)
        
        self.matched = {}
        self.all_edges = None
    
    def match_edge(self, edge):
        matches = []
        for r in range(0, len(self.edges)):
            for i in range(0, len(self.edges[r])):
                if edge == self.edges[r][i]:
                    matches.append(('o', r, i))
        
        for r in range(0, len(self.fedges)):
            for i in range(0, len(self.fedges[r])):
                if edge == self.fedges[r][i]:
                    matches.append(('f', r, i))
        return matches

    def all_possible_edges(self):
        all_edges = []
        for edges in self.edges + self.fedges:
            all_edges += edges
        
        return all_edges
    
    def get_all_edges(self):
        if self.all_edges:
            return self.all_edges
        result = []

        for d, edges in enumerate(self.edges):
            for i, edge in enumerate(edges):
                result.append(Edge(edge, 'o', d, i, self))
        
        for d, edges in enumerate(self.fedges):
            for i, edge in enumerate(edges):
                result.append(Edge(edge, 'f', d, i, self))
        
        self.all_edges = result
        return result
    
    def get_edges(self):
        if self.flipped:
            return [
                (edge, i, self) for i, edge in enumerate(self.fedges[self.direction])
            ]
        return [
            (edge, i, self) for i, edge in enumerate(self.edges[self.direction])
        ]
    
    def match_to_tile(self, tile):
        my_edges = self.get_edges()
        other = tile.get_edges()
        match_points = []
        for i in range(0, 4):
            if other[(i+2)%4] == my_edges[i]:
                match_points.append(i)
        return match_points

    def can_match_any(self, edges):
        my_edges = self.get_edges()
        result = []
        for edge, idx, tile in edges:
            me, midx, _ = my_edges[(idx+2) % 4]
            if edge == me:
                result.append(((edge, idx, tile),(me, midx, self)))
        return result
    
    def match_tile(self, tile):
        for te in tile.get_all_edges():
            for me in self.get_all_edges():
                if te.tile.id == me.tile.id:
                    raise Exception('boom')
                if te.edge == me.edge:
                    print('>', te, me)
                    te.matches.append(me)
                    me.matches.append(te)


class Edge:

    def __init__(self, edge, flip, direction, idx, tile):
        self.edge = edge
        self.flip = flip
        self.direction = direction
        self.idx = idx
        self.tile = tile
        self.matches = []
    
    def __repr__(self):
        return self.edge + '(' + self.tile.id + ')'
    
    def __str__(self):
        return self.__repr__()


def as_tiles(tiles_data):
    tiles = {}
    for tile_id, data in tiles_data.items():
        tiles[tile_id] = Tile(tile_id, data)
    return tiles


def are_we_done(space, total):
    if len(space) == total:
        minx = min(space.values(), key=lambda k: k[0])
        maxx = max(space.values(), key=lambda k: k[0])
        miny = min(space.values(), key=lambda k: k[1])
        maxy = max(space.values(), key=lambda k: k[1])

        return (maxx - minx) == (maxy - miny)
    return False 

def match_tile(tiles, eq, space, total):
    if not tiles:
        return are_we_done(space, total)
    nt = tiles[0]
    print('@', nt.id)
    for flip in (False, True):
        for d in range(0, 4):
            nt.direction = d
            nt.flipped = flip

            matches = nt.can_match_any(eq)
            if not matches:
                return False
            for eq_match, tile_match in matches:
                put_edges = nt.get_edges()
                put_edges.remove(tile_match)
                neq = eq + []
                neq.remove(eq_match)
                nspace = {}
                nspace.update(space)

                x,y = space[eq_match[2]]
                wall = tile_match[1]
                if wall == 0:
                    nspace[nt] = (x, y-1)
                elif wall == 1:
                    nspace[nt] = (x+1, y)
                elif wall == 2:
                    nspace[nt] = (x, y+1)
                else:
                    nspace[nt] = (x-1, y)

                if match_tile(tiles[1:], neq + put_edges, nspace, total):
                    return True
    
    return False

            


def part1(inpf):
    tiles = as_tiles(read_input(inpf))

    tiles_list = list(tiles.values())
    # space = {
    #     tiles_list[0]: (0, 0)
    # }
    # eq = tiles_list[0].get_edges()
    # total = len(tiles)

    # return match_tile(tiles_list[1:],eq, space, total)
    for i in range(0, len(tiles_list) - 1):
        for j in range(i+1, len(tiles_list)):
            t1 = tiles_list[i]
            t2 = tiles_list[j]
            t1.match_tile(t2)

    corners = set()
    for tile in tiles_list:
        grouped = {}
        for edge in tile.get_all_edges():
            key = '{}-{}'.format(edge.flip, edge.direction)
            grouped[key] = grouped.get(key, []) + edge.matches
        print(tile.id, grouped)
        for key, edges in grouped.items():
            if len(edges)//4 == 2:
                print(tile.id, 'might be a corner @', key)
                corners.add(int(tile.id))
            elif len(edges)//4 == 3:
                print(tile.id, 'might be an edge tile @', key)
            else:
                #print(len(edges))
                pass
    result = 1
    for c in corners:
        result *= c
    print(corners)
    return result

print('Part 1:', part1('input'))