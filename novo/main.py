from PPlay.keyboard import Keyboard
from PPlay.window import Window
from menu import Menu
from dificuldade import Dificuldade
from ranking import Ranking
from jogo import Jogar
import globals

janela = Window(globals.WIDTH, globals.HEIGHT)
janela.set_title("Space Invaders")

menu = Menu(janela)
dificuldade = Dificuldade(janela)
ranking = Ranking(janela)
jogo = Jogar(janela)


while globals.GAME_STATE != 5:
    janela.set_background_color((0, 0, 0))

    if globals.GAME_STATE == 1:
        menu.run()
    elif globals.GAME_STATE == 2:
        jogo.run()
    elif globals.GAME_STATE == 3:
        dificuldade.run()
        jogo = Jogar(janela)
    elif globals.GAME_STATE == 4:
        ranking.run()

    janela.update()