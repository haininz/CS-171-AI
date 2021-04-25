from random import randint
from BoardClasses import Move
from BoardClasses import Board
import copy
import math
import random
import time
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class node:
    def __init__(self, parent, state, round):
        self.round_played = 0
        self.win = 0
        self.parent = parent
        self.children = []
        self.state = copy.deepcopy(state)
        self.round = round

def UCB(node):
    f = node.win / node.round_played
    s = math.sqrt(2) * math.sqrt((math.log(node.parent.round_played))/node.round_played)
    return f + s

def opponent_turn(num):
    opponent = {1:2,2:1}
    return opponent[num]

def get_color(num):
    color = {1:'B', 2:'W'}
    return color[num]

def get_raw_move(state, round):
    temp_list = state.get_all_possible_moves(round)
    possible_move = []
    for i in temp_list:
        for j in i:
            possible_move.append(j)
    return possible_move

def all_tried_move(node):
    move_list = []
    for i in node.children:
        move_list.append(i.state.saved_move[-1][0])
    return move_list

def compare(x, y):
    if str(x) == str(y):
        return True
    return False


class MCTS:
    'have the basic skeleton'
    def __init__(self, state, turn):
        self.time_limit = 305
        self.start = node(None, state, turn)
        self.turn = turn

    def run_search(self):
        while self.time_limit != 0:
            leaf = self._select(self.start)
            cnode = self._expand(leaf)
            who_win = self._simulate(cnode)
            self._backpropagate(cnode, who_win)
            self.time_limit -= 1
        score = float('-inf')
        best = None
        for i in self.start.children:
            # temp_score = UCB(i)
            # if temp_score > score:
            #     score = temp_score
            if i.win/i.round_played > score:
                score = i.win/i.round_played
                best = i
        # print('run search')
        return best.state.saved_move[-1][0]


    def _select(self, nodepick):
        possible_move = get_raw_move(nodepick.state, nodepick.round)
        best = nodepick
        while True:
            if len(best.children) != len(possible_move):
                break
            best = possible_move[0]
            score = float('-inf')
            for i in nodepick.children:
                temp_score = UCB(i)
                if temp_score > score:
                    score = temp_score
                    best = i
            possible_move = get_raw_move(best.state, best.round)
            if len(best.children) == len(possible_move):
                return best
            # print('best')

        return best


    def _expand(self, nodepick):
        possible_move = get_raw_move(nodepick.state, nodepick.round)
        already_try = all_tried_move(nodepick)
        already_try_str = []
        possible_move_str = []
        for i in already_try:
            already_try_str.append(str(i))
        for j in possible_move:
            possible_move_str.append(str(j))
        available = set(possible_move_str) - set(already_try_str)
        if len(available) == 0:
            return nodepick
        rd_choice = random.choice(list(available))
        index = possible_move_str.index(rd_choice)
        i = possible_move[index]
        copy_state = copy.deepcopy(nodepick.state)
        new_turn = opponent_turn(nodepick.round)
        copy_state.make_move(i, nodepick.round)
        unvisited_node = node(nodepick, copy_state, new_turn)
        nodepick.children.append(unvisited_node)
        # # print('expand')
        return unvisited_node


    def _simulate(self, node):
        state = copy.deepcopy(node.state)
        if (node.parent == None):
            parents_round = node.round
        else:
            parents_round = node.parent.round
        round = node.round
        while True:
            who_win = state.is_win(parents_round)
            if who_win != 0:
                break
            temp_list = state.get_all_possible_moves(round)
            possible_move = []
            for i in temp_list:
                for j in i:
                    possible_move.append(j)
            move = random.choice(possible_move)
            state.make_move(move, round)
            parents_round = round
            round = opponent_turn(round)
        # print('simulate')
        return who_win



    def _backpropagate(self, node, who_win):
        while node != None:
            if node.round != who_win or who_win == -1:
                node.win += 1
                node.round_played += 1
            else:
                node.round_played += 1
            node = node.parent
        # print('back')



class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.total_time = 60 * 8
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        start = time.time()
        if self.total_time <= 15:
            moves = self.board.get_all_possible_moves(self.color)
            index = randint(0, len(moves) - 1)
            inner_index = randint(0, len(moves[index]) - 1)
            move = moves[index][inner_index]
        else:
            search = MCTS(self.board, self.color)
            move = search.run_search()
        self.board.make_move(move, self.color)
        end = time.time()
        cost = end - start
        self.total_time -= cost

        return move

