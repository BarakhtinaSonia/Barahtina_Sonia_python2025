import os
import argparse
import re 

def read_gitignore(gitignore_path):
    with open(gitignore_path, 'r') as f:
        lines = f.readlines()
    view = []
    for line in lines:
        view.append(line)
    return view


def ignored_yes_or_no(file_path, gitignore_view, project_dir):
    file_path = os.path.normpath(file_path)
    project_dir = os.path.normpath(project_dir)
    relative_path = os.path.relpath(file_path, project_dir).replace('\\', '/')
    
    for view in gitignore_view:
        view = view.replace('\\', '/')
        if view == relative_path:
            return view
        if view.startswith('*'):
            regex_view = view.replace('.', r'\.').replace('*', '.*') + '$'
            if re.match(regex_view, relative_path):
                return view
            if re.match(regex_view, os.path.basename(file_path)):
                return view
    
    return None

def find_files_ignored(project_dir, gitignore_view):
    ignored_files = []
    for root, dirs, files in os.walk(project_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        
        dir_path = os.path.relpath(root, project_dir).replace('\\', '/')
        for view in gitignore_view:
            if view.endswith('/'):
                dir_pattern = view.rstrip('/')
                dir_pattern = re.escape(dir_pattern).replace(r'\*', '.*')
                if re.fullmatch(dir_pattern, dir_path):
                    dirs[:] = []
                    break
        
        for file in files:
            file_path = os.path.join(root, file)
            ignore_rule = ignored_yes_or_no(file_path, gitignore_view, project_dir)
            if ignore_rule is not None:
                ignored_files.append((file_path, ignore_rule))
    
    return ignored_files

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project_dir', required=True)
    args = parser.parse_args()
    
    project_dir = os.path.abspath(args.project_dir)
    gitignore_path = os.path.join(project_dir, '.gitignore')
    
    if not os.path.exists(gitignore_path):
        print("No .gitignore file found in the project directory")
        return
    
    gitignore_view = read_gitignore(gitignore_path)
    ignored_files = find_files_ignored(project_dir, gitignore_view)
    
    print("Ignored files:")
    for file_path, rule in ignored_files:
        print(f"{file_path} ignored by expression {rule}")

if __name__ == "__main__":
    main()