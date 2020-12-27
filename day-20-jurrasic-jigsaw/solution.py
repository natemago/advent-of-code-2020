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
    # result = []
    # for x in range(0, len(data[0])):
    #     row = ''
    #     for y in range(0, len(data)):
    #         row += data[y][x]
    #     result.append(row)

    # return result
    return [''.join([data[j][i] for j in range(len(data))]) for i in range(len(data[0])-1,-1,-1)]

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


def as_tiles(tiles_data):
    tiles = {}
    for tile_id, data in tiles_data.items():
        tiles[tile_id] = Tile(tile_id, data)
    return tiles

def tile_string(tile):
    result = '\n'.join(tile)
    return result


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
        
        self.all_edges = self._get_edges()
        self.edges_structured = self._edges_by_rotation()
        print(self.id, len(self.all_edges), 'edges')
    
    def _get_edges(self):
        result = []

        for r, edges in enumerate(self.edges):
            for idx, edge in enumerate(edges):
                result.append(TileEdge(edge, 'o', r, idx, self))
        
        for r, edges in enumerate(self.fedges):
            for idx, edge in enumerate(edges):
                result.append(TileEdge(edge, 'f', r, idx, self))

        return result
    
    def get_edges(self):
        return self.all_edges
    
    def _edges_by_rotation(self):
        result = {
            'o': [],
            'f': [],
        }
        
        for r, edges in enumerate(self.edges):
            row = []
            for idx, edge in enumerate(edges):
                row.append(TileEdge(edge, 'o', r, idx, self))
            result['o'].append(row)
        
        for r, edges in enumerate(self.fedges):
            row = []
            for idx, edge in enumerate(edges):
                row.append(TileEdge(edge, 'f', r, idx, self))
            result['f'].append(row)
        return result


class TileEdge:

    def __init__(self, edge, flip, direction, idx, tile):
        self.edge = edge
        self.flip = flip
        self.direction = direction
        self.idx = idx
        self.tile = tile
        self.matches = []
        self._key = '{edge} {flip}-{direction}-{idx} (@{tile})'.format(
            edge=self.edge,
            flip=self.flip,
            idx=self.idx,
            direction=self.direction,
            tile=self.tile.id,
        )
    
    def __repr__(self):
        return self._key
    
    def __str__(self):
        return self.__repr__()
    
    def __eq__(self, o):
        if o is None or not isinstance(o, TileEdge):
            return False
        return str(self) == str(o)

    def __hash__(self):
        return self._key.__hash__()


class E:

    # a -> b
    def __init__(self, av, bv, a, b):
        self.av = av
        self.bv = bv
        self.a = a
        self.b = b

    def __eq__(self, o):
        if o is None or not isinstance(o, E):
            return False
        return self.a == o.a and self.b == o.b
    
    def __hash__(self):
        return (str(self.a) + str(self.b)).__hash__()
    
    def __str__(self):
        return '{} -> {}'.format(self.a, self.b)
    
    def __repr__(self):
        return self.__str__()


class V:

    def __init__(self, tile):
        self.tile = tile
        self.oute = []
        self.ine= []

    def get_out_edges(self, flip, direction):
        result = []

        for edge in self.oute:
            if edge.b.direction == direction and edge.b.flip == flip:
                result.append(edge)

        return result
    
    def get_in_edges(self, flip, direction):
        result = set()

        for edge in self.ine:
            if edge.b.direction == direction and edge.b.flip == flip:
                result.add(edge)

        return result
    
    def __repr__(self):
        return 'V {}'.format(self.tile.id)
    
    def __str__(self):
        return self.__repr__()


class G:

    def __init__(self):
        self.edges = set()
        self.vertices = {}

    def add_vertex(self, tile):
        if tile.id in self.vertices:
            raise Exception('Vertex exists: ' + tile.id)
        self.vertices[tile.id] = V(tile)


    def get_vertex(self, tile_id):
        if tile_id not in self.vertices:
            raise Exception('No such vertex:' + tile_id)
        return self.vertices[tile_id]

    def add_edge(self, a, b):
        av = self.get_vertex(a.tile.id)
        bv = self.get_vertex(b.tile.id)
        edge = E(av, bv, a, b)
        if (edge, a, b) in self.edges:
            raise Exception('Edge exists: %s' % edge)
        av.oute.append(edge)
        bv.ine.append(edge)
        self.edges.add((edge, a, b))
        print('g: add edge', edge, a, '->', b)
    
    def __str__(self):
        return 'G: {} vertices, {} edges'.format(len(self.vertices), len(self.edges))
    
    def remove_vertices(self, vertices):
        ng = G()

        remove_edges = set()
        for v in vertices:
            remove_edges = remove_edges.union(v.oute).union(v.ine)
        
        for _, v in self.vertices.items():
            if v in vertices:
                continue
            ng.add_vertex(v.tile)
        
        for _, v in self.vertices.items():
            if v in vertices:
                continue
            for edge in v.oute:
                if edge in remove_edges:
                    continue
                ng.add_edge(edge.a, edge.b)
            
            # for edge in v.ine:
            #     if edge in remove_edges:
            #         continue
            #     ng.add_edge(edge.a, edge.b)
        
        return ng

    def from_vertices(self, vertices):
        ng = G()

        for v in vertices:
            ng.add_vertex(v.tile)

        for v in vertices:
            for edge in v.oute:
                if edge.av in vertices and edge.bv in vertices:
                    ng.add_edge(edge.a, edge.b)

        return ng


'''
  in direction n:
     n(0) -> f(2) for f in directions of tile 2
     n(1) -> 3
     2 -> 0
     3 -> 1

     general:
     n(i) for i in [0,3], for n in [0, 3] <=> f((i+2)%4) for f in [0, 3]
     n - direction of tile 1
     f - direction of tile 2
     i - edge number: 0 - top, 1 - right, 2 - down, 3 - left
'''
def build_graph(tiles):
    graph = G()
    ta = list(tiles.values())
    print(len(ta))
    for tile in ta:
        graph.add_vertex(tile)
    
    for i in range(0, len(ta)-1):
        for j in range(i+1, len(ta)):
            a = ta[i]
            b = ta[j]
            print('Compairing:', a.id, 'with', b.id)

            if a.id == b.id:
                raise Exception('What is this?')

            # aedges = a.get_edges()
            # bedges = b.get_edges()
            # print('Matching tile {} to tile {}:'.format(a.id, b.id))
            # c = 0
            # for ae in aedges:
            #     for be in bedges:
            #         #print(ae.edge, '==', be.edge)
            #         if ae.edge == be.edge:
            #             graph.add_edge(ae, be)
            #             graph.add_edge(be, ae)
            #             c += 1
            c = 0
            for fa in ['o', 'f']:
                for fb in ['o', 'f']:
                    aedges = a.edges_structured[fa]
                    bedges = b.edges_structured[fb]
                    
                    for ra in range(4):
                        for idx in range(4):
                            for rb in range(4):
                                ae = aedges[ra][idx]
                                be = bedges[rb][(idx+2)%4]
                                if ae.edge == be.edge:
                                    graph.add_edge(ae, be)
                                    graph.add_edge(be, ae)
                                    c += 1
            print('   ->', c, 'possible matchings.')
    
    return graph


def walk_graph(graph):
    possible = []
    q = []

    total = len(graph.vertices)

    for _, v in graph.vertices.items():
        for flip in ['o', 'f']:
            for d in range(0, 4):
                q.append((v, flip, d, {v}, []))
    cnt = 1
    tote = 0
    best = 0
    while q:
        currv, flip, direction, seen, backtrack = q.pop()
        if len(seen) == total - 1:
            #print('STOP!', cnt)
            #print(backtrack, ' + ', currv)
            possible.append(backtrack)
            
        # if currv in seen:
        #     continue
        if best < len(seen):
            best = len(seen)
        for edge in currv.get_out_edges(flip, direction):
            tote += 1
            if edge.bv not in seen:
                q.append((edge.bv, edge.b.flip, edge.b.direction, seen.union({currv}), backtrack + [edge]))

        if cnt % 100000 == 0:
            #print('Average out edges:', tote/cnt)
            print('Seen', len(seen), '; iters=', cnt, 'q=',len(q), 'best=', best)
        cnt += 1
    
    return possible

'''
  a b c
  d e f
  g h i


  a b c d e f g h i
a x 1 0 1 0 0 0 0 0
b 1 x 1 0 1 0 0 0 0
c 0 1 x 0 0 1 0 0 0
d 1 0 0 x 1 0 1 0 0
e 0 1 0 1 x 1 0 1 0
f 0 0 1 0 1 x 0 0 1
g 0 0 0 1 0 0 x 1 0
h 0 0 0 0 1 0 1 x 1
i 0 0 0 0 0 1 0 1 x

'''

def dumb_walk(v, flip, direction, seen):
    edges = v.get_out_edges(flip, direction)
    if edges:
        for edge in edges:
            if edge.bv in seen:
                continue
            path = dumb_walk(edge.bv, edge.b.flip, edge.b.direction, seen.union({v}))
            print(len(seen))
            if path:
                return [v] + path
    return None


def strip_border(graph):
    corners = set()
    borders = set()
    inner = set()
    for _, v in graph.vertices.items():
        for flip in ['o', 'f']:
            for d in range(4):
                edges = v.get_out_edges(flip, d)
                if len(edges) == 2:
                    corners.add(v)
                elif len(edges) == 3:
                    borders.add(v)
                elif len(edges) == 4:
                    inner.add(v)
    return corners, borders, inner


def write_tile(tile, x, y, pixels, flp, direction):
    data = tile.data if flp == 'o' else flip(tile.data)
    while direction:
        data = rot(data)
        direction -= 1

    for i in range(len(data)):
        for j in range(len(data[0])):
            xx = j+x
            yy = i+y
            pixels[(xx, yy)] = data[i][j]
    



def reconstruct(track):
    pixels = {}
    tiles = {}

    edge = track[0].a
    tiles[(0, 0)] = edge.tile
    write_tile(edge.tile, 0, 0, pixels, edge.flip, edge.direction)

    tile_size = len(edge.tile.data)
    tx, ty = (0, 0)
    for edge in track:
        edge = edge.b
        vx, vy = ([0, 1], [1, 0], [0, -1], [-1, 0])[edge.idx]
        write_tile(edge.tile, (tx + vx)*tile_size, (ty + vy)*tile_size, pixels, edge.flip, edge.direction)
        tx += vx
        ty += vy
        tiles[(tx, ty)] = edge.tile
    
    return tiles, pixels


def print_reconstruction(pixels):
    lx = min(pixels.keys(), key=lambda k: k[0])[0]
    ly = min(pixels.keys(), key=lambda k: k[1])[1]
    hx = max(pixels.keys(), key=lambda k: k[0])[0]
    hy = max(pixels.keys(), key=lambda k: k[1])[1]

    #print(pixels)

    result = ''

    for y in range(ly, hy+1):
        for x in range(lx, hx+1):
            result += pixels.get((x, y), ' ')
        result += '\n'
    return result

def part1(inpf):
    tiles = as_tiles(read_input(inpf))
    
    for tid, tile in tiles.items():
        print(tid, tile.id)
    
    graph = build_graph(tiles)
    print(len(tiles), 'tiles')
    print(graph)
    

    #walk_graph(graph)
    # #data = list(tiles.values())[0].data
    # '''
    # 123
    # 456 
    # 789
    
    # rot 90:
    # 369
    # 258
    # 147
    # '''
    # data = [
    #     '123',
    #     '456',
    #     '789',
    # ]
    # print(tile_string(data))
    # print('-----------')
    # data = rot(data)
    # print(tile_string(data))
    # data = rot(data)
    # print('-----------')
    # print(tile_string(data))
    # data = rot(data)
    # print('-----------')
    # print(tile_string(data))
    # data = rot(data)

    # Part 1 solution
    # ========================
    # p1 = set()
    # borders = set()
    # inner = set()
    # for _, v in graph.vertices.items():
    #     for flip in ['o', 'f']:
    #         for d in range(4):
    #             edges = v.get_out_edges(flip, d)
    #             if len(edges) == 2:
    #                 print('Possible puzzle corner: ', v.tile.id, flip, d)
    #                 p1.add(v.tile.id)
    #             elif len(edges) == 3:
    #                 print('Possible puzzle border:', v.tile.id, flip, d)
    #                 borders.add(v.tile.id)
    #             elif len(edges) == 4:
    #                 inner.add(v.tile.id)
    

    # print('Corners: ', len(p1), p1)
    # print('Borders: ', len(borders), ' ->', borders)
    # print('Inner:', len(inner))


    # # let's start from a corner tile
    # configuration = None
    # for v in p1:
    #     v = graph.vertices[v]
    #     for flip in ['o', 'f']:
    #         for direction in range(4):
    #             t = dumb_walk(v, flip, direction, {v})
    #             if t:
    #                 print('Got one!', t)
    #                 configuration = t
    #                 break
    

    # result = 1
    # for p in p1:
    #     result *= int(p)
    # return result


    total_to_check = 1
    while graph.vertices:
        corners, borders, inner = strip_border(graph)
        print('-------------------------------')
        print('Corners: ', len(corners))
        print('Borders: ', len(borders))
        print('Inner: ', len(inner))
        print('Total: ', len(corners) + len(borders) + len(inner), '; Graph: ', len(graph.vertices))
        graph = graph.remove_vertices(corners.union(borders))
        border_graph = graph.from_vertices(corners.union(borders))
        possible = walk_graph(border_graph)
        print('Possible: ', len(possible) / len(corners.union(borders)))

        total_to_check *= len(possible) / len(corners.union(borders))
        for track in possible:
            tls, pixels = reconstruct(track)
            print('---------------------------------------------------')
            #
            if len(tls) < 10:
                print(tls)
                print(print_reconstruction(pixels))
            
    
    print('Total to check:', total_to_check)



print('Part 1: ', part1('test_input'))
