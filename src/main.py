import pygame
import sys
from const import *
from game import Game
from square import Square
from move import Move
from chessengine import ChessEngine

class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.engine = ChessEngine(depth=3)
        self.dragger = self.game.dragger

    def mainloop(self):
        game = self.game
        screen = self.screen
        dragger = self.game.dragger
        board = self.game.board
        engine = self.engine
        play_with_ai = False
        clock = pygame.time.Clock()
        while True:
            #show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for events in pygame.event.get():
                #clicks
                if events.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(events.pos)

                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece (color)?
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col, bool=True)
                            dragger.save_inital(events.pos)
                            dragger.drag_piece(piece)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                
                #mouse motion
                elif events.type == pygame.MOUSEMOTION:
                    motion_row = events.pos[1] // SQSIZE
                    motion_col = events.pos[0] // SQSIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(events.pos)
                        #show methods
                        game.show_bg(screen) #can remove if you want to show trail
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen) #can remove if you want to show trail
                        game.show_hover(screen)
                        dragger.update_blit(screen)
                
                #click release
                elif events.type == pygame.MOUSEBUTTONUP:

                    if dragger.dragging:
                        dragger.update_mouse(events.pos)

                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        #create move
                        inital = Square(dragger.inital_row, dragger.inital_col)
                        final = Square(released_row, released_col)
                        move = Move(inital, final)

                        if board.valid_move(dragger.piece, move):
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)

                            board.set_true_en_passant(dragger.piece)
                            #sounds
                            game.sound_effect(captured)
                            #show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                            if play_with_ai and game.next_player == ai_color:
                                piece, ai_move = engine.get_best_move(game.board, ai_color)
                                if ai_move:
                                    move = Move(ai_move.inital, ai_move.final)
                                    game.board.move(piece, move)
                                    game.next_turn()
                    dragger.undrag_piece()

                #key press
                elif events.type == pygame.KEYDOWN:
                    if events.key == pygame.K_a:
                        play_with_ai = True
                        ai_color = 'black'  # AI will play as black
                        game.reset()  # Reset the game when AI starts
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board
                    #changing themes
                    if events.key == pygame.K_t:
                        game.change_theme()

                    #changing themes
                    if events.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        dragger = self.game.dragger
                        board = self.game.board
                        
                #quit application
                elif events.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.mainloop()
