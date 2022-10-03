import pickle
from spylls.hunspell import Dictionary

def serialize_dict():
    dictionary = Dictionary.from_files('assets/uk_UA')
    with open('assets/dictionary', 'wb') as file:
        pickle.dump(dictionary, file)


if __name__ == "__main__":
    serialize_dict()
