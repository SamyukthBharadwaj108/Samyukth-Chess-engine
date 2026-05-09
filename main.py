import chess
import tkinter as tk
from tkinter import messagebox
from stockfish import Stockfish

# =========================================================
# STOCKFISH ENGINE
# =========================================================

stockfish = Stockfish("/opt/homebrew/bin/stockfish")

# Default difficulty
stockfish.set_skill_level(10)

# =========================================================
# CHESS BOARD
# =========================================================

board = chess.Board()

selected_square = None
possible_moves = []

# =========================================================
# PIECE SYMBOLS
# =========================================================

piece_symbols = {
    'P': '♙',
    'N': '♘',
    'B': '♗',
    'R': '♖',
    'Q': '♕',
    'K': '♔',

    'p': '♟',
    'n': '♞',
    'b': '♝',
    'r': '♜',
    'q': '♛',
    'k': '♚'
}

# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()
root.title("♟️ Samyukth Chess Engine")
root.configure(bg="#0F172A")

buttons = []

main_frame = tk.Frame(root, bg="#0F172A")
main_frame.pack(side=tk.LEFT, padx=20, pady=20)

side_frame = tk.Frame(root, bg="#0F172A")
side_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

# =========================================================
# EVALUATION BAR
# =========================================================

eval_label = tk.Label(
    side_frame,
    text="Evaluation: 0.0",
    font=("Arial", 14, "bold"),
    bg="#0F172A",
    fg="white"
)

eval_label.pack(pady=10)

# =========================================================
# MOVE HISTORY
# =========================================================

history_title = tk.Label(
    side_frame,
    text="Move History",
    font=("Arial", 14, "bold"),
    bg="#0F172A",
    fg="white"
)

history_title.pack()

history_box = tk.Text(
    side_frame,
    height=18,
    width=25,
    bg="#1E293B",
    fg="white",
    insertbackground="white",
    font=("Consolas", 10)
)

history_box.pack(pady=10)

# =========================================================
# ENGINE COMMENTARY
# =========================================================

commentary_title = tk.Label(
    side_frame,
    text="Engine Commentary",
    font=("Arial", 14, "bold"),
    bg="#0F172A",
    fg="white"
)

commentary_title.pack(pady=10)

commentary_box = tk.Label(
    side_frame,
    text="😈 Ready to dominate.",
    wraplength=240,
    justify="left",
    font=("Arial", 11),
    bg="#0F172A",
    fg="white"
)

commentary_box.pack()

# =========================================================
# DIFFICULTY SYSTEM
# =========================================================

difficulty_levels = {
    "Beginner": 1,
    "Intermediate": 5,
    "Advanced": 10,
    "Master": 15,
    "Stockfish Nightmare": 20
}

def set_difficulty(label):

    skill = difficulty_levels[label]

    stockfish.set_skill_level(skill)

    difficulty_label.config(
        text=f"Current Difficulty: {label}"
    )

difficulty_label = tk.Label(
    side_frame,
    text="Current Difficulty: Advanced",
    font=("Arial", 12, "bold"),
    bg="#0F172A",
    fg="white"
)

difficulty_label.pack(pady=12)

# =========================================================
# DIFFICULTY BUTTONS
# =========================================================

for label in difficulty_levels:

    btn = tk.Button(
        side_frame,
        text=label,
        command=lambda l=label: set_difficulty(l),

        font=("Arial", 12, "bold"),

        bg="#2563EB",
        fg="#FFFFFF",

        activebackground="#1D4ED8",
        activeforeground="#FFFFFF",

        width=22,
        height=2,

        relief=tk.RAISED,
        borderwidth=3
    )

    btn.pack(pady=5)

# =========================================================
# COMMENTARY GENERATOR
# =========================================================

def generate_comment(score):

    if score == "Mate":
        return "💀 Forced mate detected. Absolute destruction."

    if score > 5:
        return "😈 Completely winning. This is brutal."

    elif score > 2:
        return "🔥 Strong pressure building."

    elif score > 0.5:
        return "🙂 Slight edge for the engine."

    elif score > -0.5:
        return "😌 Balanced position... for now."

    elif score > -2:
        return "👀 Careful. Things are getting dangerous."

    else:
        return "💀 Yeah... this position is collapsing."

# =========================================================
# UPDATE EVALUATION
# =========================================================

def update_evaluation():

    stockfish.set_fen_position(board.fen())

    try:

        evaluation = stockfish.get_evaluation()

        if evaluation["type"] == "cp":
            score = round(evaluation["value"] / 100, 2)

        else:
            score = "Mate"

    except:
        score = 0

    eval_label.config(
        text=f"Evaluation: {score}"
    )

    commentary_box.config(
        text=generate_comment(score)
    )

# =========================================================
# UPDATE MOVE HISTORY
# =========================================================

def update_history():

    history_box.delete(1.0, tk.END)

    moves = [move.uci() for move in board.move_stack]

    for i in range(0, len(moves), 2):

        white_move = moves[i]

        black_move = (
            moves[i + 1]
            if i + 1 < len(moves)
            else ""
        )

        history_box.insert(
            tk.END,
            f"{i//2 + 1}. {white_move} {black_move}\n"
        )

# =========================================================
# DRAW BOARD
# =========================================================

def draw_board():

    for i in range(64):

        row = 7 - (i // 8)
        col = i % 8

        piece = board.piece_at(i)

        text = (
            piece_symbols.get(piece.symbol(), '')
            if piece
            else ''
        )

        # =================================================
        # OLIVE GREEN + WHITE BOARD
        # =================================================

        if (row + col) % 2 == 0:
            color = "#EEEED2"
        else:
            color = "#769656"

        # =================================================
        # SELECTED TILE
        # =================================================

        if i == selected_square:
            color = "#F6F669"

        # =================================================
        # LEGAL MOVES
        # =================================================

        if i in possible_moves:
            color = "#BACA44"

        buttons[i].config(
            text=text,
            bg=color,
            activebackground=color,
            font=("Segoe UI Symbol", 32, "bold"),
            fg="#000000",
            width=3,
            height=1,
            relief=tk.RAISED,
            borderwidth=1
        )

    update_evaluation()
    update_history()

# =========================================================
# ENGINE MOVE
# =========================================================

def make_engine_move():

    if board.is_game_over():
        return

    stockfish.set_fen_position(board.fen())

    best_move = stockfish.get_best_move()

    if best_move:

        move = chess.Move.from_uci(best_move)

        board.push(move)

        draw_board()

# =========================================================
# CLICK HANDLER
# =========================================================

def on_click(i):

    global selected_square
    global possible_moves

    if board.is_game_over():

        messagebox.showinfo(
            "Game Over",
            f"Result: {board.result()}"
        )

        return

    # =====================================================
    # FIRST CLICK
    # =====================================================

    if selected_square is None:

        piece = board.piece_at(i)

        if piece and piece.color == board.turn:

            selected_square = i

            possible_moves = [

                move.to_square

                for move in board.legal_moves

                if move.from_square == i
            ]

        draw_board()

        return

    # =====================================================
    # SECOND CLICK
    # =====================================================

    move = chess.Move(selected_square, i)

    if move in board.legal_moves:

        board.push(move)

        selected_square = None
        possible_moves = []

        draw_board()

        root.update()

        # ENGINE RESPONSE
        make_engine_move()

    else:

        selected_square = None
        possible_moves = []

        draw_board()

    # =====================================================
    # GAME OVER
    # =====================================================

    if board.is_game_over():

        messagebox.showinfo(
            "Game Over",
            f"Result: {board.result()}"
        )

# =========================================================
# RESET GAME
# =========================================================

def reset_game():

    global board
    global selected_square
    global possible_moves

    board = chess.Board()

    selected_square = None
    possible_moves = []

    draw_board()

# =========================================================
# RESET BUTTON
# =========================================================

reset_button = tk.Button(
    side_frame,
    text="♻️ New Game",
    command=reset_game,

    font=("Arial", 12, "bold"),

    bg="#DC2626",
    fg="#FFFFFF",

    activebackground="#B91C1C",
    activeforeground="#FFFFFF",

    width=22,
    height=2,

    relief=tk.RAISED,
    borderwidth=3
)

reset_button.pack(pady=12)

# =========================================================
# CREATE BOARD BUTTONS
# =========================================================

for i in range(64):

    button = tk.Button(
        main_frame,
        command=lambda i=i: on_click(i)
    )

    button.grid(
        row=7 - (i // 8),
        column=i % 8
    )

    buttons.append(button)

# =========================================================
# START PROGRAM
# =========================================================

draw_board()

root.mainloop()