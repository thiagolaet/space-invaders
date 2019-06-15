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
        self.FPS = 0
        self.fpsAtual = 0
        self.cronometroFPS = 0
        self.teclado = janela.get_keyboard()
        self.jogador = Jogador(self.janela)
        self.inimigos = Inimigos(self.janela, self.nivel)

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

    def passarNivel(self):
        self.nivel += 1
        self.inimigos.quantidadeColunas += globals.DIFICULDADE
        self.inimigos.quantidadeLinhas += globals.DIFICULDADE
        self.inimigos.spawn()
        self.inimigos.quantidadeInimigos = self.inimigos.quantidadeColunas * self.inimigos.quantidadeLinhas

    def run(self):
        self.cronometroFPS += self.janela.delta_time()
        self.FPS += 1
        if self.cronometroFPS > 1: 
            self.fpsAtual = self.FPS   
            self.FPS = 0
            self.cronometroFPS = 0
        if self.inimigos.quantidadeInimigos == 0:
            self.passarNivel()
        self.inimigos.run()
        self.jogador.run()
        self.colisaoTiroInimigo()
        
        #Desenhando textos
        self.janela.draw_text(str(self.fpsAtual), 0, 0, size=12, color=(255,255,255))
        self.janela.draw_text("Level: " + str(self.nivel), 280, 5, size=28, color=(255,255,255), font_name="Minecraft")
        
        if(self.teclado.key_pressed("ESC")):
            globals.GAME_STATE = 1