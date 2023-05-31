import random


OPERATIONS = ['+', '-', '*', '/']

EXPRESSION_DEPTH = 3

POPULATION_SIZE = 10
MAX_GENERATIONS = 5000


class Expression():
    def __init__(self, op, left_node, right_node):
        self.op = op
        self.left_node = left_node
        self.right_node = right_node
        self.cache = None

    def __str__(self):
        return f'({self.left_node} {self.op} {self.right_node})'

def evaluate(node):
    if isinstance(node, int):
        return node

    op = node.op
    left_node = evaluate(node.left_node)
    right_node = evaluate(node.right_node)

    if op == '+':
        return left_node + right_node
    elif op == '-':
        return left_node - right_node
    elif op == '*':
        return left_node * right_node
    elif op == '/':
        return left_node / right_node
    else:
        return 0

def generate_expression(depth):
    if depth <= 0:
        return random.randint(0, 10)

    op = random.choice(OPERATIONS)
    left_node = generate_expression(depth - 1)
    right_node = generate_expression(depth - 1)

    return Expression(op, left_node, right_node)

def generate_population(size):
    return list(map(lambda _: generate_expression(EXPRESSION_DEPTH), range(size)))

def fitness(expr, target):
    diff = None

    try:
        result = evaluate(expr)
        expr.cache = result

        diff = abs(result - target)
    except ZeroDivisionError:
        diff = 1000 # large error

    return 1 / (diff + 1)

def diversity(population):
    d = 0

    for i in range(len(population)):
        for j in range(i+1, len(population)):
            expr1, expr2 = population[i], population[j]
            if expr1.cache != expr2.cache:
                d += 1
    return d

def select_parents(population, fitnesses):
    fitnesses_sum = sum(fitnesses)
    weights = list(map(lambda f: f / fitnesses_sum, fitnesses))

    parent1 = random.choices(population, weights=weights, k=1)[0]
    parent2 = random.choices(population, weights=weights, k=1)[0]

    return parent1, parent2

def cross(expr1, expr2, crossing_rate):
    if random.uniform(0, 1) > crossing_rate:
        return random.choice([expr1, expr2])

    op = random.choice([expr1.op, expr2.op])
    left_node = random.choice([expr1.left_node, expr2.left_node])
    right_node = random.choice([expr1.right_node, expr2.right_node])

    return Expression(op, left_node, right_node)

def mutate(expr, mutation_rate):
    if random.uniform(0, 1) < mutation_rate:
        return expr

    left_node = None
    right_node = None

    if random.uniform(0, 1) > 0.5:
        left_node = generate_expression(EXPRESSION_DEPTH - 1)
        right_node = expr.right_node
    else:
        left_node = expr.left_node
        right_node = generate_expression(EXPRESSION_DEPTH - 1)

    return Expression(expr.op, left_node, right_node)

def run(target):
    crossing_rate = 0.8
    mutation_rate = 0.2

    population = generate_population(POPULATION_SIZE)

    for _ in range(MAX_GENERATIONS):
        fitnesses = list(map(lambda f : fitness(f, target), population))
        
        if diversity(population) > POPULATION_SIZE * 0.8:
            crossing_rate *= 1.1
            mutation_rate *= 0.9
        else:
            crossing_rate *= 0.9
            mutation_rate *= 1.1

        parent1, parent2 = select_parents(population, fitnesses)
        crossing_child = cross(parent1, parent2, crossing_rate)
        mutation_child = mutate(random.choice([parent1, parent2]), mutation_rate)

        population = sorted(population, key=lambda expr: fitness(expr, target))
        population[0] = crossing_child
        population[1] = mutation_child

    return population[POPULATION_SIZE - 1]


if __name__ == "__main__":
    expr = run(target=100)
    print('expression:', expr)
    print('evaluation:', evaluate(expr))
