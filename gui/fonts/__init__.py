import os
from kivy.resources import resource_add_path, resource_find


resource_add_path(os.path.dirname(os.path.abspath(__file__)))
RAYSSO_FONT = resource_find("RaySSOFont.ttf")

