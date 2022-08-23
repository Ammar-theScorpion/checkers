import pygame
import threading
import sys
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece



class Board:

    def get_pos(self):
        while True:
            x = self.n.get()
            print(x.rem)

            if x.rem:
                self.board[7-x.atx][x.aty] = 0
                if x.color == RED:
                    self.red_left-=1
                else:
                    self.white_left-=1
            else:
                self.can = True
                x.row = 7-x.row
                v = self.board[7-x.atx][x.aty]
                self.board[7-x.atx][x.aty], self.board[x.row][x.col] = self.board[x.row][x.col], self.board[7-x.atx][x.aty]
                self.board[x.row][x.col].move(x.row, x.col, 7-x.atx, x.aty)
                self.draw(self.win)
                pygame.display.update()

    def __init__(self, n, win):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.n = n
        self.can = False
        self.move_red = -1
        self.move_white = 1
        self.red_pos = RED
        self.bla_pos = BLACK
        self.win = win
        self.create_board()

        thread = threading.Thread(target=self.get_pos, args=())
        thread.start()
    
    def draw_squares(self, win):
        win.fill(self.bla_pos)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, self.red_pos, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col, piece.row, piece.col)
        string = str(piece.row)+' ' + str(piece.col)+' ' + str(piece.x)+' ' + str(piece.y)+' ' + str(piece.color)+' ' + str(piece.atx)+' ' + str(piece.aty) + '' + str(piece.rem)
        self.n.send(piece)
        print(sys.getsizeof(piece))
        
        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):

        upper_color = WHITE
        below_color = RED
        alpha = 1
        if self.n.get_status() == "reflict":
            upper_color = RED
            below_color = WHITE
            alpha = 0
            self.move_white = -1
            self.red_pos = BLACK
            self.bla_pos = RED

            self.move_red = 1


        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  alpha) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, upper_color))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, below_color))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
       
    
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            p = self.board[piece.row][piece.col]
            p.set_rem()
            p.atx = piece.row
            p.aty = piece.col
            self.n.send(p)
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row+self.move_red, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row +self.move_red, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +self.move_white, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +self.move_white, min(row+3, ROWS), 1, piece.color, right))
        print(moves)

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)

                    moves.update(self._traverse_left(r+self.move_white, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+self.move_white, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+self.move_red, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+self.move_red, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves