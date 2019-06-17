from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.mouse import Mouse
import globals


class Dificuldade(object):
    def __init__(self, janela):
        self.janela = janela
        self.mouse = Mouse()
        self.teclado = janela.get_keyboard()
        self.titulo = Sprite("assets/dificuldade_titulo.png", 1)
        self.barra = Sprite("assets/dificuldade_barra.png", 1)
        self.seletor = Sprite("assets/dificuldade_seletor.png", 1)
        self.play = Sprite("assets/menu_play.png")
        self.playHover = Sprite("assets/menu_playhover.png")
        self.dificuldadePasso = 203
        self.set_pos()
        self._draw()
    
    def set_pos(self):
        self.titulo.set_position(self.janela.width/2 - self.titulo.width/2, 25)
        self.barra.set_position(self.janela.width/2 - self.barra.width/2, self.janela.height/2 - self.barra.height/2)
        self.seletor.set_position(self.janela.width/2 - self.seletor.width/2, 7 + self.janela.height/2 - self.seletor.height/2)
        self.play.set_position(self.janela.width/2 - self.play.width/2, self.janela.height/2 + 100)
        self.playHover.set_position(self.janela.width/2 - self.play.width/2, self.janela.height/2 + 100)

    def _draw(self):
        self.titulo.draw()
        self.barra.draw()
        self.seletor.draw()
        self.play.draw()   

    def checarDificuldade(self):
        if(self.seletor.x == self.janela.width/2 - self.seletor.width/2):
            dificuldade = 2
        elif(self.seletor.x == self.janela.width/2 - self.seletor.width/2 - self.dificuldadePasso):
            dificuldade = 1
        elif(self.seletor.x == self.janela.width/2 - self.seletor.width/2 + self.dificuldadePasso):
            dificuldade = 3
        return dificuldade

    def run(self):
        self.janela.set_background_color((0, 0, 0))
        self._draw()
        globals.DIFICULDADE = self.checarDificuldade()
        if(self.teclado.key_pressed("ESC")):
            globals.GAME_STATE = 1
        if(globals.DIFICULDADE == 2):
            if(self.teclado.key_pressed("LEFT")):
                self.seletor.x -= self.dificuldadePasso
                self.janela.delay(200)
            if(self.teclado.key_pressed("RIGHT")):
                self.seletor.x += self.dificuldadePasso
                self.janela.delay(200)
        if(globals.DIFICULDADE == 1):
            if(self.teclado.key_pressed("RIGHT")):
                self.seletor.x += self.dificuldadePasso
                self.janela.delay(200)
        if(globals.DIFICULDADE == 3):
            if(self.teclado.key_pressed("LEFT")):
                self.seletor.x -= self.dificuldadePasso
                self.janela.delay(200)
        if(self.mouse.is_over_object(self.play)):
            self.playHover.draw()
            if(self.mouse.is_button_pressed(1)):
                globals.GAME_STATE = 2
