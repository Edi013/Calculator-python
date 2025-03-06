from collections import deque


# Operator class to hold precedence and arguments
class Operator:
    def __init__(self, precedence, arguments):
        self.precedence = precedence
        self.arguments = arguments


# Mapping of operators and their precedence
operator_map = {
    '/': Operator(4, 2),
    '*': Operator(3, 2),
    '+': Operator(2, 2),
    '-': Operator(1, 2)
}


# Expression to be evaluated
expression = "-((1+2)/((6*-7)+(7*-4)/2)-3)"


# Symbol class to represent different types of symbols in the expression
class Symbol:
    class Type:
        Unknown = 0
        Literal_Numeric = 1
        Operator = 2
        Parenthesis_Open = 3
        Parenthesis_Close = 4

    def __init__(self, symbol="", symbol_type=Type.Unknown, op=None):
        self.symbol = symbol
        self.type = symbol_type
        self.op = op if op else Operator(0, 0)


# Parser
# Initialize stacks
stkHolding = deque()  # Holding stack for operators and parentheses
stkOutput = deque()  # Output stack for RPN
symPrevious = Symbol("0", Symbol.Type.Unknown)
pass_num = 0

# Process the expression
for c in expression:
    if c.isdigit():
        # Push literals directly to output
        stkOutput.append(Symbol(symbol=str(c), symbol_type=Symbol.Type.Literal_Numeric))
        symPrevious = stkOutput[-1]
    elif c == '(':
        # Push open parenthesis to holding stack
        stkHolding.appendleft(Symbol(symbol=str(c), symbol_type=Symbol.Type.Parenthesis_Open))
        symPrevious = stkHolding[0]
    elif c == ')':
        # Backflush holding stack into output until open parenthesis
        while len(stkHolding) != 0 and stkHolding[0].type != Symbol.Type.Parenthesis_Open:
            stkOutput.append(stkHolding.popleft())

        if len(stkHolding) == 0:
            print(f"!!!! ERROR! Unexpected parenthesis '{c}'")
            exit(0)

        # Remove the corresponding open parenthesis
        stkHolding.popleft()
        symPrevious = Symbol(symbol=str(c), symbol_type=Symbol.Type.Parenthesis_Close)
    elif c in operator_map:
        # Handle operator
        new_op = operator_map[c]

        # Check for unary operators (+ or -)
        if c in ['-', '+']:
            if symPrevious.type not in [Symbol.Type.Literal_Numeric, Symbol.Type.Parenthesis_Close]:
                # Unary operator case (e.g., leading minus or after opening parenthesis or another operator)
                new_op = Operator(100, 1)  # Higher precedence for unary minus/plus

        # Pop operators from holding stack if they have higher precedence
        while len(stkHolding) != 0 and stkHolding[0].type != Symbol.Type.Parenthesis_Open:
            if stkHolding[0].type == Symbol.Type.Operator:
                holding_stack_op = stkHolding[0].op
                if holding_stack_op.precedence >= new_op.precedence:
                    stkOutput.append(stkHolding.popleft())
                else:
                    break
            else:
                break

        # Push the new operator to the holding stack
        stkHolding.appendleft(Symbol(symbol=str(c), symbol_type=Symbol.Type.Operator, op=new_op))
        symPrevious = stkHolding[0]
    else:
        print(f"Bad Symbol: '{c}'")
        exit(0)

    pass_num += 1

# Drain the holding stack into output
while len(stkHolding) != 0:
    stkOutput.append(stkHolding.popleft())

# Print the RPN expression
print(f"Expression:= {expression}")
print("RPN       := ", end="")
for s in stkOutput:
    print(s.symbol, end="")
print()

# Solver
stkSolve = deque()

for inst in stkOutput:
    if inst.type == Symbol.Type.Literal_Numeric:
        stkSolve.append(float(inst.symbol))
    elif inst.type == Symbol.Type.Operator:
        # Make sure there are enough operands on the stack before popping
        if len(stkSolve) < inst.op.arguments:
            print("Error: Insufficient operands for operation")
            exit(0)

        # Pop operands for the operation
        mem = [stkSolve.pop() for _ in range(inst.op.arguments)]

        result = 0.0
        if inst.op.arguments == 2:
            if inst.symbol == '/':
                result = mem[1] / mem[0]
            elif inst.symbol == '*':
                result = mem[1] * mem[0]
            elif inst.symbol == '+':
                result = mem[1] + mem[0]
            elif inst.symbol == '-':
                result = mem[1] - mem[0]

        if inst.op.arguments == 1:
            if inst.symbol == '+':
                result = +mem[0]
            elif inst.symbol == '-':
                result = -mem[0]

        stkSolve.append(result)

# Output the result
print(f"Result    := {stkSolve[0]}")
