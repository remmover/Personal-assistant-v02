from collections import UserDict
import pickle


class Text:

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"{self.text}"


class Keyword:

    def __init__(self, keyword):
        self.keyword = keyword

    def __eq__(self, other):
        if isinstance(other, Keyword):
            return self.keyword == other.keyword
        return False

    def __repr__(self):
        return f"{self.keyword}"
    


class RecordNote:

    def __init__(self, text: Text, keyword: Keyword = None):
        self.texts = [text] if text else []
        self.keywords = [keyword] if keyword else []

    def add_note(self, text: Text):
        self.texts.append(text)

    def add_keywords(self, keyword: Keyword):
        self.keywords.append(keyword)

    def edit_note(self, new_text: Text):
        if len(self.texts) > 0:
            self.texts[0] = new_text

    def edit_keyword(self, old_keyword: Keyword, new_keyword: Keyword):
        if old_keyword in self.keywords:
            index = self.keywords.index(old_keyword)
            self.keywords[index] = new_keyword

    def __repr__(self):
        join_text = ", ".join(str(text) for text in self.texts)
        join_keyword = ", ".join(str(keyword) for keyword in self.keywords)
        return "\n" f"- {join_text}\n{f'- Теги: {join_keyword}' if join_keyword else ''}" "\n"


class Notebook(UserDict):
   
    def add_record(self, record: RecordNote):
        if self.data:
            name_note = f"Запис {int(max(self.data.keys())[6:]) + 1}"
        else:
            name_note = "Запис 1"
        self.data[name_note] = record
        return f"Нотатку додано:\n\n{name_note}: {self.data[name_note]}"

    def search(self, param):
        if len(param) < 3:
            return "Для здійснення пошуку треба ввести принаймні 3 символи."
        result = ""
        for key, value in self.items():
            if param.lower() in str(key).lower() or param.lower() in str(
                    value).lower():
                result += f"{key} {value}\n"
        if not result:
            return "Упс, нічого подібного не знайдено :("
        return result

    def delete_note(self, param):
        keys_to_delete = [
            key for key in self.keys() if param.lower() in key.lower()
        ]
        if not keys_to_delete:
            return "Запису для видалення не знайдено. Якщо необхідно, спробуйте ще раз."
        for key in keys_to_delete:
            del self[key]
        return f"Видалено {len(keys_to_delete)} записів."

    def sorting_by_keyword(self):
        sorted_data = dict(
            sorted(self.data.items(),
                   key=lambda x: str(x[1].keywords).lower()))
        self.data = sorted_data
        sorted_show = [f"{key}: {value}" for key, value in self.data.items()]
        return '\n'.join(sorted_show)

    def show_all_notes(self):
        notes = [f"{key}: {value}" for key, value in self.data.items()]
        return '\n'.join(notes)

    def __repr__(self):
        output = ""
        for key, value in self.data.items():
            output += f"{key} {value}\n"
        return output

    def save_to_notebin(self, path="notebook.bin"):
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_notebin(path="notebook.bin"):
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return NOTE_BOOK
        except EOFError:
            return NOTE_BOOK


NOTE_BOOK = Notebook()

# if __name__ == '__main__':
#     key1 = Keyword('купити')
#     text1 = Text('хліб, молоко, печиво')
#     key2 = Keyword('прибирання')
#     text2 = Text('помити підлогу, витерти пил')
#     record1 = RecordNote(text=text1, keyword=key1)
#     record2 = RecordNote(text=text2, keyword=key2)
#     Note_book.add_record(record1)
#     Note_book.add_record(record2)
#     print(Note_book.show_all_notes())