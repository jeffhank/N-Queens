# Author: Jeff Hank
# Date: February 17, 2020
# Class: COMP SCI 540 LEC 001
# Assignment: P3 N-Queens
# Files: nqueens.py

import random


# returns a list of all valid successor states given the state of the board
# state - state of the board
# boulderX - x coordinate of the boulder
# boulderY - y coordinate of the boulder
# returns a list of successor states
def succ(state, boulderX, boulderY):
    size = len(state)
    succList = []
    x = 0
    for item in state:
        for y in range(size):
            newState = state.copy()
            newState[x] = y
            if newState != state:
                if not (x == boulderX and y == boulderY):
                    if newState not in succList:
                        succList.append(newState)
        x += 1
    succList.sort()
    return succList

# returns an integer score for the state of the board which corresponds to the number of queens on the board that are
# being attacked
# state - state of the board
# boulderX - x coordinate of the boulder
# boulderY - y coordinate of the boulder
# returns a score such that the goal state has score zero
def f(state, boulderX, boulderY):
    fscore = 0
    for i, item in enumerate(state):
        attacked = False
        # check row to right
        for j in range(i + 1, len(state)):
            if j == boulderX and item == boulderY:
                break
            if state[j] == item:
                fscore = fscore + 1
                attacked = True
                break
        if not attacked:
            # check row to left
            for j in range(i - 1, -1, -1):
                if j == boulderX and item == boulderY:
                    break
                if state[j] == item:
                    fscore = fscore + 1
                    attacked = True
                    break
        if not attacked:
            # check diagonal upright
            row = item + 1
            for j in range(i + 1, len(state)):
                if row < len(state):
                    if j == boulderX and row == boulderY:
                        break
                    if state[j] == row:
                        fscore = fscore + 1
                        attacked = True
                        break
                    row = row + 1
                else:
                    break
        if not attacked:
            # check diagonal downright
            row = item - 1
            for j in range(i + 1, len(state)):
                if row >= 0:
                    if j == boulderX and row == boulderY:
                        break
                    if state[j] == row:
                        fscore = fscore + 1
                        attacked = True
                        break
                    row = row - 1
                else:
                    break
        if not attacked:
            # check diagonal upleft
            row = item + 1
            for j in range(i - 1, -1, -1):
                if row < len(state):
                    if j == boulderX and row == boulderY:
                        break
                    if state[j] == row:
                        fscore = fscore + 1
                        attacked = True
                        break
                    row = row + 1
                else:
                    break
        if not attacked:
            # check diagonal downleft
            row = item - 1
            for j in range(i - 1, -1, -1):
                if row >= 0:
                    if j == boulderX and row == boulderY:
                        break
                    if state[j] == row:
                        fscore = fscore + 1
                        attacked = True
                        break
                    row = row - 1
                else:
                    break
    return fscore

# geenrates the successors and selects the best one to return
# curr - current state of the board
# boulderX - x coordinate of the boulder
# boulderY - y coordinate of the boulder
# returns the successor state of curr with the lowest f
def choose_next(curr, boulderX, boulderY):
    succList = succ(curr, boulderX, boulderY)
    succList.append(curr)
    lowestf = f(curr, boulderX, boulderY)
    for item in succList:
        if f(item, boulderX, boulderY) < lowestf:
            lowestf = f(item, boulderX, boulderY)
    nextList = []
    for item in succList:
        if f(item, boulderX, boulderY) == lowestf:
            nextList.append(item)
    nextList.sort()
    if nextList[0] == curr:
        return None
    return nextList[0]

# runs the hill climbing algorithm from the given state and returns the convergent state
# initial_state - initial state of the board
# boulderX - x coordinate of the boulder
# boulderY - y coordinate of the boulder
# returns the convergent state and prints the current state for each step in the hill climbing function
def nqueens(initial_state, boulderX, boulderY):
    curr = initial_state.copy()
    foundMin = False
    print(initial_state, " - f=", f(curr, boulderX, boulderY), sep="")
    while not foundMin:
        newState = choose_next(curr, boulderX, boulderY)
        if newState is not None:
            print(newState, " - f=", f(newState, boulderX, boulderY), sep="")
            curr = newState.copy()
        else:
            foundMin = True
    return curr


# randomly generates a board state
# n - the size of the board
# returns the state of the board
def generate_board(n):
    board = []
    for col in range(n):
        row = random.randint(0, n - 1)
        board.append(row)
    return board


# given a state_list, find the minimums and return an ordered list to break any ties
# state_list - list of board states
# boulderX - x coordinate of the boulder
# boulderY - y coordinate of the boulder
# returns a list of minimums
def find_min(state_list, boulderX, boulderY):
    fList = []
    for item in state_list:
        fList.append(f(item, boulderX, boulderY))
    minf = fList[0]
    for item in fList:
        if item < minf:
            minf = item
    nextlist = []
    for i, item in enumerate(state_list):
        if fList[i] == minf:
            nextlist.append(item)
    nextlist.sort()
    return nextlist


# tries k times to find a solution to a randomly generated board
# n - size of the board
# k - tries k times to find a solution
# boulderX - x coordinate of the boulder
# boulderY - y coordinate of the boulder
def nqueens_restart(n, k, boulderX, boulderY):
    solutions = []
    found_solution = False
    for iter in range(k):
        valid_board = False
        while not valid_board:
            state = generate_board(n)
            if not (state[boulderX] == boulderY):
                valid_board = True
        curr_state = nqueens(state, boulderX, boulderY)
        if curr_state not in solutions:
            solutions.append(curr_state)
        if f(curr_state, boulderX, boulderY) == 0:
            found_solution = True
            break
    if found_solution:
        print("SOLUTION:", solutions[len(solutions) - 1])
    else:
        bestlist = find_min(solutions, boulderX, boulderY)
        bestlist.sort(reverse=True)
        print("NO SOLUTION ... Best results:")
        for item in bestlist:
            print(item, " - f=", f(item, boulderX, boulderY), sep="")
