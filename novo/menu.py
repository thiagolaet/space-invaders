from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.mouse import Mouse
import globals


class Menu(object):
    def __init__(self, janela):
        self.janela = janela
        self.distancia = 40
        self.play = Sprite("assets/menu_play.png")
        self.playHover = Sprite("assets/menu_playhover.png")
        self.dificuldade = Sprite("assets/menu_dificuldade.png")
        self.dificuldadeHover = Sprite("assets/menu_dificuldadehover.png")
        self.ranking = Sprite("assets/menu_ranking.png")
        self.rankingHover = Sprite("assets/menu_rankinghover.png")
        self.sair = Sprite("assets/menu_sair.png")
        self.sairHover = Sprite("assets/menu_sairhover.png")
        self.mouse = Mouse()
        self.set_pos()
        self._draw()

    def set_pos(self):
        self.play.set_position(self.janela.width/2 - self.play.width/2, self.distancia)
        self.playHover.set_position(self.janela.width/2 - self.play.width/2, self.distancia)
        self.dificuldade.set_position(self.janela.width/2 - self.dificuldade.width/2, 2*self.distancia + self.play.height)
        self.dificuldadeHover.set_position(self.janela.width/2 - self.dificuldade.width/2, 2*self.distancia + self.play.height)
        self.ranking.set_position(self.janela.width/2 - self.ranking.width/2, 3*self.distancia + self.ranking.height + self.play.height)
        self.rankingHover.set_position(self.janela.width/2 - self.ranking.width/2, 3*self.distancia + self.ranking.height + self.play.height)
        self.sair.set_position(self.janela.width/2 - self.sair.width/2, 4*self.distancia + self.ranking.height + self.play.height + self.ranking.height)
        self.sairHover.set_position(self.janela.width/2 - self.sair.width/2, 4*self.distancia + self.ranking.height + self.play.height + self.ranking.height)

    def _draw(self):
        self.play.draw()
        self.dificuldade.draw() 
        self.ranking.draw() 
        self.sair.draw() 

    def run(self):
        self._draw()
        self.set_pos()
        if(self.mouse.is_over_object(self.play)):
            self.playHover.draw()
            if(self.mouse.is_button_pressed(1)):
                globals.GAME_STATE = 2
        if(self.mouse.is_over_object(self.dificuldade)):
            self.dificuldadeHover.draw()
            if(self.mouse.is_button_pressed(1)):
                globals.GAME_STATE = 3
        if(self.mouse.is_over_object(self.ranking)):
            self.rankingHover.draw()
            if(self.mouse.is_button_pressed(1)):
                globals.GAME_STATE = 4
        if(self.mouse.is_over_object(self.sair)):
            self.sairHover.draw()
            if(self.mouse.is_button_pressed(1)):
                globals.GAME_STATE = 5
