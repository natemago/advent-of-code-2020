def part1(numbers, turns=2020):
    spoken = {}

    for i in range(0, len(numbers)):
        spoken[numbers[i]] = (i, i)
    
    turn = len(numbers)
    last = numbers[-1]

    while turn < turns:
        last_spoken, before_that = spoken.get(last, (turn, turn))
        
        say_word = last_spoken - before_that

        say_word_last_spoken = spoken.get(say_word, (turn, turn))[0]

        spoken[say_word] = (turn, say_word_last_spoken)

        last = say_word
        if turn % 1000000 == 0:
            print('  still working...')
        turn += 1

    return last

def f(arg):
    for i in range(0, 19):
        pass
    print(i)


def part1(numbers, turns=2020):
    spoken = {}

    for i in range(0, len(numbers) - 1):
        spoken[numbers[i]] = i
    
    turn = len(numbers) - 1
    last = numbers[-1]
    while turn < turns - 1:
        seen_at = spoken.get(last)
        if seen_at is None:
            say = 0
        else:
            say = turn - seen_at
        
        spoken[last] = turn
        last = say

        turn += 1

    return last




INPUT = [0,8,15,2,12,1,4]
TEST_INPUT = [0,3,6]

# print('Part 1:', part1(INPUT))
# print('Part 2:', part1(INPUT, 30000000))
f(True)
        