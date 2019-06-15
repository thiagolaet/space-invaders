from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
import globals

class Jogador(object):
    def __init__(self, janela):
        self.janela = janela
        self.player = Sprite("assets/jogo_jogador.png")
        self.listaTiros = []
        self.teclado = self.janela.get_keyboard()
        self.cronometroTiros = 0
        self.set_pos()
        self._draw()

    def set_pos(self):
        self.player.set_position(self.janela.width/2 - self.player.width/2, self.janela.height - 50)
    
    def _draw(self):
        self.player.draw()
        for i in range(len(self.listaTiros)):
            self.listaTiros[i].draw()

    def atirar(self):
        tiro = Sprite("assets/jogo_tiro.png")
        tiro.set_position(self.player.x + self.player.width/2 - tiro.width/2, self.player.y)
        self.listaTiros.append(tiro)

    def atualizarTiros(self):
        for i in range(len(self.listaTiros)):
            self.listaTiros[i].move_y(self.janela.delta_time() * globals.FRAME_PER_SECOND *-5)
            if(self.listaTiros[i].y <= 0):
                self.listaTiros.pop(i)
                break

    def run(self):        
        #Andar para os lados
        self.player.move_key_x(10 * self.janela.delta_time() * globals.FRAME_PER_SECOND)
        
        #Atirar
        if(self.cronometroTiros >= 0.6):
            if(self.teclado.key_pressed("UP")):
                self.atirar()
                self.cronometroTiros = 0
        self.cronometroTiros += self.janela.delta_time()

        #Checagem de laterais da tela
        if(self.player.x < 0):
            self.player.set_position(0, self.janela.height-50)
        if(self.player.x + self.player.width > self.janela.width):
            self.player.x = self.janela.width - self.player.width
        
        #Mover os tiros e remover da lista
        self.atualizarTiros()

        self._draw()

class Inimigos(object):
    def __init__(self, janela, nivel):
        self.janela = janela
        self.matrizInimigos = []
        self.quantidadeColunas = 5 + globals.DIFICULDADE
        self.quantidadeLinhas = 5 + globals.DIFICULDADE
        self.cronometroAvancar = 0
        self.nivel = nivel
        self.quantidadeInimigos = self.quantidadeColunas * self.quantidadeLinhas
        self.velocidadeInimigos = (5 * globals.DIFICULDADE * self.janela.delta_time())/self.quantidadeInimigos
        self.direcaoInimigos = 1
        self.spawn()

    def spawn(self):
        for i in range(self.quantidadeColunas):
            self.matrizInimigos.append([])
            for j in range(self.quantidadeLinhas):
                self.matrizInimigos[i].append(Sprite("assets/jogo_inimigo.png"))
                #Arrumar isto
                self.matrizInimigos[i][j].set_position((j+1)* (self.janela.width/(self.janela.width/60)), (i+1)*50)

    def moverInimigos(self):
        #Atualizando velocidade dos inimigos
        if self.quantidadeInimigos > 0:
            self.velocidadeInimigos = ((self.nivel + 10) * globals.DIFICULDADE * self.direcaoInimigos)/(self.quantidadeInimigos / self.nivel)
        for i in range(len(self.matrizInimigos)):
            for j in range(len(self.matrizInimigos[i])):
                self.matrizInimigos[i][j].move_x(self.janela.delta_time() * globals.FRAME_PER_SECOND * globals.DIFICULDADE * self.velocidadeInimigos)
    
    def checarLimitesLaterais(self):
        for i in range(len(self.matrizInimigos)):
            for j in range(len(self.matrizInimigos[i])):
                if (self.matrizInimigos[i][j].x <= 0) or (self.matrizInimigos[i][j].x >= (self.janela.width - self.matrizInimigos[i][j].width)):
                    return True
        return False

    def avancarInimigos(self):
        if self.cronometroAvancar > 0.15:
            if self.checarLimitesLaterais():
                self.direcaoInimigos = -self.direcaoInimigos
                for i in range(len(self.matrizInimigos)):
                    for j in range(len(self.matrizInimigos[i])):
                        self.matrizInimigos[i][j].y += 20
                self.cronometroAvancar = 0
        else: self.cronometroAvancar += self.janela.delta_time()

    def _draw(self):
        for i in range(len(self.matrizInimigos)):
            for j in range(len(self.matrizInimigos[i])):
                self.matrizInimigos[i][j].draw()
    
    def run(self):
        if self.quantidadeInimigos == 0:
            self.passarNivel()
        self.moverInimigos()
        self.avancarInimigos()
        self._draw()