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
    moveMade = False  # bandera referencia
    animate = False
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
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []
                    animate = True
            elif i.type == p.KEYDOWN:
                if i.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            #validMoves = gs.getValidMoves()
            moveMade = True
            animate=False

        # drawGameState(screen, gs, validMoves, sqSelected)
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
Selection squares
'''


def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whitemove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color("yellow"))
            for move in validMoves:
                if move.starCol == r and move.starCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


# def drawGameState(screen, gs, validMoves, sqSelected):
def drawGameState(screen, gs):
    drawBoard(screen)
    # highlightSquares(screen, gs, validMoves, sqSelected)
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


'''Animation'''


def animateMove(move, screen, board, clock):
    global colors
    dr = move.endRow - move.startRow
    dc = move.endCol - move.starCol
    framesPErSquare = 10
    frameCount = (abs(dr) + abs(dc)) * framesPErSquare
    for frame in range(frameCount):
        r, c = (move.startRow + dr * frame / frameCount, move.starCol + dc * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCapture != "--":
            screen.blit(IMAGES[move.pieceCapture], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()


