import numpy as np
import spacy
from joblib import load
from numpy.linalg import norm
import re
# python -m spacy download ru_core_news_lg!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class Travel_designer:
    def __init__(self):
        self.russian_nlp = spacy.load("ru_core_news_lg")


    def _make_vector(self, data: list, lang="ru"):
        words_vector = np.zeros(300)

        for word in data:
            words_vector += self.russian_nlp(word).vector

        if norm_vector := norm(words_vector):
            words_vector /= norm_vector

        return words_vector


    def _remove_stop_and_make_lemma(self, 
        data: str = "", lang: str = "ru",
    ):
        data = re.sub(r'[^a-zA-Zа-яА-Я!?,.]', " ", data)
        my_data = self.russian_nlp(str(data))
        tokens = [token.lemma_ for token in my_data if (token.has_vector and  not token.is_stop)]
        return tokens


    def _prepare(self, data: str, lang: str = "ru"):
        return self._make_vector(self._remove_stop_and_make_lemma(data, lang), lang="ru")

    
# extr = Travel_designer()




import torch
import torch.nn as nn

class TraveLSuperTinyModel(nn.Module):
    def __init__(self, output_size):
        super(TraveLSuperTinyModel, self).__init__()
        self.input_size = 300
        self.hidden_size = 32
        self.output_size = output_size
        self.num_layers = 2
        self.all_citys = np.array([])
        self.all_tours = np.array([])

        self.preloader = Travel_designer()
        self.lstm = nn.LSTM(input_size=self.input_size, hidden_size=self.hidden_size, 
                            num_layers=self.num_layers, batch_first=True)
        self.fc = nn.Linear(self.hidden_size, output_size)

    def _make_len(self, n):
        self.output_size = n
    
    def _choice_tours(self, city_tours: list[str]):
        self.all_tours = np.array(city_tours)
    
    def _cold_start(self, all_citys:list[str], all_tours:list[str]) -> None:
        self.all_citys = np.array(all_citys)
        self.all_tours = np.array(all_tours)

    def forward(self, city_id:str, task:str, reserved_tours:list[str]  =  [""], hidden=None) -> np.ndarray:
        reserved_tours = np.array(reserved_tours)
        x = torch.from_numpy(self.preloader._prepare(city_id))
        x = torch.tensor(np.random.rand(1, self.output_size, 300), dtype=torch.float32)
        out, hidden = self.lstm(x, hidden)
        out = self.fc(out[:, -1, :])
        out = np.random.choice(a=self.all_citys[self.all_citys!=city_id], size = self.output_size)
        if task == "tours":
            out = np.random.choice(a=self.all_tours[~np.in1d(self.all_tours, reserved_tours)], size = self.output_size)
        return out
    
# n = 10 # количество выходных нейронов

# model = TraveLSuperTinyModel(n)
# model._cold_start(all_citys=["1","2","3","4","5","6","7","8","9","10","11","12","13"], all_tours=["1","2","3","4","5","6","1","2","3","4","5","6","7","8","9","10","11","12","13", "14"])
# print(model(city_id="1", task="tours", reserved_tours = ["9","10","11","12","13"]))
# # сохранение модели в pkl файл
# torch.save(model.state_dict(), "./models/model.pkl")