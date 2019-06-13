from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.mouse import Mouse
import globals

class Ranking(object):
    def __init__(self, janela):
        self.janela = janela
        self.teclado = janela.get_keyboard()
        self.titulo = Sprite("assets/ranking_titulo.png", 1)
        self.set_pos()
        self._draw()

    def set_pos(self):
        self.titulo.set_position(self.janela.width/2 - self.titulo.width/2, 25)

    def _draw(self):
        self.titulo.draw()

    def run(self):
        self._draw()
        if(self.teclado.key_pressed("ESC")):
            globals.GAME_STATE =  1