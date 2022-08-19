# Chessboard Function: Draws chessboard and pieces


def chessboard():

    import pygame
    import sys

    def load_white():

        for i in range(len(wp)):
            wp[i] = pygame.image.load('white/wp.png')
            t = 6 + (i * 8)
            screen.blit(wp[i], square[(6 + (i * 8))])
        for i in range(2):
            wn[i - 1] = pygame.image.load('white/wn.png')
            screen.blit(wn[i - 1], square[15 + (i * 40)])
        for i in range(2):
            wb[i - 1] = pygame.image.load('white/wb.png')
            screen.blit(wb[i - 1], square[23 + (i * 24)])
        for i in range(2):
            wr[i - 1] = pygame.image.load('white/wr.png')
            screen.blit(wr[i - 1], square[7 + (i * 56)])

        screen.blit(wk, square[39])

        screen.blit(wq, square[31])

    def load_black():

        for i in range(len(bp)):
            bp[i] = pygame.image.load('black/bp.png')
            screen.blit(bp[i], square[(-7 + (i * 8))])
        for i in range(2):
            bn[i - 1] = pygame.image.load('black/bn.png')
            screen.blit(bn[i - 1], square[8 + (i * 40)])
        for i in range(2):
            bb[i - 1] = pygame.image.load('black/bb.png')
            screen.blit(bb[i - 1], square[16 + (i * 24)])
        for i in range(2):
            br[i - 1] = pygame.image.load('black/br.png')
            screen.blit(br[i - 1], square[0 + (i * 56)])
        screen.blit(bk, square[32])
        screen.blit(bq, square[24])

    #def checkMovable(piece, sq):
        #if piece == wk or bk:
            #if sq == piece

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    square_size = 80
    square = []
    count1 = 0  # this will be the count to append to squares
    count = 1
    white = (255, 255, 255)
    black = (124, 88, 62)
    bg = (255, 255, 204)
    wp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    wp_pos = []
    wn = ['B', 'G']
    wn_pos = []
    wr = ['A', 'H']
    wr_pos = []
    wb = ['C', 'F']
    wb_pos = []
    bp = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    bp_pos = []
    bn = ['B', 'G']
    bn_pos = []
    br = ['A', 'H']
    br_pos = []
    bb = ['C', 'F']
    bb_pos = []
    bk = pygame.image.load('black/bk.png')
    bk_pos = []
    bq = pygame.image.load('black/bq.png')
    bq_pos = []
    wk = pygame.image.load('white/wk.png')
    wk_pos = []
    wq = pygame.image.load('white/wq.png')
    wq_pos = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(bg)
        for row in range(1, 9):
            for column in range(1, 9):
                square.append(count1)
                if count % 2 == 0:
                    square[count1] = pygame.draw.rect(screen, black,
                                                      [square_size * row, square_size * column, square_size,
                                                       square_size])
                else:
                    square[count1] = pygame.draw.rect(screen, white,
                                                      [square_size * row, square_size * column, square_size,
                                                       square_size])
                count += 1
                count1 += 1
            count -= 1
        pygame.draw.rect(screen, black, [square_size, square_size, square_size * 8, square_size * 8], 1)
        load_white()
        load_black()
        print(wp[0])
        pygame.display.update()


chessboard()
