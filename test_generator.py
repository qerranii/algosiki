import os
import random
from solution import solve


def generate_graph(num_nodes):
    graph = {i: {} for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            if random.random() < 0.3:
                weight = random.randint(1, 100)
                graph[i][j] = weight
                graph[j][i] = weight
    return graph


def generate_tests(num_tests):
    os.makedirs('tests', exist_ok=True)
    os.makedirs('answers', exist_ok=True)

    for test_id in range(num_tests):
        num_nodes = random.randint(5, 20)
        graph = generate_graph(num_nodes)
        start = random.randint(0, num_nodes - 1)

        with open(f'tests/test_{test_id}.txt', 'w') as f:
            f.write(f"{num_nodes} {start}\n")
            for node in graph:
                for neighbor, weight in graph[node].items():
                    if neighbor > node:
                        f.write(f"{node} {neighbor} {weight}\n")

        answer = solve(graph, start)
        with open(f'answers/answer_{test_id}.txt', 'w') as f:
            f.write(str(answer))


if __name__ == "__main__":
    generate_tests(100)