import sys
import scan2
import shutil
import normalize
from pathlib import Path

def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    extension = scan2.get_extensions(path).lower()
    #print(path.name)
    new_name = normalize.normalize(path.name.replace(f".{extension}", '')) #.suffix[1:]
    #print(new_name)

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main(folder_path):
    print(folder_path)
    scan2.scan(folder_path)

    for file in scan2.image_files:
        handle_file(file, folder_path, "Images")

    for file in scan2.docs_files:
        handle_file(file, folder_path, "Documents")

    for file in scan2.video_files:
        handle_file(file, folder_path, "Video")

    for file in scan2.audio_files:
        handle_file(file, folder_path, "Audio")

    for file in scan2.others:
        handle_file(file, folder_path, "OTHER")

    for file in scan2.archives:
        handle_archive(file, folder_path, "Archives")

    remove_empty_folders(folder_path)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f'Start in {path}')

    folder = Path(path)
    main(folder.resolve())