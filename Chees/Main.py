'''Menu del ajedres'''

import pygame as p
from Chees import engine

WIDTH = HEIGHT = 512
DIMENSION = 4
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImage():
    piez = ["wK", "bK"]
    for pie in piez:
        IMAGES[pie] = p.transform.scale(p.image.load("Piezas/" + pie + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False   #bandera referencia

    loadImage()
    running = True
    sqSelected = ()  # cuadro no seleccionadao
    playerClicks = []
    while running:
        for i in p.event.get():
            if i.type == p.QUIT:
                running = False
            elif i.type == p.MOUSEBUTTONUP:
                location = p.mouse.get_pos()  # lugar del mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append((sqSelected))
                if len(playerClicks) == 2:
                    move = engine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            elif i.type == p.KEYDOWN:
                if i.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = True

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)


'''Se dibuja el teclado'''


def drawBoard(screen):
    colors = [p.Color(249, 231, 159), p.Color(187, 104, 39)]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i + j) % 2)]
            p.draw.rect(screen, color, p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''Se dibujan las piezas'''


def drawPieces(screen, board):
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            piece = board[i][j]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(j * SQ_SIZE, i * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()

