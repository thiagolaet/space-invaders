from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.gameobject import *
from PPlay.collision import *
import random

#main --------------------------------------------------------------------------------------------------------------
janela = Window(800, 600)
mouse = janela.get_mouse()
teclado = janela.get_keyboard()
GAME_STATE = 1
janela.set_title("SPACE INVADERS")
frame_per_SECOND = 60
speed_per_SECOND = 60
tempoFPS = 0
fpsAtual = 0
FPS = 0
dificuldade = 2
velocidadeInimigos = 0.2
nivel = 1
pontuacao = 0

#---------------------------------------------------------------------------------------------------------------

#menu --------------------------------------------------------------------------------------------------------------
distancia = 40
play_menu = Sprite("sprites/menu_play.png")
play_menu.set_position(janela.width/2 - play_menu.width/2, distancia)
play_menuHover = Sprite("sprites/menu_playhover.png")
play_menuHover.set_position(janela.width/2 - play_menu.width/2, distancia)

dificuldade_menu = Sprite("sprites/menu_dificuldade.png")
dificuldade_menu.set_position(janela.width/2 - dificuldade_menu.width/2, 2*distancia + play_menu.height)
dificuldade_menuHover = Sprite("sprites/menu_dificuldadehover.png")
dificuldade_menuHover.set_position(janela.width/2 - dificuldade_menu.width/2, 2*distancia + play_menu.height)

ranking_menu = Sprite("sprites/menu_ranking.png")
ranking_menu.set_position(janela.width/2 - ranking_menu.width/2, 3*distancia + ranking_menu.height + play_menu.height)
ranking_menuHover = Sprite("sprites/menu_rankinghover.png")
ranking_menuHover.set_position(janela.width/2 - ranking_menu.width/2, 3*distancia + ranking_menu.height + play_menu.height)

sair = Sprite("sprites/menu_sair.png")
sair.set_position(janela.width/2 - sair.width/2, 4*distancia + ranking_menu.height + play_menu.height + ranking_menu.height)
sairHover = Sprite("sprites/menu_sairhover.png")
sairHover.set_position(janela.width/2 - sair.width/2, 4*distancia + ranking_menu.height + play_menu.height + ranking_menu.height)

def menu(mouse, janela, play_menu, dificuldade_menu, ranking_menu, sair): 
    play_menu.draw()
    dificuldade_menu.draw()
    ranking_menu.draw()
    sair.draw()
    if(mouse.is_over_object(play_menu)):
        play_menuHover.draw()
        if(mouse.is_button_pressed(1)):
            return 2
    if(mouse.is_over_object(dificuldade_menu)):
        dificuldade_menuHover.draw()
        if(mouse.is_button_pressed(1)):
            return 3
    if(mouse.is_over_object(ranking_menu)):
        ranking_menuHover.draw()
        if(mouse.is_button_pressed(1)):
            return 4
    if(mouse.is_over_object(sair)):
        sairHover.draw()
        if(mouse.is_button_pressed(1)):
            return 5
    return 1
#---------------------------------------------------------------------------------------------------------------

#jogo --------------------------------------------------------------------------------------------------------------

jogador = Sprite("sprites/jogo_jogador.png")
jogador.set_position(janela.width/2 - jogador.width/2,janela.height-50)

#tiros ------------------------------------------------------------------------------------
ultimoTiro = 1
listaTiros = []

class tiro():
    def __init__(self):
        self.sprite = Sprite("sprites/jogo_tiro.png")

def atirar(listaTiros):
    tiroAtual = tiro()
    tiroAtual.sprite.set_position(jogador.x + jogador.width/2 - tiroAtual.sprite.width/2, jogador.y)
    listaTiros.append(tiroAtual)

def moverTiros(listaTiros):
    for i in range(len(listaTiros)):
        listaTiros[i].sprite.move_y(janela.delta_time() * speed_per_SECOND *-5)
        if(listaTiros[i].sprite.y <= 0):
            listaTiros.pop(i)
            break

#-------------------------------------------------------------------------------

#inimigos ------------------------------------------------------------------------------------

existemInimigos = 0

def checarExistemInimigos(matrizInimigos):
    existemInimigos = 0
    for i in range(int(janela.height/80)):
        for j in range(int(janela.width/80)):
            if matrizInimigos[i][j] != None:
                return 0
    return 1
        
#contador que impede que os inimigos avancem muitas vezes 
contadorLateral = 0


matrizInimigos = []

for i in range(int(janela.height/80)):
    matrizInimigos.append([])
    for j in range(int(janela.width/80)):
        matrizInimigos[i].append([])

def gerarInimigos():
    global matrizInimigos
    for i in range(int(janela.height/80)):
        for j in range(int(janela.width/80)):
            matrizInimigos[i][j] = Sprite("sprites/jogo_inimigo.png")
            matrizInimigos[i][j].set_position((j+1)* (janela.width/(janela.width/60)), (i+1)*50)
    return matrizInimigos

def desenharInimigos(matrizInimigos):
    for i in range(int(janela.height/80)):
        for j in range(int(janela.width/80)):
            if matrizInimigos[i][j] != None:
                matrizInimigos[i][j].draw()

def moverInimigos(matrizInimigos, velocidadeInimigos):
    for i in range(int(janela.height/80)):
        for j in range(int(janela.width/80)):
            if matrizInimigos[i][j] != None:
                matrizInimigos[i][j].move_x(janela.delta_time() * speed_per_SECOND * dificuldade * velocidadeInimigos)
    return matrizInimigos

def avancarInimigos(matrizInimigos):
    global velocidadeInimigos
    for i in range(int(janela.height/80)):
        for j in range(int(janela.width/80)):
            if matrizInimigos[i][j] != None:
                matrizInimigos[i][j].y += 10
    return matrizInimigos

def checarLimites(matrizInimigos):
    if(contadorLateral > 2):
        for i in range(int(janela.height/80)):
            for j in range(int(janela.width/80)):
                if(matrizInimigos[i][j] != None):
                    if matrizInimigos[i][j].x <= 0 or matrizInimigos[i][j].x >= janela.width - matrizInimigos[i][j].width:
                        return True
    return False

def checarColisao():
    global pontuacao
    global nivel
    global dificuldade
    for i in range(int(janela.height/80)):
        for j in range(int(janela.width/80)):
            for k in range(len(listaTiros)):
                if(matrizInimigos[i][j] != None):
                    if(Collision.collided(listaTiros[k].sprite, matrizInimigos[i][j])):
                        pontuacao += 10 * dificuldade * nivel
                        matrizInimigos[i][j] = None
                        listaTiros.pop(k)
    return matrizInimigos

def novaVelocidade():
    global velocidadeInimigos
    velocidadeInimigos = nivel * dificuldade *0.2
#---------------------------------------------------------------

def TelaJogo( dificuldade):
    global ultimoTiro
    global existemInimigos
    global velocidadeInimigos
    global contadorLateral
    global nivel
    global pontuacao
    janela.set_background_color((0, 0, 0))
    jogador.draw()
    ultimoTiro += janela.delta_time()
    contadorLateral += janela.delta_time()
    global matrizInimigos
    if existemInimigos == 0:
        matrizInimigos = gerarInimigos()
        existemInimigos = 1
    moverInimigos(matrizInimigos, velocidadeInimigos)
    if ultimoTiro >= 0.3:
        if(teclado.key_pressed("UP")):
            atirar(listaTiros)
            ultimoTiro = 0
    for i in range(len(listaTiros)):
        listaTiros[i].sprite.draw()
    jogador.move_key_x(10 * janela.delta_time() * frame_per_SECOND)
    if(teclado.key_pressed("ESC")):
        pontuacao = 0
        listaTiros.clear()
        existemInimigos = 0
        nivel = 1
        return 1;
    if(jogador.x < 0):
        jogador.set_position(0, janela.height-50)
    if(jogador.x + jogador.width > janela.width):
        jogador.x = janela.width - jogador.width
    moverTiros(listaTiros)
    if(checarLimites(matrizInimigos)):
        velocidadeInimigos = -(velocidadeInimigos)
        avancarInimigos(matrizInimigos)
        contadorLateral = 0
    desenharInimigos(matrizInimigos)
    if checarExistemInimigos(matrizInimigos):
        nivel += 1
        novaVelocidade()
        existemInimigos = 0
    checarColisao()
    janela.draw_text("Pontos: " + str(pontuacao), 400, 5, size=28, color=(255,255,255), font_name="Minecraft")
    janela.draw_text("Level: " + str(nivel), 280, 5, size=28, color=(255,255,255), font_name="Minecraft")
    return 2;

#--------------------------------------------------------------------------------------------------------------------

#dificuldade --------------------------------------------------------------------------------------------------------------

dificuldadeTitulo = Sprite("sprites/dificuldade_titulo.png", 1)
dificuldadeTitulo.set_position(janela.width/2 - dificuldadeTitulo.width/2, 25)

dificuldadeBarra = Sprite("sprites/dificuldade_barra.png", 1)
dificuldadeBarra.set_position(janela.width/2 - dificuldadeBarra.width/2, janela.height/2 - dificuldadeBarra.height/2)

dificuldadeSeletor = Sprite("sprites/dificuldade_seletor.png", 1)
dificuldadeSeletor.set_position(janela.width/2 - dificuldadeSeletor.width/2, 7 + janela.height/2 - dificuldadeSeletor.height/2)

dificuldadePlay = Sprite("sprites/menu_play.png")
dificuldadePlay.set_position(janela.width/2 - dificuldadePlay.width/2, janela.height/2 + 100)
dificuldadePlayHover = Sprite("sprites/menu_playhover.png")
dificuldadePlayHover.set_position(janela.width/2 - dificuldadePlay.width/2, janela.height/2 + 100)

dificuldadePasso = 203

#1 = Facil / 2 = Medio / 3 = Dificil

def TelaDificuldade():
    janela.set_background_color((0, 0, 0))
    dificuldadeTitulo.draw()
    dificuldadeBarra.draw()
    dificuldadeSeletor.draw()
    dificuldadePlay.draw()
    global dificuldade
    dificuldade = checarDificuldade()
    if(teclado.key_pressed("ESC")):
        return 1;
    if(dificuldade == 2):
        if(teclado.key_pressed("LEFT")):
            dificuldadeSeletor.x -= dificuldadePasso
            janela.delay(200)
        if(teclado.key_pressed("RIGHT")):
            dificuldadeSeletor.x += dificuldadePasso
            janela.delay(200)
    if(dificuldade == 1):
        if(teclado.key_pressed("RIGHT")):
            dificuldadeSeletor.x += dificuldadePasso
            janela.delay(200)
    if(dificuldade == 3):
        if(teclado.key_pressed("LEFT")):
            dificuldadeSeletor.x -= dificuldadePasso
            janela.delay(200)
    if(mouse.is_over_object(dificuldadePlay)):
        dificuldadePlayHover.draw()
        if(mouse.is_button_pressed(1)):
            return 2
    return 3;

def checarDificuldade():
    if(dificuldadeSeletor.x == janela.width/2 - dificuldadeSeletor.width/2):
        dificuldade = 2
    elif(dificuldadeSeletor.x == janela.width/2 - dificuldadeSeletor.width/2 - dificuldadePasso):
        dificuldade = 1
    elif(dificuldadeSeletor.x == janela.width/2 - dificuldadeSeletor.width/2 + dificuldadePasso):
        dificuldade = 3
    return dificuldade


#--------------------------------------------------------------------------------------------------------------------

#ranking --------------------------------------------------------------------------------------------------------------

rankingTitulo = Sprite("sprites/ranking_titulo.png", 1)
rankingTitulo.set_position(janela.width/2 - rankingTitulo.width/2, 25)

def TelaRanking():
    janela.set_background_color((0, 0, 0))
    rankingTitulo.draw()
    if(teclado.key_pressed("ESC")):
        return 1;
    return 4;

#--------------------------------------------------------------------------------------------------------------------

while True:
    tempoFPS += janela.delta_time()
    FPS += 1
    if tempoFPS > 1: 
        fpsAtual = FPS   
        FPS = 0
        tempoFPS = 0

    if(GAME_STATE == 1):
        janela.set_background_color((0, 0, 0))
        GAME_STATE = menu(mouse, janela, play_menu, dificuldade_menu, ranking_menu, sair)
        jogador.set_position(janela.width/2 - jogador.width/2,janela.height-50)

    if GAME_STATE == 2:
        GAME_STATE = TelaJogo(dificuldade)

    if GAME_STATE == 3:
        GAME_STATE = TelaDificuldade()

    if GAME_STATE == 4:
        GAME_STATE = TelaRanking()

    if GAME_STATE == 5:
        break

    janela.draw_text(str(fpsAtual), 0, 0, size=12, color=(255,255,255))
    janela.update()

