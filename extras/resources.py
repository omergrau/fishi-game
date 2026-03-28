import os
import sys

def load_resource(filename,type=""):
    """if 'js' in sys.modules and type== "image":
        path = os.path.join('assets/images', filename)
    if 'js' in sys.modules and type== "music":
        path = os.path.join('assets/music', filename)"""
    if 'js' in sys.modules :
        path = os.path.join('assets', filename)
    elif hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, filename)
    else:
        path = os.path.join("", filename[3:])
    return path


def entry_load():
    ocean = load_resource("../assets/images/ocean.png")
    lose_video_game = load_resource("../assets/music/lose_video-game.wav")
    main_game_music = load_resource("../assets/music/game-music-loop.wav")
    crunch = load_resource("../assets/music/plastic-crunch.wav")
    return ocean, lose_video_game, main_game_music, crunch