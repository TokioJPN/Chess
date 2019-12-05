# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:41:24 2019

@author: TokioJPN
"""
import pyglet
from pyglet.window import key, mouse
from pyglet.gl import *
from pyglet import image
import pprint

# barvy: 'b' black, 'w' white
# status: 'r' untouched 'n' touched

class Pawn:
    def __init__(self, color, image, zoom, number):
        self.color = color
        self.number = number
        self.reset()
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = zoom
        self.sprite.position = (0,0)
    
    def reset(self):
        self.taken = False
        self.row = 2 if self.color == 'w' else 7
        self.col = self.number
        self.state = 'r'
        
    def take(self):
        self.taken = True
        self.row = 1
        self.col = -2 if self.color == 'w' else -6
        
    # return True if move is valid
    def move(self, row, col, board_matrix):
        if row == self.row and col == self.col:
            return None
        target = board_matrix[row-1][col-1]
        if self.color == 'w':
            if self.state == 'r' and row-self.row == 2 and col == self.col:
                target_skip = board_matrix[row-1-1][col-1]
                if target_skip is not None:
                    return False # nelze preskakovat
                if target is None:
                    self.state = 'n'
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            elif ((row-self.row) == 1) and (col == self.col):
                if target is None:
                    self.state = 'n'
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            elif target is not None and ((row-self.row) == 1) and (abs(col-self.col) == 1) and (target.color != self.color):
                target.take()
                self.row = row
                self.col = col
                self.state = 'n'
                return True
            else:
                return False
        elif self.color == 'b':
            if self.state =='r' and row-self.row == -2 and (col == self.col):
                target_skip = board_matrix[row-1][col-1]
                if target_skip is not None:
                    return False
                if target is None:
                    self.state = 'n'
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            elif ((row-self.row) == -1) and (col == self.col):
                if target is None:
                    self.state = 'n'
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            elif target is not None and ((row-self.row) == -1) and (abs(col-self.col) == 1) and (target.color != self.color):
                target.take()
                self.state = 'n'
                self.row = row
                self.col = col
                return True
        else:
            return False
            # TADY BY SE RESIL I SACH
        return False

    def update(self, square_side):
        self.sprite.position = ((self.col-1)*square_side, (self.row-1)*square_side)


class Rook:
    def __init__(self, color, image, zoom, number):
        self.color = color
        self.number = number
        self.reset()
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = zoom
        self.sprite.position = (0,0)
        
    def reset(self):
        self.taken = False
        self.row = 1 if self.color == 'w' else 8
        self.col = 1 if self.number == 1 else 8
        
    def take(self):
        self.taken = True
        self.row = 2
        self.col = -2 if self.color == 'w' else -6
        
        # return True if move is valid
    def move(self, row, col, board_matrix):
        if row == self.row and col == self.col:
            return None
        
        if row != self.row and col != self.col:
            return False
        
        target = board_matrix[row-1][col-1]
        
        # doleva
        for c in range(self.col-1, 0, -1):
            p = board_matrix[self.row-1][c-1]
            if self.row == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        # doprava
        for c in range(self.col+1, 9, 1):
            p = board_matrix[self.row-1][c-1]
            if self.row == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        # dolu
        for r in range(self.row-1, 0, -1):
            p = board_matrix[r-1][self.col-1]
            if r == row and self.col == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        # nahoru
        for r in range(self.row+1, 9, 1):
            p = board_matrix[r-1][self.col-1]
            if r == row and self.col == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        
        return False

    def update(self, square_side):
        self.sprite.position = ((self.col-1)*square_side, (self.row-1)*square_side)

        
class Knight:
    def __init__(self, color, image, zoom, number):
        self.color = color
        self.number = number
        self.reset()
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = zoom
        self.sprite.position = (0,0)
        
    def reset(self):
        self.taken = False
        self.row = 1 if self.color == 'w' else 8
        self.col = 2 if self.number == 1 else 7
        
    def take(self):
        self.taken = True
        self.row = 3
        self.col = -2 if self.color == 'w' else -6
        
# return True if move is valid
    def move(self, row, col, board_matrix):
        if row == self.row and col == self.col:
            return None
        if ((abs(row-self.row) <= 3 and (abs(col-self.col) == 1))
        or (abs(col-self.col) <= 3 and (abs(row-self.row) == 1))):
            target = board_matrix[row-1][col-1]  # pozor na posun indexu
            
            if target is None:
                self.row = row
                self.col = col
                return True
            elif target.color != self.color:
                target.take()
                self.row = row
                self.col = col
                return True
            else:
                return False
        else:
            return False

    def update(self, square_side):
        self.sprite.position = ((self.col-1)*square_side, (self.row-1)*square_side)


class Bishop:
    def __init__(self, color, image, zoom, number):
        self.color = color
        self.number = number
        self.reset()
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = zoom
        self.sprite.position = (0,0)
        
    def reset(self):
        self.taken = False
        self.row = 1 if self.color == 'w' else 8
        self.col = 3 if self.number == 1 else 6
        
    def take(self):
        self.taken = True
        self.row = 4
        self.col = -2 if self.color == 'w' else -6
        
    # return True if move is valid
    def move(self, row, col, board_matrix):
        if row == self.row and col == self.col:
            return None
        target = board_matrix[row-1][col-1]
        for r, c in zip(range(self.row+1, 9, 1), range(self.col+1, 9, 1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        for r, c in zip(range(self.row+1, 9, 1), range(self.col-1, 0, -1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        for r, c in zip(range(self.row-1, 0, -1), range(self.col+1, 9, 1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        for r, c in zip(range(self.row-1, 0, -1), range(self.col-1, 0, -1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        
        return False

    def update(self, square_side):
        self.sprite.position = ((self.col-1)*square_side, (self.row-1)*square_side)

        
class Queen:
    def __init__(self, color, image, zoom):
        self.color = color
        self.reset()
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = zoom
        self.sprite.position = (0,0)
        
    def reset(self):
        self.taken = False
        self.row = 1 if self.color == 'w' else 8
        self.col = 4
        
    def take(self):
        self.taken = True
        self.row = 5
        self.col = -2 if self.color == 'w' else -6
        
    # return True if move is valid
    def move(self, row, col, board_matrix):
        if row == self.row and col == self.col:
            return None
        
        target = board_matrix[row-1][col-1]
        
        # doleva
        for c in range(self.col-1, 0, -1):
            p = board_matrix[self.row-1][c-1]
            if self.row == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        # doprava
        for c in range(self.col+1, 9, 1):
            p = board_matrix[self.row-1][c-1]
            if self.row == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        # dolu
        for r in range(self.row-1, 0, -1):
            p = board_matrix[r-1][self.col-1]
            if r == row and self.col == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        # nahoru
        for r in range(self.row+1, 9, 1):
            p = board_matrix[r-1][self.col-1]
            if r == row and self.col == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
            
        for r, c in zip(range(self.row+1, 9, 1), range(self.col+1, 9, 1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        for r, c in zip(range(self.row+1, 9, 1), range(self.col-1, 0, -1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take();
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        for r, c in zip(range(self.row-1, 0, -1), range(self.col+1, 9, 1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take()
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break

        for r, c in zip(range(self.row-1, 0, -1), range(self.col-1, 0, -1)):
            p = board_matrix[r-1][c-1]
            if r == row and c == col:
                if target is None:
                    self.row = row
                    self.col = col
                    return True
                elif target.color != self.color:
                    target.take()
                    self.row = row
                    self.col = col
                    return True
                else:
                    return False
            if p is not None:
                break
        return False

    def update(self, square_side):
        self.sprite.position = ((self.col-1)*square_side, (self.row-1)*square_side)
        

class King:
    def __init__(self, color, image, zoom):
        self.color = color
        self.reset()
        self.sprite = pyglet.sprite.Sprite(image)
        self.sprite.scale = zoom
        self.sprite.position = (0,0)
        
    def reset(self):
        self.taken = False
        self.row = 1 if self.color == 'w' else 8
        self.col = 5
    
    def take(self):
        self.taken = True
        self.row = 6 
        self.col = -2 if self.color == 'w' else -6
    
    # return True if move is valid
    def move(self, row, col, board_matrix):
        if row == self.row and col == self.col:
            return None
        if abs(row-self.row) <= 1 and abs(col-self.col) <= 1:
            target = board_matrix[row-1][col-1]  # pozor na posun indexu
            if target is None:
                self.row = row
                self.col = col
                return True
            elif target.color != self.color:
                target.take()
                return True
            else:
                return False
            # TADY BY SE RESIL I SACH
        else:
            return False
    
    def update(self, square_side):
        self.sprite.position = ((self.col-1)*square_side, (self.row-1)*square_side)

class ChessGame:
    def __init__(self):
        # graphics
        self.chess_png = pyglet.resource.image("data/Pieces.png")
        self.board_png = pyglet.resource.image("data/cboard.png")

        sprite_w = self.chess_png.width // 6
        sprite_h = self.chess_png.height // 2
        
        board_w = self.board_png.width
        board_h = self.board_png.height
        
        # pyglet objects
        self.main_window = pyglet.window.Window(int(0.65*board_w), int(0.65*board_h))

        self.main_window.push_handlers(self.on_draw,
                                       self.on_show,
                                       self.on_mouse_press)

        self.images = {
            'w_king': self.chess_png.get_region(0, 1*sprite_h, sprite_w, sprite_h),
            'w_queen': self.chess_png.get_region(sprite_w, sprite_h, sprite_w, sprite_h),
            'w_bishop': self.chess_png.get_region(2*sprite_w, sprite_h, sprite_w, sprite_h),
            'w_knight': self.chess_png.get_region(3*sprite_w, sprite_h, sprite_w, sprite_h),
            'w_rook': self.chess_png.get_region(4*sprite_w, sprite_h, sprite_w, sprite_h),
            'w_pawn': self.chess_png.get_region(5*sprite_w, sprite_h, sprite_w, sprite_h),
            'b_king': self.chess_png.get_region(0, 0, sprite_w, sprite_h),
            'b_queen': self.chess_png.get_region(sprite_w, 0, sprite_w, sprite_h),
            'b_bishop': self.chess_png.get_region(2*sprite_w, 0, sprite_w, sprite_h),
            'b_knight': self.chess_png.get_region(3*sprite_w, 0, sprite_w, sprite_h),
            'b_rook': self.chess_png.get_region(4*sprite_w, 0, sprite_w, sprite_h),
            'b_pawn': self.chess_png.get_region(5*sprite_w, 0, sprite_w, sprite_h),
            'board':self.board_png,
        }
        
        self.board_zoom = 0.65
        self.columns = 8
        self.rows = 8
        self.sprite_w = sprite_w
        self.sprite_h = sprite_h
        self.board_square_side = self.board_png.width/8
        sprite = pyglet.sprite.Sprite(self.images['board'])
        sprite.scale = self.board_zoom
        sprite.position = (0, 0)
        self.board_sprite = sprite
        
        self.pieces_zoom = (self.board_square_side/self.sprite_w)*self.board_zoom
        self.pieces = [King('w', self.images['w_king'], self.pieces_zoom), 
                       King('b', self.images['b_king'], self.pieces_zoom),
                       Queen('w', self.images['w_queen'], self.pieces_zoom),
                       Queen('b', self.images['b_queen'], self.pieces_zoom),
                       Bishop('w', self.images['w_bishop'], self.pieces_zoom, 1),
                       Bishop('w', self.images['w_bishop'], self.pieces_zoom, 2),
                       Bishop('b', self.images['b_bishop'], self.pieces_zoom, 1),
                       Bishop('b', self.images['b_bishop'], self.pieces_zoom, 2),
                       Knight('w', self.images['w_knight'], self.pieces_zoom, 1),
                       Knight('w', self.images['w_knight'], self.pieces_zoom, 2),
                       Knight('b', self.images['b_knight'], self.pieces_zoom, 1),
                       Knight('b', self.images['b_knight'], self.pieces_zoom, 2),
                       Rook('w', self.images['w_rook'], self.pieces_zoom, 1),
                       Rook('w', self.images['w_rook'], self.pieces_zoom, 2),
                       Rook('b', self.images['b_rook'], self.pieces_zoom, 1),
                       Rook('b', self.images['b_rook'], self.pieces_zoom, 2),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 1),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 2),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 3),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 4),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 5),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 6),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 7),
                       Pawn('w', self.images['w_pawn'], self.pieces_zoom, 8),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 1),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 2),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 3),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 4),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 5),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 6),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 7),
                       Pawn('b', self.images['b_pawn'], self.pieces_zoom, 8),]
        
        for piece in self.pieces:
            piece.update(self.board_square_side*self.board_zoom)

        self.make_board_matrix()
        
        self.active_player = 'w' # prvni hraje bily
        self.player_state = 'select'  # vybira figuru, po oznaceni stav 'move'

    def make_board_matrix(self):
        self.board_matrix = []
        for row in range(8):
            R = []
            for col in range(8):
                R.append(None)
            self.board_matrix.append(R)
        
        for piece in self.pieces:
            if not piece.taken:
                self.board_matrix[piece.row-1][piece.col-1] = piece
                

    def on_show(self):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def on_draw(self):
        self.main_window.clear()  # vymazani okna
        # draw background
        self.board_sprite.draw()
        
        for piece in self.pieces:
            if not piece.taken: 
                piece.sprite.draw()

    def on_mouse_press(self, x, y, b, mod):
        if b == mouse.LEFT:
            print('leva myska na pozici:', x, y)
            col = int(x // (self.board_square_side * self.board_zoom))
            row = int(y // (self.board_square_side * self.board_zoom))
            chess_col = col + 1
            chess_row = row + 1
#            print('chess_col', chess_col, ', chess_row', chess_row);
            print('BEGIN:  player_state', self.player_state, ' , active_player', self.active_player )
            if self.player_state == 'select':
                target = self.board_matrix[row][col]
                if target is not None and target.color == self.active_player:
                    self.selected_piece = target
                    self.player_state = 'move'
                    
            elif self.player_state == 'move':
                result = self.selected_piece.move(chess_row, chess_col, self.board_matrix)
                if result is None:
                    self.player_state = 'select'
                elif result:
                    self.make_board_matrix()
                    for piece in self.pieces:
                        piece.update(self.board_square_side*self.board_zoom)
                    self.player_state = 'select'
                    self.active_player = 'w' if self.active_player == 'b' else 'b'
            
            print('END:  player_state', self.player_state, ' , active_player', self.active_player )


            
game_state = ChessGame()

pyglet.app.run()