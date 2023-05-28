import torch
from Travel_designer import Travel_designer, TraveLSuperTinyModel

# ОБЯЗАТЕЛЬНО В НАЧАЛЕ СКАЧАТЬ ВЕСА SPACY ДЛЯ РУССКОГО ЯЗЫКА.
# ОБЯЗАТЕЛЬНО!!!!!!!!!!
# В терминале прописываешь python -m spacy download ru_core_news_lg
# делается 1 раз

# Заргужаем модель Я НЕ УМЕЮ В НОРМАЛЬНЫЕ ПУТИ, НАПИШИТЕ ТАК, ЧТОБ РАБОТАЛО АДЕКВАТНО, ПОЖАЛУЙСТА
model = TraveLSuperTinyModel(10)
model.load_state_dict(torch.load("./models/model.pkl"))

# Вот эта ручка дёргается 1 раз, и нужно загрузить ВСЕ города и Все туры начального города (можно любой или пихнуть [""]).
model._cold_start(
    all_citys=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13"],
     #(можно любые туры в начале пихнуть, либо пихнуть [""])
    all_tours=[
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
    ],
)
 

# получение idшек поездок в городе
# Получаете np.ndarray всех городов в которые можно поехать. Выбранный город не попадается.
print(model(city_id="1", task="citys"))

# Понимаете, что за раз хотите выводить меньше/больше. Дёргается в любой момент. По умолчанию 10
model._make_len(2)

# Пихаете туры того города в котором нужно выьрать (или все туры, из которых хотите, чтобы модель выбирала)
# Если не меняется локация или желаемыре туры, не нужно обновлять 
model._choice_tours(["2", "10", "111"]) 

    #город пользователя                 # Туры выьранные пользователем, которые не должны учавствовать в выборе. 
                                        # Пересечение времени туров НЕ проверяется
print(model(city_id="1", task="tours", reserved_tours=["9", "10", "11", "2", "13"]))

#Смари внимательно. Когда нужно вытащить id городов - пихаешь task="city", если id туров - tack="tours"