AI = 'X'
HUMAN = 'O'
EMPTY = ' '
def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)
def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions
def is_board_full(board):
    return all(cell != EMPTY for row in board for cell in row)
def minimax(board, depth, is_maximizing):
    if check_winner(board, AI):
        return 1
    if check_winner(board, HUMAN):
        return -1
    if is_board_full(board):
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    score = minimax(board, depth + 1, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = HUMAN
                    score = minimax(board, depth + 1, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score
def find_best_move(board):
    best_move = None
    best_score = -float('inf')
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                score = minimax(board, 0, False)
                board[i][j] = EMPTY
                
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    return best_move
def play_game():
    board = [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]
    human_turn = True

    while True:
        print_board(board)

        if check_winner(board, AI):
            print("AI wins!")
            break
        if check_winner(board, HUMAN):
            print("You win!")
            break
        if is_board_full(board):
            print("It's a draw!")
            break
        if human_turn:
            print("Your move! Enter row and column (0, 1, or 2):")
            row, col = map(int, input().split())
            if board[row][col] == EMPTY:
                board[row][col] = HUMAN
                human_turn = False
            else:
                print("Invalid move, try again.")
        else:
            print("AI is making a move...")
            ai_move = find_best_move(board)
            if ai_move:
                board[ai_move[0]][ai_move[1]] = AI
            human_turn = True
play_game()
