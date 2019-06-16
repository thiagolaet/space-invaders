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
        self.vivo = True

        self.gameOverImg = Sprite("assets/game_over.png")
        self.gameOverImg.set_position(self.janela.width/2 - self.gameOverImg.width/2, self.janela.height/2 - self.gameOverImg.height/2)

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
        if self.inimigos.quantidadeColunas > self.janela.width/60 - 1:
            self.inimigos.quantidadeColunas = int(self.janela.width/60 - 1)
        if self.inimigos.quantidadeLinhas > self.janela.height/60 - 2:
            self.inimigos.quantidadeLinhas = int(self.janela.height/60-2)
        self.inimigos.spawn()
        self.inimigos.quantidadeInimigos = self.inimigos.quantidadeColunas * self.inimigos.quantidadeLinhas

    def checarGameOverY(self):
        for i in range(len(self.inimigos.matrizInimigos)):
            for j in range(len(self.inimigos.matrizInimigos[i])):
                if (self.inimigos.matrizInimigos[i][j].y >= self.jogador.player.y):
                    return True
        return False

    def colisaoTiroPlayer(self):
        for i in range(len(self.inimigos.listaTiros)):
            if Collision.collided(self.inimigos.listaTiros[i], self.jogador.player):
                self.jogador.vidas -= 1
                self.inimigos.listaTiros.pop(i)
                break
    
    def gameOver(self):
        if(self.teclado.key_pressed("ESC")):
            globals.GAME_STATE = 1
        self.gameOverImg.draw()
        self.janela.draw_text(str(self.pontuacao) + " Pontos", self.janela.width/2 - 80, self.janela.height/2 + self.gameOverImg.height, size=40, color=(255,255,255), font_name="Minecraft")

    def run(self):
        self.cronometroFPS += self.janela.delta_time()
        self.FPS += 1
        if self.cronometroFPS > 1: 
            self.fpsAtual = self.FPS   
            self.FPS = 0
            self.cronometroFPS = 0
            
        if self.vivo: 
            if self.inimigos.quantidadeInimigos == 0:
                self.passarNivel()
            self.inimigos.run()
            self.jogador.run()
            self.colisaoTiroInimigo()
            self.colisaoTiroPlayer()

            #Desenhando textos
            self.janela.draw_text("Vidas: " + str(self.jogador.vidas), 150, 5, size=28, color=(255,255,255), font_name="Minecraft")
            self.janela.draw_text(str(self.fpsAtual), 0, 0, size=12, color=(255,255,255))
            self.janela.draw_text("Nivel: " + str(self.nivel), 280, 5, size=28, color=(255,255,255), font_name="Minecraft")
            
            if(self.teclado.key_pressed("ESC")):
                self.nivel = 1
                self.inimigos = Inimigos(self.janela, self.nivel)
                self.jogador = Jogador(self.janela)
                globals.GAME_STATE = 1

            if self.checarGameOverY() or self.jogador.vidas == 0:
                self.nivel = 1
                self.inimigos = Inimigos(self.janela, self.nivel)
                self.jogador = Jogador(self.janela)
                self.vivo = False

        else:
            self.gameOver()





