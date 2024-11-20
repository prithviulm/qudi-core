import sys
from pathlib import Path

def read_requirements(file_path):
    if not Path(file_path).is_file():
        return set()
    with open(file_path, 'r') as file:
        return set(file.readlines())

def compare_pip_freeze(current_file, previous_file, output_file):
    current = read_requirements(current_file)
    previous = read_requirements(previous_file)

    diff = current.symmetric_difference(previous)

    with open(output_file, 'w') as file:
        if not diff:
            file.write("No differences found.\n")
        else:
            file.writelines(diff)
    
    return diff

if __name__ == "__main__":
    current_file = sys.argv[1]
    previous_file = sys.argv[2]
    output_file = sys.argv[3]

    diff = compare_pip_freeze(current_file, previous_file, output_file)

    if diff:
        print(f"Differences found. See {output_file} for details.")
    else:
        print("No differences found.")
