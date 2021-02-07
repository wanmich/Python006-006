#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from loguru import logger

"""
if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')
具体要求：
定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。
"""


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, type, size, character):
        self.type = type
        self.size = size
        self.character = character

    @property
    def is_beast(self):
        return True if self.type == '食肉' and (self.size == '中' or self.size == '大') and self.character == '性格凶猛' else False

    def __str__(self):
        return self.__class__.__name__ + ': ' + self.name


class Cat(Animal):
    sound = "喵～"

    def __init__(self, name, type, size, character):
        super().__init__(type, size, character)
        self.name = name

    @property
    def is_pet(self):
        return False if self.is_beast else True


class Dog(Animal):
    sound = "汪汪汪～"

    def __init__(self, name, type, size, character):
        super().__init__(type, size, character)
        self.name = name

    @property
    def is_pet(self):
        return False if self.is_beast else True


class Zoo:
    def __init__(self, name):
        self.name = name
        self.__animals = dict()
        logger.info(f'__animals type: {type(self.__animals)}')

    def add_animal(self, animal):
        animal_class_name = animal.__class__.__name__
        logger.info(f'添加【{animal_class_name}】--【{animal.name}】')
        if animal_class_name in self.__animals:
            logger.info(f"【{animal_class_name}】--【{animal.name}】已存在，请勿重复添加~")
        else:
            self.__animals[animal_class_name] = animal

    def __getattr__(self, item):
        if item in self.__animals:
            return self.__animals[item]
        else:
            logger.warning(f"'{self.__class__.__name__}' object has no attribute '{item}'")


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')

    # 实例化两只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫1', '食肉', '小', '温顺')
    logger.info(f'【{cat1.name}】是凶猛动物：{cat1.is_beast}')
    logger.info(f'【{cat1.name}】适合作为宠物：{cat1.is_pet}')

    cat2 = Cat('大花猫2', '食肉', '大', '性格凶猛')
    logger.info(f'【{cat2.name}】是凶猛动物：{cat2.is_beast}')
    logger.info(f'【{cat2.name}】适合作为宠物：{cat2.is_pet}')

    # 增加两只猫到动物园
    z.add_animal(cat1)
    z.add_animal(cat2)

    # 动物园是否有猫这种动物
    has_cat = hasattr(z, 'Cat')
    logger.info(f'动物园有猫这种动物: {has_cat}')

    have_cat = hasattr(z, 'Dog')
    logger.info(f'动物园有狗这种动物: {has_cat}')

    logger.info(z.Cat)
    logger.info(z.Dog)
