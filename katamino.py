import numpy as np
import random
import time

import puzzle

# Initialize list of pieces and colors
pieces_list, colors = puzzle.get_piece_list()

# Game definition
slam_id = int(input("Which small slam would you like me to try? (1-7) "))
columns = int(input("How many pieces are we playing with? (3-8) "))
pieces = []
challenge = puzzle.get_challenge(slam_id, columns)

# Info message && setup pieces array
print("Playing small slam ", slam_id, ", pieces:", challenge)
for i in range(columns):
    piece_id = challenge[i]
    pieces.append(piece_id * pieces_list[piece_id-1])

# Display pieces nicely
print("Playing with these pieces:")
puzzle.print_pieces(challenge, pieces, colors)

# Variables to control how many positioning attempts are tried per piece
rotation_tries_per_piece = 30
translation_tries_per_piece = columns * 10

# Init variables for solving loop
solved = False
run = 0
puzzle_start_time = time.time()
epoch_start_time = time.time()
runs_last_piece = []

# Solving loop
print("Trying to solve puzzle...")
while not solved:
    # Display some info every 1000 runs (epoch)
    if run % 1000 == 0 and run != 0:
        print (run, "runs, average exec time per run", round((time.time()-epoch_start_time)/1000,3), "seconds")
        # EPOCH information:
        # for i in range(columns):
        #     print (" * Runs that have placed", i+1, "pieces:", sum(1 for x in runs_last_piece if x >= i))
        epoch_start_time = time.time()
    # Init variables per run 
    piece_placed = True
    last_piece_placed = -1
    board = np.zeros((5, columns), dtype=np.int8)
    # Shuffle piece order for each run
    random.shuffle(pieces)
    # Piece loop
    for i in range(columns):
        piece = pieces[i]
        # If previous piece was correctly placed try to position this one. Otherwise give up straight away
        if piece_placed:
            # Init variables per piece rotation
            piece_placed = False
            this_piece_rotation_try = 0
            while not (piece_placed or this_piece_rotation_try > rotation_tries_per_piece):
                # Random mirror, rotate and offset the piece, and put it in an array the same size as the board
                random_piece = puzzle.randomize_piece(piece)
                # Verify piece fits in board, otherwise try another rotation (this is only important for small boards)
                if random_piece.shape[0] <= board.shape[0] and random_piece.shape[1] <= board.shape[1]:
                    # Calculate possible maximum offset
                    pad_hor = board.shape[0]-random_piece.shape[0]
                    pad_ver = board.shape[1]-random_piece.shape[1]
                    # Translation loop
                    this_piece_translation_try = 0
                    while not (piece_placed or this_piece_translation_try > translation_tries_per_piece):
                        # Try to place the rotated piece randomly across the board
                        offset_hor = random.randint(0, pad_hor)
                        offset_ver = random.randint(0, pad_ver)
                        padded_piece = np.pad(random_piece, ((offset_hor, pad_hor-offset_hor), (offset_ver, pad_ver-offset_ver)), mode='constant', constant_values = 0)
                        # If there is overlap between the offset piece and the rest of pieces on the dashboard, try another translation
                        overlap = np.sum(np.logical_and(board, padded_piece))
                        if overlap == 0:    # No overlap, verify that by placing the piece here we are not creating an island of zeros not multiple of 5
                            # Before placing the piece, check whether there is an island of zeros not multiple of 5
                            # If so, do not place the piece here, keep on trying
                            zero_island_size = puzzle.smallestZeroRegion(board + padded_piece)
                            if zero_island_size % 5 == 0:
                                board = board + padded_piece  # Place piece on the board
                                last_piece_placed = i         # Update variable to track the last piece placed in each run
                                piece_placed = True           # Mark this piece as placed
                            # else:   ### DEBUG ###
                            #     print("Zero-island of size not multiple of 5 detected! ->", zero_island_size)
                            #     print(board + padded_piece)
                            #     input("Please press ENTER to continue...")
                        # Next translation
                        this_piece_translation_try += 1
                # Next rotation
                this_piece_rotation_try += 1
    # If the rotation or translation limit was reached for a piece, piece_placed should be false. Otherwise, it means we have placed all the pieces
    if piece_placed:
        solved = True
    else:
        runs_last_piece.append(last_piece_placed)
    ### DEBUG ###
    # puzzle.print_board(board, colors)
    # print("Smallest zero region:", smallestZeroRegion(board))
    # input("Please press ENTER to continue...")

    # Next run
    run += 1

if solved:
    print("Puzzle solved with", run, "tries in", round((time.time()-puzzle_start_time)), "seconds")
    puzzle.print_board(board, colors)
else:
    print("Mmmh, I could not solve the puzzle :-(")   # Actually we are never going to reach this