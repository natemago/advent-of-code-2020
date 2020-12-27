
def read_input(inpf):
    with open(inpf) as f:
        card = int(f.readline().strip())
        door = int(f.readline().strip())
        return (card, door)



def solution(inpf):
    card, door = read_input(inpf)
    print('Card:', card, ', door:', door)
    sn = 1
    e = 1
    while True:
        sn *= 7
        sn = sn % 20201227
        if sn == card or sn == door:
            print('Found one:', e)
            sk = card if sn == door else door

            return pow(sk, e, 20201227)
        e += 1

print('Solution:', solution('input'))
        
