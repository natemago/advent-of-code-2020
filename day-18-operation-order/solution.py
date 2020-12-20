def read_input(inpf):
    expressions = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            expressions.append((parse_expr(line), line))
    return expressions

def parse_expr(expr):
    result = []
    for c in expr.strip():
        if c == ' ':
            continue
        if c == '(':
            result.append(('lparen', c))
        elif c == ')':
            result.append(('rparen', c))
        elif c in ['*', '+']:
            result.append(('op', c))
        else:
            result.append(('num', int(c)))
    return result


def to_rpn(expression, precedence):
    out = []
    op_stack = []
    for token, value in expression:
        if token == 'num':
            out.append(('num', value))
            continue
        if token == 'op':
            while op_stack:

                ops_type, ops_value = op_stack[-1]
                if ops_type != 'op':
                    break
                
                ops_prec = precedence[ops_value]
                curr_prec = precedence[value]
                if ops_prec < curr_prec:
                    break
                # if op_stack[-1][0] == 'lparen':
                #     break
                out.append(op_stack.pop())
            op_stack.append(('op', value))
            continue
        if token == 'lparen':
            op_stack.append(('lparen', value))
            continue
        if token == 'rparen':
            while op_stack:
                if op_stack[-1][0] == 'lparen':
                    break
                out.append(op_stack.pop())
            if op_stack[-1][0] == 'lparen':
                op_stack.pop()
    
    while op_stack:
        if op_stack[-1][0] == 'lparen':
            raise Exception('Mismatched parentesis')
        out.append(op_stack.pop())
    
    return out


def evaluate(rpn_expression):
    stack = []
    for token, value in rpn_expression:
        if token == 'op':
            if len(stack) < 2:
                raise Exception('Invalid expression')
            a = stack.pop()
            b = stack.pop()
            if value == '+':
                stack.append(a+b)
            else:
                stack.append(a*b)
        elif token == 'num':
            stack.append(value)
        else:
            raise Exception('Woops, invalid token:', (token, value))
    if len(stack) != 1:
        raise Exception('Invalid expression')
    return stack[0]


def part1(inpf):
    precedence = {
        '+': 1,
        '*': 1,
    }
    total = 0
    for expression, line in read_input(inpf):
        total += evaluate(to_rpn(expression, precedence))
    return total


def part2(inpf):
    precedence = {
        '+': 2,
        '*': 1,
    }
    total = 0
    for expression, line in read_input(inpf):
        total += evaluate(to_rpn(expression, precedence))
    return total

print('Part 1:', part1('input'))
print('Part 2:', part2('input'))
                


