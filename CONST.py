''' Импортирование библиотек и необходимых констант '''
import os
import sys
import random
import pygame
import time
import math
import copy
from PIL import Image
import webbrowser

RAIL_MATRIX = [
    [
        [0, -1, 0, -1]
    ],

    [
        [1, 3, -1, -1]
    ],

    [
        [1, 3, -1, -1], [-1, 1, 3, -1], [0, -1, 0, -1]
    ],

    [
        [0, -1, 0, -1], [-1, 0, -1, 0]
    ]
]

TYPES_OF_RESOURCES = ['passenger', 'iron', 'coal', 'wood', 'crops']

CAPACITY = [(10, 42), (10,), (10,), (10,), (10,), (10,)]
TRAIN_STATS = {'coal_capacity' : 99, 'blocks_per_second' : 2, 'coal_per_second' : 0.6, 'names' : ["Томас", "Джеймс", "Гордон", "Эдвард", "Эмили", "Перси", "Генри", "Тоби"]}

LOADING_DURATION_MS = [500, 500, 500, 500, 500, 500]
BUILDINGS_COOLDOWN_MS = {'coal_mine' : 500, 'iron_mine' : 500, 'sawmill' : 500, 'seaport' : 500, 'station' : 500, 'storage' : 500}

ITEMS_FOR_COLLECTING_RESOURCES = {'iron' : 1, 'coal' : 1, 'wood' : 1, 'crops' : 1}
EXP_FOR_COLLECTING_RESOURCES = {'iron' : 1, 'coal' : 1, 'wood' : 1, 'crops' : 1, 'passenger' : 1}
EXP_FOR_BUYING_ITEMS = {'coal_mine' : 30, 'iron_mine' : 50, 'sawmill' : 20, 'seaport' : 100, 'station' : 10, 'storage' : 40,
                        'rail_0' : 2, 'rail_1' : 2, 'rail_2' : 2, 'rail_3' : 2,
                        'car_0' : 5, 'car_1' : 5, 'car_2' : 5, 'car_3' : 5, 'car_4' : 5, 'car_5' : 5,
                        'coal' : 0, 'iron' : 0, 'wood' : 0, 'crops' : 0}

BUILDINGS_LIST = ['coal_mine', 'iron_mine', 'sawmill', 'seaport', 'station', 'storage']
RAILS_LIST = ['rail_0', 'rail_1', 'rail_2', 'rail_3']
CARRIAGES_LIST = ['car_0', 'car_1', 'car_2', 'car_3', 'car_4', 'car_5']
RESOURCES_LIST = ['coal', 'iron', 'wood', 'crops']

PASSENGER_TICKET_COST = (5, 15)
PASSENGER_REQUIRED_FOOD = 1

SHOP_PRODUCTS = [['rail_0', 'rail_1', 'rail_2', 'rail_3'],
                        ['coal_mine', 'iron_mine', 'sawmill', 'seaport', 'station', 'storage'],
                        ['car_0', 'car_1', 'car_2', 'car_3', 'car_4', 'car_5'],
                        ['coal', 'iron', 'wood', 'crops']]
SHOP_DESCRIPTION = {'rail_0' : "Прямой рельс перемещает поезда в том же направлении.",
                           'rail_1' : "Поворотный рельс позволяет повернуть поезд на 90 градусов.",
                           'rail_2' : "Т-образная развилка работает как прямой или как поворотный рельс.",
                           'rail_3' : "Перекрёсток пропускает поезда в одном из двух направлений.",
                           'coal_mine' : "Угольная шахта приносит уголь.",
                           'iron_mine' : "Железная шахта приносит железо.",
                           'sawmill' : "Лесопилка приносит доски.",
                           'seaport' : "Морской порт приносит еду.",
                           'station' : "На станции происходит посадка и выход пассажиров.",
                           'storage' : "На складе разгружаются вагоны с ресурсами.",
                           'car_0' : "Пассажирский вагон перевозит пассажиров.",
                           'car_1' : "Вагон-самосвал перевозит железо.",
                           'car_2' : "Полувагон перевозит уголь.",
                           'car_3' : "Вагон-платформа перевозит доски.",
                           'car_4' : "Вагон-хоппер перевозит еду.",
                           'car_5' : "Локомотив тянет за собой остальные вагоны.",
                           'coal' : "Уголь нужен для движения поездов.",
                           'iron' : "Железо используется при строительстве.",
                           'wood' : "Доски используются при строительстве.",
                           'crops' : "Еда нужна для перевозки пассажиров."}
RESOURCES_FOR_SELLING = {'coal_mine' : {'money' : 10}, 'iron_mine' : {'money' : 10}, 'sawmill' : {'money' : 5}, 'seaport' : {'money' : 25}, 'station' : {'money' : 20}, 'storage' : {'money' : 25},
                         'rail_0' : {'money' : 2}, 'rail_1' : {'money' : 3}, 'rail_2' : {'money' : 5}, 'rail_3' : {'money' : 6},
                         'car_0' : {'money' : 15}, 'car_1' : {'money' : 7}, 'car_2' : {'money' : 5}, 'car_3' : {'money' : 5}, 'car_4' : {'money' : 10}, 'car_5' : {'money' : 25},
                         'coal' : {'money' : 1}, 'iron' : {'money' : 1}, 'wood' : {'money' : 1}, 'crops' : {'money' : 2}}
RESOURCES_FOR_BUILDING = {'coal_mine': {'money': 20, 'wood': 10},
                                       'iron_mine': {'money': 20, 'wood': 5},
                                       'sawmill': {'money': 10},
                                       'seaport': {'money': 50, 'iron': 15, 'wood': 20},
                                       'station': {'money': 40, 'iron': 5, 'wood': 10},
                                       'storage' : {'money' : 50, 'wood' : 15},
                                       'rail_0': {'money': 5, 'iron': 2, 'wood': 2},
                                       'rail_1': {'money': 7, 'iron': 2, 'wood': 3},
                                       'rail_2': {'money': 10, 'iron': 5, 'wood': 5},
                                       'rail_3': {'money': 12, 'iron': 7, 'wood': 8},
                                       'car_0': {'money': 30, 'iron': 10, 'wood': 20},
                                       'car_1': {'money': 15, 'iron': 30, 'wood': 5},
                                       'car_2': {'money': 10, 'iron': 20, 'wood': 5},
                                       'car_3': {'money': 10, 'iron': 10, 'wood': 10},
                                       'car_4': {'money': 20, 'iron': 20, 'wood': 20},
                                       'car_5': {'money': 50, 'iron': 30, 'wood': 20},
                                       'coal' : {'money' : 3},
                                       'iron' : {'money' : 2},
                                       'wood' : {'money' : 2},
                                       'crops' : {'money' : 5}}
LVL_FOR_BUILDING = {'coal_mine': 3, 'iron_mine': 4, 'sawmill': 2, 'seaport': 7, 'station': 1, 'storage' : 2,
                    'rail_0': 1, 'rail_1': 1, 'rail_2': 2, 'rail_3': 2,
                    'car_0': 1, 'car_1': 4, 'car_2': 3, 'car_3': 2, 'car_4': 7, 'car_5': 1,
                    'coal' : 1, 'iron' : 1, 'wood' : 1, 'crops' : 1}


REQUIRED_EXP = [0, 100, 150, 200, 250, 300, 350, 400, 450, 500]

INITIAL_BUILDINGS = {'coal_mine' : 0, 'iron_mine' : 0, 'sawmill' : 0, 'seaport' : 0, 'station' : 2, 'storage' : 0}
INITIAL_RAILS = {'rail_0' : 10, 'rail_1' : 4, 'rail_2' : 0, 'rail_3' : 0}
INITIAL_CARRIAGES = {'car_0' : 1, 'car_1' : 0, 'car_2' : 0, 'car_3' : 0, 'car_4' : 0, 'car_5' : 1}
INITIAL_RESOURCES = {'money': 100, 'iron': 0, 'coal': 0, 'wood': 0, 'crops': 0}

BUILDINGS_ON_BIOMES = {'mountains': ['coal_mine', 'iron_mine'], 'forest': ['sawmill'], 'sea': ['seaport'], 'plain': ['station', 'storage', 'rail']}

CITY_NAMES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Нижний Новгород", "Челябинск", "Самара", "Уфа", "Ростов-на-Дону", "Омск", "Волгоград"]