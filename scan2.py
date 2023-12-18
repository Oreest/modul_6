import sys
from pathlib import Path

image_files = list()
docs_files = list()
audio_files = list()
video_files = list()
#docx_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {
    'JPEG': image_files,
    'PNG': image_files,
    'JPG': image_files,

    'TXT': docs_files,
    'PDF': docs_files,
    'XLSX': docs_files,
    'PPTX': docs_files,
    'DOCX': docs_files,
    'DOC': docs_files,

    'MP3': audio_files,
    'OGG': audio_files,
    'WAV': audio_files,
    'AMR': audio_files,

    'AVI': video_files,
    'MP4': video_files,
    'MOV': video_files,
    'MKV': video_files,

    'ZIP': archives,
    'GZ': archives,
    'TAR': archives
}

def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('Images', 'Audio', 'Video', 'Documents', 'Archives', 'OTHER'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)

if __name__ == '__main__':
    path = sys.argv[1]
    print(f"Start in {path}")

    folder = Path(path)

    scan(folder)

    print(f"Images: {image_files}")
    print(f"Audio files: {audio_files}")
    print(f"Video files: {video_files}")
    #print(f"txt: {txt_files}")
    print(f"documents: {docs_files}")
    print(f"archives: {archives}")
    print(f"unkown: {others}")
    print(f"All extensions: {extensions}")
    print(f"Unknown extensions: {unknown}")
    print(f"Folder: {folders}")
