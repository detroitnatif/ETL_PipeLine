import os

def print_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')

# Call the function with the project path
print_directory_structure('/Users/tylerklimas/Desktop/etl')