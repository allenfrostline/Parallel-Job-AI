from ward import check_collision, COLS, join_matrices
import heuristic
from copy import copy
import numpy as np
from collections import namedtuple

Move = namedtuple('Move', ['x', 'result_state'])


class AI(object):
    def __init__(self, ward):
        self.state = ward
        self.heuristics = {

            heuristic.avg_height: -1,
            heuristic.max_height: -2,
            heuristic.scv_beds: -10,
            heuristic.avg_beds: -20,
            heuristic.max_beds: -50,
            heuristic.scv_hours: -100,
            heuristic.avg_hours: -200,
            heuristic.max_hours: -500,
        
        }
        self.instant_play = True

    def new_board(self, x, y, patient):
        # return a new board
        return join_matrices(self.state.board, patient, (x, y))

    def intersection_point(self, x, patient):
        # Find the y coordinate closest to the top where patient will collide
        y = 0
        while not check_collision(self.state.board, patient, (x, y)):
            y += 1
        return y - 1

    @staticmethod
    def max_x_for_patient(patient):
        # The furthest position you can move patient to the right
        return COLS - len(patient[0])

    def utility(self, state):
        # the utility function
        return sum([fun(state) * weight for (fun, weight) in self.heuristics.items()])

    def all_possible_moves(self):
        moves = []
        patient = self.state.patient
        for x in range(self.max_x_for_patient(patient) + 1):
            y = self.intersection_point(x, patient)
            result_state = copy(self.state)
            result_state.board = join_matrices(self.state.board, patient, (x, y))
            for row in result_state.board[:-1]:  # scan all rows of the board
                
                result_state.hours = sum([r for r in row if r > 0])  # compute the total operation hours for tomorrow
                result_state.maxhours = max(result_state.maxhours, result_state.hours)
                result_state.totalhours = np.append(result_state.totalhours, result_state.hours)  # update the total daily operation hours
                
                result_state.beds = len([r for r in row if r == -2 or r > 0])  # compute the total number of beds to be occupied tomorrow
                result_state.maxbeds = max(result_state.maxbeds, result_state.beds)
                result_state.totalbeds = np.append(result_state.totalbeds, result_state.beds)  # update the total daily beds using

            result_state.avgbeds = result_state.totalbeds.mean() if len(result_state.totalbeds) else 0
            result_state.scvbeds = (result_state.totalbeds.std() + 1e-2)**2 / (result_state.totalbeds.mean() + 1e-2)**2 if len(result_state.totalbeds > 1) else 0
            
            result_state.avghours = result_state.totalhours.mean() if len(result_state.totalhours) else 0
            result_state.scvhours = (result_state.totalhours.std() + 1e-2)**2 / (result_state.totalhours.mean() + 1e-2)**2 if len(result_state.totalhours > 1) else 0

            moves.append(Move(x, result_state))
        return moves

    def best_move(self):
        return max(self.all_possible_moves(), key=lambda m: self.utility(m.result_state))

    def make_move(self):
        # Move the current patient to the desired position by modifying wardApp's state
        ward = self.state
        move = self.best_move()
        ward.lock.acquire()
        ward.move_to(move.x)
        if self.instant_play:
            ward.patient_y = self.intersection_point(move.x, ward.patient)
        ward.lock.release()
