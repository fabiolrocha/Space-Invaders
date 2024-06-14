import pygame  # Biblioteca para criar o jogo
import random  # Biblioteca para gerar aleatoriamente

# Inicialização do Pygame
pygame.init()

# ======================================================================

# Cores
preto = (0, 0, 0)  # Cor preta
vermelho = (255, 0, 0)  # Cor vermelha
branco = (255, 255, 255)  # Cor branca

# ======================================================================

# Tamanho da tela
x = 1280
y = 720

janela = pygame.display.set_mode((x, y))

# ======================================================================

# Nome do jogo
pygame.display.set_caption('Space Invaders')

# ======================================================================

# Imagens
nave_aliada = pygame.image.load('Imagens/Nave_Aliada.gif')
nave_inimiga = pygame.image.load('Imagens/Nave_Inimiga.gif')
tiro = pygame.image.load('Imagens/Tiro.png')
imagem_fundo = pygame.image.load('Imagens/Fundo_Espaço.jpg')

# ======================================================================

# Mudar o tamanho da imagem de fundo
imagem_fundo = pygame.transform.scale(imagem_fundo, (x, y))

# Tamanho da nave e rotação dela
nave_aliada = pygame.transform.scale(nave_aliada, (75, 75))
nave_aliada = pygame.transform.rotate(nave_aliada, -90)

# Tamanho da nave e rotação dela
nave_inimiga = pygame.transform.scale(nave_inimiga, (70, 70))

# Tamanho do tiro e rotação dele
tiro = pygame.transform.scale(tiro, (50, 50))
tiro = pygame.transform.rotate(tiro, -90)

# ======================================================================

#Transformar os personagens em objetos
nave_aliada_rect = nave_aliada.get_rect()
nave_inimiga_rect = nave_inimiga.get_rect()
tiro_rect = tiro.get_rect()

# ======================================================================

# Posições dos personagens
posicao_aliado_y = 360
posicao_aliado_x = 100

posicao_inimigo_y = 360
posicao_inimigo_x = 1100

posicao_tiro_y = 375
posicao_tiro_x = 105

# Velocidade dos personagens
velocidade_tiro = 0

# ======================================================================

# Variáveis
fonte = pygame.font.SysFont('joystix', 30, True, True)

atirar = False

loop = True

pause = False

vida = 3

pontos = 0

# ======================================================================

# Funções
def respawn():
    x = 1350
    y = random.randint(1, 645)
    return [x, y]

def respawn_tiro():
    atirar = False
    respawn_tiro_x = posicao_aliado_x + 5
    respawn_tiro_y = posicao_aliado_y + 15
    velocidade_tiro = 0
    return [respawn_tiro_x, respawn_tiro_y, atirar, velocidade_tiro]

def colisao():
    global pontos
    global vida
    if nave_aliada_rect.colliderect(nave_inimiga_rect):
        vida -= 0.5
        return True
    elif nave_inimiga_rect.x <= 10:
        pontos -= 1
        return True
    elif tiro_rect.colliderect(nave_inimiga_rect):
        pontos += 0.5
        return True
    else:
        return False

def mostrar_texto_centralizado(texto, fonte, cor, y_offset=0):
    texto_renderizado = fonte.render(texto, True, cor)
    rect_texto = texto_renderizado.get_rect(center=(640, 360 + y_offset))
    janela.blit(texto_renderizado, rect_texto)

def game_over():
    janela.fill(preto)
    mostrar_texto_centralizado("Game Over", pygame.font.SysFont('joystix', 60, True, True), vermelho, -100)
    mostrar_texto_centralizado(f"Pontuação: {int(pontos)}", fonte, branco)
    mostrar_texto_centralizado("Pressione R para reiniciar ou Q para sair", fonte, branco, 100)
    pygame.display.update()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True
                if evento.key == pygame.K_q:
                    pygame.quit()
                    exit()
    return False
def start_game():
    janela.fill(preto)
    mostrar_texto_centralizado("Space Invaders", pygame.font.SysFont('joystix', 60, True, True), vermelho, -100)
    mostrar_texto_centralizado("Pressione qualquer tecla para começar", fonte, branco)
    pygame.display.update()
    esperando1 = True
    while esperando1:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                esperando1 = False

def pause_game():
    janela.fill(preto)
    mostrar_texto_centralizado("Pausado", pygame.font.SysFont('joystix', 60, True, True), vermelho, -100)
    mostrar_texto_centralizado("Pressione ESC para continuar", fonte, branco)
    pygame.display.update()
    esperando2 = True
    while esperando2:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return True

# ======================================================================

start_game()

while loop:
    for events in pygame.event.get():
        # Sair do jogo
        if events.type == pygame.QUIT:
            loop = False
        # Pausar o jogo
        elif events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    pause_game()
        if vida == 0:
            if not game_over():
                loop = False
            else:
                vida = 3
                pontos = 0
                posicao_aliado_y = 360
                posicao_aliado_x = 100
                posicao_inimigo_y = 360
                posicao_inimigo_x = 1100
                posicao_tiro_y = 375
                posicao_tiro_x = 105
                velocidade_tiro = 0
# ======================================================================
#             
    # Imagem de fundo
    janela.blit(imagem_fundo, (0, 0))

# ======================================================================

    # Movimento do fundo
    rel_x = x % imagem_fundo.get_rect().width
    janela.blit(imagem_fundo, (rel_x - imagem_fundo.get_rect().width, 0))
    if rel_x < 1280:
        janela.blit(imagem_fundo, (rel_x, 0))

# ======================================================================

    # Movimento dos bonecos
    x -= 1  # Movimento do fundo
    posicao_inimigo_x -= 2  # Movimento do inimigo
    posicao_tiro_x += velocidade_tiro  # Movimento do tiro

# ======================================================================

    # Teclas de movimento
    tecla = pygame.key.get_pressed()
    # teclas do jogador andar no WASD
    if tecla[pygame.K_w] and posicao_aliado_y > 1:  # andar para cima
        posicao_aliado_y -= 1.5
        if not atirar:
            posicao_tiro_y -= 1.5
    if tecla[pygame.K_s] and posicao_aliado_y < 645:  # andar para baixo
        posicao_aliado_y += 1.5
        if not atirar:
            posicao_tiro_y += 1.5
    if tecla[pygame.K_a] and posicao_aliado_x > 1:  # andar para esquerda
        posicao_aliado_x -= 1.5
        if not atirar:
            posicao_tiro_x -= 1.5
    if tecla[pygame.K_d] and posicao_aliado_x < 1205:  # andar para direita
        posicao_aliado_x += 1.5
        if not atirar:
            posicao_tiro_x += 1.5
    # teclas do jogador andar nas setinhas
    if tecla[pygame.K_UP] and posicao_aliado_y > 1:  # andar para cima
        posicao_aliado_y -= 1.5
        if not atirar:
            posicao_tiro_y -= 1.5
    if tecla[pygame.K_DOWN] and posicao_aliado_y < 645:  # andar para baixo
        posicao_aliado_y += 1.5
        if not atirar:
            posicao_tiro_y += 1.5
    if tecla[pygame.K_LEFT] and posicao_aliado_x > 1:  # andar para esquerda
        posicao_aliado_x -= 1.5
        if not atirar:
            posicao_tiro_x -= 1.5
    if tecla[pygame.K_RIGHT] and posicao_aliado_x < 1205:  # andar para direita
        posicao_aliado_x += 1.5
        if not atirar:
            posicao_tiro_x += 1.5        
    # tecla de atirar
    if tecla[pygame.K_SPACE]:  # atirar
        atirar = True
        velocidade_tiro = 4

# ======================================================================

    #Posição da area de colisão
    nave_aliada_rect.x = posicao_aliado_x
    nave_aliada_rect.y = posicao_aliado_y

    nave_inimiga_rect.x = posicao_inimigo_x
    nave_inimiga_rect.y = posicao_inimigo_y

    tiro_rect.x = posicao_tiro_x
    tiro_rect.y = posicao_tiro_y

# ======================================================================
    # Respawn
    if posicao_inimigo_x <= 10 or colisao():
        respawn_pos = respawn()
        posicao_inimigo_x = respawn_pos[0]
        posicao_inimigo_y = respawn_pos[1]

    if posicao_tiro_x >= 1280 or colisao():
        respawn_tiro_pos = respawn_tiro()
        posicao_tiro_x = respawn_tiro_pos[0]
        posicao_tiro_y = respawn_tiro_pos[1]
        atirar = respawn_tiro_pos[2]
        velocidade_tiro = respawn_tiro_pos[3]

# ======================================================================

    # Texto
    score = fonte.render(f'Pontos:  {int(pontos)}', True, vermelho)
    janela.blit(score, (10, 10))

    sobrevivencia = fonte.render(f'Vidas:  {int(vida)}', True, vermelho)
    janela.blit(sobrevivencia, (10, 50))

# ======================================================================

    # Criar personagem
    janela.blit(tiro, (posicao_tiro_x, posicao_tiro_y))
    janela.blit(nave_aliada, (posicao_aliado_x, posicao_aliado_y))
    janela.blit(nave_inimiga, (posicao_inimigo_x, posicao_inimigo_y))

# ======================================================================

    # Atualizar a tela
    pygame.display.update()

# ======================================================================

# Encerrar o Pygame
pygame.quit()
