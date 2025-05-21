import os
import subprocess
import sys
from validator import validate_solution
from test_generator import generate_tests

FORBIDDEN_MODULES = ['heapq', 'numpy', 'scipy', 'networkx', 'keras', 'pillow', 'tensorflow']
TIME_LIMIT = 2
MEMORY_LIMIT = 100


def check_forbidden_imports(code_path):
    with open(code_path, 'r') as f:
        code = f.read()
    return not any(f'import {m}' in code or f'from {m}' in code for m in FORBIDDEN_MODULES)


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <solution_path>")
        return

    user_code = sys.argv[1]

    if not os.path.exists('tests'):
        generate_tests(100)

    if not check_forbidden_imports(user_code):
        print("Forbidden modules used!")
        return

    print("Running tests...")
    test_results = validate_solution(user_code, TIME_LIMIT, MEMORY_LIMIT)

    passed = 0
    for result in test_results:
        if result['status'] == 'success':
            passed += 1
        else:
            print(f"Test {result['test_id']} failed: {result['message']}")

    print(f"\nPassed {passed}/{len(test_results)} tests")
    print("Memory check active:", "Yes" if test_results[0]['memory_checked'] else "No")


if __name__ == "__main__":
    main()