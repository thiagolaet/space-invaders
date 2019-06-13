from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
import random

class Jogar(object):
    def __init__(self, janela):
        self.janela = janela
        self.pontuacao = 0
        self.nivel = 1
        self.tempo = 0
        self.teclado = janela.get_keyboard()

    def run(self):
        if this.teclado.