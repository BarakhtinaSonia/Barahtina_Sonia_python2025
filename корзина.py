import os
import time
import argparse
from datetime import datetime

def clean_trash(trash_folder_path, age_thr):
    log_path = os.path.join(trash_folder_path, 'clean_trash.log')
    
    while True:
        deleted_items = []
        for root, dirs, files in os.walk(trash_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_age = time.time() - os.path.getmtime(file_path)
                    if file_age > age_thr:
                        os.remove(file_path)
                        deleted_items.append(file_path)

        for root, dirs, files in os.walk(trash_folder_path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                try:
                    os.rmdir(dir_path)
                    deleted_items.append(dir_path)
                except OSError:
                    pass  

        if deleted_items:
            with open(log_path, 'a') as f:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                for item in deleted_items:
                    f.write(f"{timestamp} - Deleted: {item}\n")

        time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Clean trash folder')
    parser.add_argument('--trash_folder_path', help='Path to trash folder', required=True)
    parser.add_argument('--age_thr', help='File age threshold in seconds', type=int, required=True)
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.trash_folder_path):
        print(f"Error: {args.trash_folder_path} тако папки не существует")
        exit(1)

    if args.age_thr <= 0:
        print("Error: Вы ввели некорректный возраст для проверки!!!")
        exit(1)
