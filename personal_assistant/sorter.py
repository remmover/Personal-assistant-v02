from pathlib import Path
from string import punctuation
import shutil


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = (
    'a', 'b', 'v', 'g', 'd', 'e', 'e', 'j', 'z', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'f',
    'h', 'ts', 'ch', 'sh', 'sch', '', 'y', '', 'e', 'yu',
    'ya', 'je', 'i', 'ji', 'g'
)
PROBLEM_SYMBOLS = punctuation.replace('.', ' ')
TRANS = {}

CATEGORIES = {
    'Images': ['.jpeg', '.png', '.jpg', '.svg'],
    'Videos': ['.avi', '.mp4', '.mov', '.mkv'],
    'Docs': ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    'Audio': ['.mp3', '.ogg', '.wav', '.amr'],
    'Archives': ['.zip', '.gz', '.tar'],
    'Other': None
}


for cyrillic, translation in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(cyrillic)] = translation
    TRANS[ord(cyrillic.upper())] = translation.upper()

for symbol in PROBLEM_SYMBOLS:
    TRANS[ord(symbol)] = "_"


def normalize(name: str) -> str:
    return name.translate(TRANS)


def create_folders(directory):
    for folder_name in CATEGORIES.keys():
        try:
            new_folder = directory / folder_name
            new_folder.mkdir()
        except FileExistsError:
            print(f'Folder named {folder_name} already exists.')


def find_replace(directory: Path, file: Path):
    for category, extensions in CATEGORIES.items():
        new_path = directory / category
        if not extensions:
            file.replace(new_path / normalize(file.name))
            return None
        if file.suffix.lower() in extensions:
            file.replace(new_path / normalize(file.name))
            return None

    return None


def replace_files(directory: Path):
    for file in directory.glob('**/*.*'):
        find_replace(directory, file)


def unpack_archive(directory: Path):
    archive_directory = directory / 'ARCHIVES'
    for archive in archive_directory.glob('*.*'):
        path_archive_folder = archive_directory / archive.stem.upper()
        shutil.unpack_archive(archive, path_archive_folder)


def delete_empty_folders(directory: Path):
    empty_folders = []
    for folder in directory.glob('**/*'):
        if folder.is_dir() and not any(folder.iterdir()):
            empty_folders.append(folder)

    for folder in empty_folders:
        shutil.rmtree(str(folder))
        print(f'{folder.name} folder deleted.')


def main():
    path_folder = input('\nВітаю! Я допоможу тобі розсортувати файли по теках. Мені потрібен шлях до папки, що я мушу відсортувати (накшталт C:/Users/Admin/Unsorted):\n')
    if path_folder == '' or path_folder == 'exit':
        return '\nВпевнений, що наступного разу тобі знадобиться моя допомога.'
    else:
        user_input = input(
            f'Ти впевнений, що хочеш відсортувати файлі у теці "{path_folder}" ?(так/ні): \n').lower()

        match user_input:
            case 'ні':
                return 'Виконання програми зупинено користувачем.'

            case 'так':
                try:
                    directory = Path(path_folder)
                except IndexError:
                    print('Must be path to folder.')
                if not directory.exists():
                    print("Такої теки не існує.")
                else:
                    unpuck_input = input("Чи потрібно разпакувати архіви?(так/ні): \n").lower()
                    if unpuck_input == 'так':
                        create_folders(directory)
                        replace_files(directory)
                        unpack_archive(directory)
                        delete_empty_folders(directory)

                    else:
                        create_folders(directory)
                        replace_files(directory)
                        delete_empty_folders(directory)
        return 'Роботу програми завершено'
                    
