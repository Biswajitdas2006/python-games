import pygame
import chess

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 760, 760
SQUARE_SIZE = WIDTH // 8

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIGHLIGHT_COLOR = (200, 200, 0)

# Load piece images
PIECES = {
    'P': pygame.image.load('images/wp.png'),
    'R': pygame.image.load('images/wr.png'),
    'N': pygame.image.load('images/wn.png'),
    'B': pygame.image.load('images/wb.png'),
    'Q': pygame.image.load('images/wq.png'),
    'K': pygame.image.load('images/wk.png'),
    'p': pygame.image.load('images/bp.png'),
    'r': pygame.image.load('images/br.png'),
    'n': pygame.image.load('images/bn.png'),
    'b': pygame.image.load('images/bb.png'),
    'q': pygame.image.load('images/bq.png'),
    'k': pygame.image.load('images/bk.png'),
}

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess')

# Initialize chess board using python-chess
board = chess.Board()

# Stacks to handle undo and redo moves
undo_stack = []
redo_stack = []

def draw_board(screen):
    """Draw the chessboard."""
    colors = [WHITE, BLACK]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board):
    """Draw pieces on the chessboard."""
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_image = PIECES[piece.symbol()]
                screen.blit(piece_image, (col*SQUARE_SIZE, row*SQUARE_SIZE))

def highlight_square(screen, row, col):
    """Highlight a square on the chessboard."""
    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def get_square_under_mouse():
    """Get the chessboard square under the mouse."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    col = mouse_x // SQUARE_SIZE
    row = mouse_y // SQUARE_SIZE
    return (7 - row) * 8 + col  # Convert screen coords to chess square

def undo_move():
    """Undo the last move and push it to the redo stack."""
    if len(board.move_stack) > 0:
        move = board.pop()
        undo_stack.append(move)
        return True
    return False

def redo_move():
    """Redo the last undone move."""
    if len(undo_stack) > 0:
        move = undo_stack.pop()
        board.push(move)
        return True
    return False

def main():
    clock = pygame.time.Clock()
    running = True
    selected_square = None
    move_made = False

    while running:
        draw_board(screen)
        draw_pieces(screen, board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                square = get_square_under_mouse()
                piece = board.piece_at(square)

                if selected_square is None:
                    if piece and (piece.color == (board.turn == chess.WHITE)):  # Select the piece
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in board.legal_moves:
                        board.push(move)
                        move_made = True
                    selected_square = None

            # Handle undo and redo keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:  # Undo move
                    if undo_move():
                        print("Undo successful")

                if event.key == pygame.K_r:  # Redo move
                    if redo_move():
                        print("Redo successful")

        # Highlight the selected square
        if selected_square is not None:
            row, col = divmod(selected_square, 8)
            highlight_square(screen, 7 - row, col)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
