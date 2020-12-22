def read_input(inpf):
    player1 = []
    player2 = []

    player = None

    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.lower().startswith('player 1:'):
                player = 1
            elif line.lower().startswith('player 2:'):
                player = 2
            else:
                if player == 1:
                    player1.append(int(line))
                elif player == 2:
                    player2.append(int(line))
                else:
                    raise Exception('no player')
    
    return (player1, player2)



def play_crab_combat(player1, player2, recurse=False):
    seen = set()
    r = 1
    while True:
        if not player1:
            return 'p2', player2
        if not player2:
            return 'p1', player1

        if recurse:
            game = str(player1) + str(player2)
            if game in seen:
                return 'p1', player1
            seen.add(game)

        p1c = player1[0]
        p2c = player2[0]

        player1 = player1[1:]
        player2 = player2[1:]
        if recurse and p1c <= len(player1) and p2c <= len(player2):
            winner, _ = play_crab_combat(player1[0:p1c], player2[0:p2c], recurse)
        else:
            winner = 'p1' if p1c > p2c else 'p2'

        if winner == 'p1':
            player1.append(p1c)
            player1.append(p2c)
        else:
            player2.append(p2c)
            player2.append(p1c)
        r += 1
        



def part1(inpf):
    player1, player2 = read_input(inpf)
    winner, winner_cards = play_crab_combat(player1, player2, False)
    score = 0
    n = 1
    for i in range(0, len(winner_cards)):
        score += n*winner_cards[-(i+1)]
        n += 1

    print('Winner:', winner, 'with cards', winner_cards)
    return score


def part2(inpf):
    player1, player2 = read_input(inpf)

    winner, winner_cards = play_crab_combat(player1, player2, True)
    score = 0
    n = 1
    for i in range(0, len(winner_cards)):
        score += n*winner_cards[-(i+1)]
        n += 1

    print('Winner:', winner, 'with cards', winner_cards)
    return score


print('Part 1:', part1('input'))
print('Part 2:', part2('input'))