from server.services.nearest_store.store_info import get_closest_store, get_weather_forecast, get_coordinates
from pathlib import Path
from glob import glob
import random
import json


def get_subdirectory_files(file_ext: str = ".json"):
    """Find full paths for all .json files underneath of current folder"""
    directory = f"{Path(__file__).parent}/dialogue"
    dirs_list = [p for p in glob(directory + "**/*", recursive=True)]
    file_list = [[f for f in glob(p + f"**/*{file_ext}", recursive=True)] for p in dirs_list]
    flat_list = [item for sublist in file_list for item in sublist]
    return flat_list


def text_cleaning(sentence: str, tokenize: bool = True):
    """Cleaning dirty text for better chatbot performance"""
    # 1. Tokenize all words
    # 2. Lowercase all words in sentence
    # 3. Removing all characters but alphabetical and numeric characters
    # 4. Combine list of strings to string if tokenize is false
    sentence = [w for w in sentence.split()]
    sentence = [w for w in sentence if len(w) > 1]
    sentence = [w.lower() for w in sentence]
    sentence = ["".join([i for i in w if i.isalpha() or i.isalnum()]) for w in sentence]
    sentence = " ".join(sentence) if tokenize is False else sentence
    return sentence


class Dialogue:
    def __init__(self):
        self.intents = []
        self.pattern = {}
        self.respond = {}
        self._open_json_files()

    def _open_json_files(self):
        """Opens all the json files in subdirectories"""
        for file_path in get_subdirectory_files():
            with open(file_path, encoding='utf-8') as json_file:
                file = json.load(json_file)
                self._unpack_json_files(file)

    def _unpack_json_files(self, file):
        """Recursive function to unpack lists of dicts, followed by
        adding the key:value content to different class variables"""
        if isinstance(file, list):
            for dict_elem in file:
                self._unpack_json_files(dict_elem)
        elif isinstance(file, dict):
            self.intents.append(file['tag'])
            self.pattern[file['tag']] = [text_cleaning(elem, tokenize=False) for elem in file['patterns']]
            self.respond[file['tag']] = file['responses']

    def get_dialog_response(self, user_msg: str) -> dict:
        user_sentence = text_cleaning(user_msg)
        bool_classify = {intent: [] for intent in self.intents}
        prob_classify = {intent: 0 for intent in self.intents}

        # First go through each word of each pattern in each intent
        # and classify it with the user message using boolean classification
        for intent in self.intents:
            for pattern in self.pattern[intent]:
                for word in user_sentence:
                    print(pattern, word)
                    if word in pattern:
                        bool_classify[intent].append(1)
                    else:
                        bool_classify[intent].append(0)

        # Secondly we calculate the probability of choosing the correct
        # intent by dividing the sum of matches with the amount of patterns
        for intent in self.intents:
            total = sum(bool_classify[intent])
            length = len(bool_classify[intent])
            if total != 0 and length != 0:
                print(intent, total, length, bool_classify[intent])
                prob_classify[intent] = round(total/length, 2)

        # And finally, return the response message
        highest_prob = sorted(prob_classify, key=prob_classify.get, reverse=True)
        if highest_prob[0] == "Weather":
            msg = get_weather_forecast(city="Aarhus", api_response=True)['msg']
        elif highest_prob[0] == "Distance":
            lat, lon = get_coordinates(city="Aarhus")
            msg = get_closest_store(lat_customer=lat, lon_customer=lon, api_response=True)['msg']
        else:
            msg = random.choice(self.respond[highest_prob[0]])
        print(msg)
        return {"msg": msg,
                "data": {idx: prob_classify[idx] for idx in highest_prob}}




