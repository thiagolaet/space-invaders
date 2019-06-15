from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
from actors import Jogador, Inimigos
import globals
import random

class Jogar(object):
    def __init__(self, janela):
        self.janela = janela
        self.pontuacao = 0
        self.nivel = 1
        self.teclado = janela.get_keyboard()
        self.jogador = Jogador(self.janela)
        self.inimigos = Inimigos(self.janela)

    def colisaoTiroInimigo(self):
        for i in range(len(self.inimigos.matrizInimigos)):
            for j in range(len(self.inimigos.matrizInimigos[i])):
                for k in range(len(self.jogador.listaTiros)):
                    if(Collision.collided(self.jogador.listaTiros[k], self.inimigos.matrizInimigos[i][j])):
                        self.inimigos.matrizInimigos[i].pop(j)
                        self.jogador.listaTiros.pop(k)
                        if(len(self.inimigos.matrizInimigos[i])) == 0:
                            self.inimigos.matrizInimigos.pop(i)
                        self.inimigos.quantidadeInimigos -= 1
                        return

    def run(self):
        self.inimigos.run()
        self.jogador.run()
        self.colisaoTiroInimigo()
        if(self.teclado.key_pressed("ESC")):
            globals.GAME_STATE = 1