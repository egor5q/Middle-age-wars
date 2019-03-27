import os
import telebot
import time
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient



class Game:
    
    def __init__(self):
        self.players={}
        self.turn=1
        self.currentplayer=None


