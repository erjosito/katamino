import numpy as np
import random
import time


# Pentamino (aka piece) definitions:
def get_piece_list():
    # blue horizontal bar
    piece_1 = np.zeros((1, 5), dtype=np.int8)
    piece_1[0, 0] = 1
    piece_1[0, 1] = 1
    piece_1[0, 2] = 1
    piece_1[0, 3] = 1
    piece_1[0, 4] = 1
    # Orange "L"
    piece_2 = np.zeros((2, 4), dtype=np.int8)
    piece_2[0, 0] = 1
    piece_2[1, 0] = 1
    piece_2[1, 1] = 1
    piece_2[1, 2] = 1
    piece_2[1, 3] = 1
    # "brown"
    piece_3 = np.zeros((2, 4), dtype=np.int8)
    piece_3[0, 1] = 1
    piece_3[1, 0] = 1
    piece_3[1, 1] = 1
    piece_3[1, 2] = 1
    piece_3[1, 3] = 1
    # Purple "Z"
    piece_4 = np.zeros((2, 4), dtype=np.int8)
    piece_4[0, 0] = 1
    piece_4[0, 1] = 1
    piece_4[0, 2] = 1
    piece_4[1, 2] = 1
    piece_4[1, 3] = 1
    # Blue "corner"
    piece_5 = np.zeros((3, 3), dtype=np.int8)
    piece_5[0, 0] = 1
    piece_5[0, 1] = 1
    piece_5[0, 2] = 1
    piece_5[1, 2] = 1
    piece_5[2, 2] = 1
    # Pink "6"
    piece_6 = np.zeros((2, 3), dtype=np.int8)
    piece_6[0, 1] = 1
    piece_6[0, 2] = 1
    piece_6[1, 0] = 1
    piece_6[1, 1] = 1
    piece_6[1, 2] = 1
    # Yellow "bridge"
    piece_7 = np.zeros((2, 3), dtype=np.int8)
    piece_7[0, 0] = 1
    piece_7[0, 1] = 1
    piece_7[0, 2] = 1
    piece_7[1, 0] = 1
    piece_7[1, 2] = 1
    # Blue "2"
    piece_8 = np.zeros((3, 3), dtype=np.int8)
    piece_8[0, 0] = 1
    piece_8[0, 1] = 1
    piece_8[1, 1] = 1
    piece_8[2, 1] = 1
    piece_8[2, 2] = 1
    # Grey "7"
    piece_9 = np.zeros((3, 3), dtype=np.int8)
    piece_9[0, 1] = 1
    piece_9[1, 0] = 1
    piece_9[1, 1] = 1
    piece_9[2, 1] = 1
    piece_9[2, 2] = 1
    # Green "T"
    piece_10 = np.zeros((3, 3), dtype=np.int8)
    piece_10[0, 0] = 1
    piece_10[0, 1] = 1
    piece_10[0, 2] = 1
    piece_10[1, 1] = 1
    piece_10[2, 1] = 1
    # Green "W"
    piece_11 = np.zeros((3, 3), dtype=np.int8)
    piece_11[0, 2] = 1
    piece_11[1, 1] = 1
    piece_11[1, 2] = 1
    piece_11[2, 0] = 1
    piece_11[2, 1] = 1
    # Red "+"
    piece_12 = np.zeros((3, 3), dtype=np.int8)
    piece_12[0, 1] = 1
    piece_12[1, 0] = 1
    piece_12[1, 1] = 1
    piece_12[1, 2] = 1
    piece_12[2, 1] = 1

    piece_list = [ piece_1, piece_2, piece_3, piece_4, piece_5, piece_6, piece_7, piece_8, piece_9, piece_10, piece_11, piece_12]
    colors = ["\u001b[32m", "\u001b[38;5;208m", "\u001b[38;5;94m", "\u001b[38;5;129m", "\u001b[36m", "\u001b[35;1m", "\u001b[33m", "\u001b[36;1m", "\u001b[30;1m", "\u001b[32m", "\u001b[32;1m", "\u001b[31m"]

    return piece_list, colors

# Return a vector with the pieces of a challenge
def get_challenge(id, columns):
    challenges = []
    challenges.append([ 2,  3, 10,  6, 11,  8,  5,  4])
    challenges.append([ 4,  6,  7,  2,  8,  3, 10, 11])
    challenges.append([ 2,  5,  6, 10,  4,  7,  8,  9])
    challenges.append([ 3,  6,  7,  4,  5,  9, 11, 10])
    challenges.append([ 2,  4,  5,  8,  7, 10,  3, 11])
    challenges.append([ 6,  7,  9,  3, 10,  4,  2, 11])
    challenges.append([ 2,  5,  6,  8,  3, 11,  4,  9])
    return challenges[id-1][:columns]

# Pretty print the pieces in a challenge
# The 1st argument is a list of pieces, the second is the piece reference
def print_pieces(challenge, pieces, colors, hor_stretch_factor=2, stretch_factor=2):
    columns=len(challenge)
    default_color="\033[0m"
    display=np.zeros((5,columns*5), dtype=np.int8)  # matrix to hold pieces for display
    for i in range(columns):
        piece = pieces[i]
        piece = np.pad(piece, ((0,5-piece.shape[0]), (0,5-piece.shape[1])), mode='constant', constant_values = 0) # pad to a 5x5 array
        piece = np.pad(piece,((0,0),(i*5,(columns-i-1)*5)), mode='constant', constant_values = 0) # pad to match the display
        display = display + piece
    # Convert each row to characters, to print nicely
    # see http://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
    for i in range(5):
        line = ""
        for j in range(columns*5):
            if bool(display[i,j]):
                line = line + colors[challenge[(j//5)]-1] + u"\u2588" * stretch_factor * hor_stretch_factor + default_color
            else:
                line+=" " * stretch_factor * hor_stretch_factor
        for numlines in range(stretch_factor):
            print(line)

# Prints the board
def print_board(board, colors, hor_stretch_factor=2, stretch_factor=2):
    columns=np.shape(board)[1]
    default_color="\033[0m"
    for i in range(5):
        line = ""
        for j in range(columns):
            if bool(board[i,j]):
                line = line + colors[board[i,j]-1] + u"\u2588" * hor_stretch_factor * stretch_factor + default_color
            else:
                line += " " * hor_stretch_factor * stretch_factor
        for numlines in range(stretch_factor):
            print(line)

# Function to randomly flip and/or rotate a piece
def randomize_piece(piece):
    # Flip horizontally (or not)
    if bool(random.getrandbits(1)):
        piece = np.fliplr(piece)
    # Flip vertically (or not)
    if bool(random.getrandbits(1)):
        piece = np.flipud(piece)
    # Rotate 0/90/180/270
    piece = np.rot90(piece, random.randint(0,3))
    # end
    return piece

# A function to check if a given cell (row, col) can be included in DFS  
# See https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/ for DFS
def isSafe(M, row, col, visited): 
    # row number is in range, column number is in range and value is 0 and not yet visited  
    return ((row >= 0) and (row < M.shape[0]) and
            (col >= 0) and (col < M.shape[1]) and 
            not bool(M[row][col]) and
            not visited[row][col])

# A utility function to do DFS for a 2D boolean matrix. It only considers the 4 neighbours as adjacent vertices  
# See https://www.geeksforgeeks.org/depth-first-search-or-dfs-for-a-graph/ for DFS
def DFS(M, row, col, visited, count): 
    # These arrays are used to get row and column numbers of 4 neighbours of a given cell  
    rowNbr = [ 1, -1,  0,  0]  
    colNbr = [ 0,  0,  1, -1]  
    # Mark this cell as visited  
    visited[row][col] = True
    # Recur for all connected neighbours  
    for k in range(4): 
        if (isSafe(M, row + rowNbr[k], col + colNbr[k], visited)): 
            # increment region length by one  
            count[0] += 1
            DFS(M, row + rowNbr[k],  
                col + colNbr[k], visited, count) 

# The main function that returns largest length region of a given boolean 2D matrix  
def smallestZeroRegion(M): 
    # Make a bool array to mark visited cells. Initially all cells are unvisited  
    visited = np.zeros((M.shape[0], M.shape[1]), dtype=np.int8)
    # Initialize result as a large number and travese through the all cells of given matrix  
    init_value = 999999
    result = init_value
    for i in range(M.shape[0]): 
        for j in range(M.shape[1]): 
            # If a cell with value 0 (False) is not  
            if (not bool(M[i][j]) and not visited[i][j]): 
                # visited yet, then new region found, the current size would be 1
                count = [1]     # Defined as list to be passed as reference
                DFS(M, i, j, visited, count)  
                # smallest region  
                result = min(result, count[0]) 
    if result == init_value:
        return 0       # No island was found
    else:
        return result  # Size of the smallest island
