
def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()

    while len(visited) < len(graph):
        current = min(
            (node for node in graph if node not in visited),
            key=lambda x: distances[x]
        )
        visited.add(current)

        for neighbor, weight in graph[current].items():
            new_dist = distances[current] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
    return distances


def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] >= target:
            result = mid
            right = mid - 1
        else:
            left = mid + 1
    return result if result != -1 else -1


def solve(graph, start):
    distances = dijkstra(graph, start)
    valid_distances = [d for d in distances.values() if d != float('inf')]

    if not valid_distances:
        return -1

    sorted_dist = sorted(valid_distances)
    avg = sum(sorted_dist) // len(sorted_dist)

    return binary_search(sorted_dist, avg)


if __name__ == "__main__":
    import sys
    from ast import literal_eval


    def parse_input():
        lines = [line.strip() for line in sys.stdin if line.strip()]
        n, start = map(int, lines[0].split())
        graph = {i: {} for i in range(n)}

        for line in lines[1:]:
            u, v, w = map(int, line.split())
            graph[u][v] = w
            graph[v][u] = w

        return graph, start


    graph, start = parse_input()
    print(solve(graph, start))