import hashlib

KNOWN_SOLUTIONS = []


def get_code_hash(file_path):
    with open(file_path, 'r') as f:
        code = f.read()
    return hashlib.sha256(code.encode()).hexdigest()


def check_plagiarism(user_code_path):
    user_hash = get_code_hash(user_code_path)

    if user_hash in KNOWN_SOLUTIONS:
        return False
    return True