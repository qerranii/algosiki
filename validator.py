import os
import subprocess
import time

try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


def validate_solution(solution_path, time_limit, memory_limit):
    test_files = sorted(os.listdir('tests'))
    results = []

    for test_file in test_files:
        test_id = test_file.split('_')[1].split('.')[0]
        result = {
            'test_id': test_id,
            'status': 'unknown',
            'message': '',
            'memory_checked': False
        }

        try:
            with open(f'tests/{test_file}', 'r') as f:
                test_data = f.read()

            process = subprocess.Popen(
                ['python', solution_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            start_time = time.time()
            memory_peak = 0

            if PSUTIL_AVAILABLE:
                ps_proc = psutil.Process(process.pid)

            try:
                stdout, stderr = process.communicate(
                    input=test_data,
                    timeout=time_limit
                )

                if PSUTIL_AVAILABLE:
                    try:
                        memory_peak = ps_proc.memory_info().rss / 1024 / 1024
                        for child in ps_proc.children(recursive=True):
                            mem = child.memory_info().rss / 1024 / 1024
                            if mem > memory_peak:
                                memory_peak = mem
                    except psutil.NoSuchProcess:
                        pass

                    if memory_peak > memory_limit:
                        result.update({
                            'status': 'failed',
                            'message': f"ML ({memory_peak:.1f}MB > {memory_limit}MB)"
                        })
                        results.append(result)
                        continue

                exit_code = process.poll()
                if exit_code != 0:
                    result.update({
                        'status': 'failed',
                        'message': f"Runtime error (code {exit_code}): {stderr.strip() or 'No output'}"
                    })
                else:
                    with open(f'answers/answer_{test_id}.txt', 'r') as f:
                        expected = int(f.read().strip())
                    user_answer = int(stdout.strip())
                    result['status'] = 'success' if user_answer == expected else 'failed'
                    result['message'] = f"Expected {expected}, got {user_answer}" if result[
                                                                                         'status'] == 'failed' else ''

            except subprocess.TimeoutExpired:
                process.kill()
                result.update({
                    'status': 'failed',
                    'message': f"TL ({time_limit}s)"
                })

            result['memory_checked'] = PSUTIL_AVAILABLE

        except Exception as e:
            result.update({
                'status': 'error',
                'message': f"System error: {str(e)}"
            })

        results.append(result)

    return results