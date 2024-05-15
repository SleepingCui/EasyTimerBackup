from json_read import *
import logging
def debugging():
    global config
    config = json_read()
    if config["debug"]["debug_mode"] == True:
        return True
    else:
        return False