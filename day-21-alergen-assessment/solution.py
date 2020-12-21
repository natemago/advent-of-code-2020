def read_input(inpf):
    foods = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if '(contains' in line:
                parts = line.split('(contains')
                ingridients = [p.strip() for p in parts[0].strip().split()]
                alergens = [p.strip() for p in parts[1][:-1].strip().split(',')]
                foods.append((ingridients, alergens))
            else:
                foods.append(([p.strip() for p in line.strip().split()], []))
    return foods


def part1(inpf):
    foods = read_input(inpf)

    all_ingridients = set()
    alergenic = {}
    for ingridients, alergens in foods:
        ingridients_set = set(ingridients)
        for alergen in alergens:
            may_contain_alergen = alergenic.get(alergen, ingridients_set)
            alergenic[alergen] = may_contain_alergen.intersection(ingridients_set)
        all_ingridients = all_ingridients.union(ingridients_set)
    
    alergenic_ingridients = set()
    for alergen, ingridients in alergenic.items():
        alergenic_ingridients = alergenic_ingridients.union(ingridients)
    non_alergenic = all_ingridients.difference(alergenic_ingridients)

    count = 0
    for ingridients, _ in foods:
        for ingr in ingridients:
            if ingr in non_alergenic:
                count += 1
    return count


def part2(inpf):
    foods = read_input(inpf)

    alergenic = {}
    for ingridients, alergens in foods:
        ingridients_set = set(ingridients)
        for alergen in alergens:
            may_contain_alergen = alergenic.get(alergen, ingridients_set)
            alergenic[alergen] = may_contain_alergen.intersection(ingridients_set)
    
    result = []

    while alergenic:
        for alergen, ingridients in alergenic.items():
            for oa, oi in alergenic.items():
                if alergen == oa:
                    continue
                ingridients = ingridients.difference(oi)

            if len(ingridients) == 1:
                result.append((alergen, list(ingridients)[0]))
                del alergenic[alergen]
                break

    
    result = ','.join([k[1] for k in sorted(result, key=lambda k: k[0])])

    return result



print('Part 1:', part1('input'))
print('Part 2:', part2('input'))