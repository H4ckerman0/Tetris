import os, sys

SCREEN_WIDTH = 504
SCREEN_HEIGHT = 630
TILESIZE = 42

if getattr(sys, 'frozen', False):
    game_path = os.path.dirname(sys.executable)
elif __file__:
    game_path = os.path.dirname(__file__)

block_data = {
    "blue": game_path + r"\graphics\blocks\blue.png", 
    "cyan": game_path + r"\graphics\blocks\cyan.png",
    "green": game_path + r"\graphics\blocks\green.png",
    "orange": game_path + r"\graphics\blocks\orange.png",
    "purple": game_path + r"\graphics\blocks\purple.png",
    "red": game_path + r"\graphics\blocks\red.png",
    "yellow": game_path + r"\graphics\blocks\yellow.png",
    "pink": game_path + r"\graphics\blocks\pink.png"
    }