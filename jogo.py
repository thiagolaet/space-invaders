from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
from PPlay.animation import *
from actors import Jogador, Inimigos
import globals
import random

class Jogar(object):
    def __init__(self, janela):
        self.janela = janela
        self.pontuacao = 0
        self.tempo = 0
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
        
        self.playerDead = Animation("assets/jogo_jogador-respawn.png", 12)
        self.playerDead.set_total_duration(1000)
        self.cronometroMorte = 1

    def colisaoTiroInimigo(self):
        for i in range(len(self.inimigos.matrizInimigos)):
            for j in range(len(self.inimigos.matrizInimigos[i])):
                for k in range(len(self.jogador.listaTiros)):
                    if(Collision.collided(self.jogador.listaTiros[k], self.inimigos.matrizInimigos[i][j])):
                        self.pontuacao += 50 + 50 / self.tempo
                        self.inimigos.matrizInimigos[i].pop(j)
                        self.jogador.listaTiros.pop(k)
                        if(len(self.inimigos.matrizInimigos[i])) == 0:
                            self.inimigos.matrizInimigos.pop(i)
                        self.inimigos.quantidadeInimigos -= 1
                        return

    def reset(self):
        self.nivel = 1
        self.pontuacao = 0
        self.vivo = 1
        self.inimigos = Inimigos(self.janela, self.nivel)
        self.jogador = Jogador(self.janela)
        self.cronometroMorte = 1

    def passarNivel(self):
        self.pontuacao += self.nivel * 1000
        self.nivel += 1
        self.inimigos.quantidadeColunas += globals.DIFICULDADE
        self.inimigos.quantidadeLinhas += globals.DIFICULDADE
        if self.inimigos.quantidadeColunas > self.janela.width/60 - 1:
            self.inimigos.quantidadeColunas = int(self.janela.width/60 - 1)
        if self.inimigos.quantidadeLinhas > self.janela.height/60 - 2:
            self.inimigos.quantidadeLinhas = int(self.janela.height/60-2)
        self.jogador.listaTiros.clear()
        self.inimigos.listaTiros.clear()
        self.tempo = 0
        self.inimigos.spawn()
        self.inimigos.quantidadeInimigos = self.inimigos.quantidadeColunas * self.inimigos.quantidadeLinhas

    def checarGameOverY(self):
        for i in range(len(self.inimigos.matrizInimigos)):
            for j in range(len(self.inimigos.matrizInimigos[i])):
                if (self.inimigos.matrizInimigos[i][j].y + self.inimigos.matrizInimigos[i][j].height >= self.jogador.player.y):
                    return True
        return False

    def colisaoTiroPlayer(self):
        for i in range(len(self.inimigos.listaTiros)):
            if Collision.collided(self.inimigos.listaTiros[i], self.jogador.player):
                self.jogador.vidas -= 1
                self.inimigos.listaTiros.pop(i)
                self.respawn()
                self.cronometroMorte = 0
                break

    def respawn(self):            
        self.playerDead.set_curr_frame(0)
        self.playerDead.set_position(self.jogador.player.x, self.jogador.player.y)
        self.jogador.player.set_position(self.janela.width/2 - self.jogador.player.width/2, self.janela.height - 50)
    
    def gameOver(self):
        if(self.teclado.key_pressed("ESC")):
            globals.GAME_STATE = 1
            self.reset()
        self.gameOverImg.draw()
        self.janela.draw_text("Pontos: " + str(int(self.pontuacao)), self.janela.width/2 - 120, self.janela.height/2 + self.gameOverImg.height, size=40, color=(255,255,255), font_name="Minecraft")

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

            self.tempo += self.janela.delta_time()

            #Desenhando textos
            self.janela.draw_text("Vidas: " + str(self.jogador.vidas), 150, 5, size=28, color=(255,255,255), font_name="Minecraft")
            self.janela.draw_text(str(self.fpsAtual), 0, 0, size=12, color=(255,255,255))
            self.janela.draw_text("Nivel: " + str(self.nivel), 280, 5, size=28, color=(255,255,255), font_name="Minecraft")
            self.janela.draw_text("Pontos: " + str(int(self.pontuacao)), 450, 5, size=28, color=(255,255,255), font_name="Minecraft")

            
            if(self.teclado.key_pressed("ESC")):
                globals.GAME_STATE = 1
                self.reset()

            if self.checarGameOverY() or self.jogador.vidas == 0:
                self.nivel = 1
                self.inimigos = Inimigos(self.janela, self.nivel)
                self.jogador = Jogador(self.janela)
                self.vivo = False
            
            if self.cronometroMorte < 0.9:
                self.playerDead.draw()
                self.playerDead.update()
                self.cronometroMorte += self.janela.delta_time()

        else:
            self.gameOver()





