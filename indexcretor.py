import os
import re

class BookIndexer:
    def __init__(self):
        self.index = {}
        self.exclude_words = set()

    def index_pages(self):
        self.load_exclude_words()

        file_list = self.get_file_list()
        for file in file_list:
            self.index_file(file)

    def load_exclude_words(self):
        with open("exclude-words.txt", "r") as exclude_file:
            for word in exclude_file:
                self.exclude_words.add(word.strip().lower())

    def get_file_list(self):
        file_list = []
        for filename in os.listdir("."):
            if filename.startswith("Page") and filename.endswith(".txt"):
                file_list.append(filename)
        return file_list

    def index_file(self, filename):
        page_num = int(re.search(r"\d+", filename).group())
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                words = re.findall(r"\b[a-zA-Z]+(?:'[a-zA-Z]+)?\b", line)
                for word in words:
                    self.index_word(word.lower(), page_num)

    def index_word(self, word, page_num):
        if word in self.exclude_words:
            return
        if word not in self.index:
            self.index[word] = set()
        self.index[word].add(page_num)

    def save_index(self, filename):
        with open(filename, "w") as file:
            for word in sorted(self.index):
                pages = sorted(self.index[word])
                file.write(f"{word} : {', '.join(map(str, pages))}\n")


def main():
    book_indexer = BookIndexer()
    book_indexer.index_pages()
    book_indexer.save_index("index.txt")

if __name__ == "__main__":
    main()
