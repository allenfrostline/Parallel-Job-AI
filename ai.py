from factory import check_collision, COLS, join_matrices
import heuristic
from copy import copy
import numpy as np
from collections import namedtuple

Move = namedtuple('Move', ['x', 'result_state'])


class AI(object):
    def __init__(self, factory):
        self.state = factory
        self.heuristics = {

            heuristic.avg_height: -1,
            heuristic.max_height: -3,
            heuristic.scv_machines: -10,
            heuristic.avg_machines: -30,
            heuristic.max_machines: -90,
            heuristic.scv_hours: -100,
            heuristic.avg_hours: -300,
            heuristic.max_hours: -900,
        
        }
        self.instant_play = True

    def new_board(self, x, y, job):
        # return a new board
        return join_matrices(self.state.board, job, (x, y))

    def intersection_point(self, x, job):
        # Find the y coordinate closest to the top where job will collide
        y = 0
        while not check_collision(self.state.board, job, (x, y)):
            y += 1
        return y - 1

    @staticmethod
    def max_x_for_job(job):
        # The furthest position you can move job to the right
        return COLS - len(job[0])

    def utility(self, state):
        # the utility function
        return sum([fun(state) * weight for (fun, weight) in self.heuristics.items()])

    def all_possible_moves(self):
        moves = []
        job = self.state.job
        for x in range(self.max_x_for_job(job) + 1):
            y = self.intersection_point(x, job)
            result_state = copy(self.state)
            result_state.board = join_matrices(self.state.board, job, (x, y))
            for row in result_state.board[:-1]:  # scan all rows of the board
                
                result_state.hours = sum([r for r in row if r > 0])  # compute the total operation hours for tomorrow
                result_state.maxhours = max(result_state.maxhours, result_state.hours)
                result_state.totalhours = np.append(result_state.totalhours, result_state.hours)  # update the total daily operation hours
                
                result_state.machines = len([r for r in row if r == -2 or r > 0])  # compute the total number of machines to be occupied tomorrow
                result_state.maxmachines = max(result_state.maxmachines, result_state.machines)
                result_state.totalmachines = np.append(result_state.totalmachines, result_state.machines)  # update the total daily machines using

            result_state.avgmachines = result_state.totalmachines.mean() if len(result_state.totalmachines) else 0
            result_state.scvmachines = (result_state.totalmachines.std() + 1e-2)**2 / (result_state.totalmachines.mean() + 1e-2)**2 if len(result_state.totalmachines > 1) else 0
            
            result_state.avghours = result_state.totalhours.mean() if len(result_state.totalhours) else 0
            result_state.scvhours = (result_state.totalhours.std() + 1e-2)**2 / (result_state.totalhours.mean() + 1e-2)**2 if len(result_state.totalhours > 1) else 0

            moves.append(Move(x, result_state))
        return moves

    def best_move(self):
        return max(self.all_possible_moves(), key=lambda m: self.utility(m.result_state))

    def make_move(self):
        # Move the current job to the desired position by modifying factoryApp's state
        factory = self.state
        move = self.best_move()
        factory.lock.acquire()
        factory.move_to(move.x)
        if self.instant_play:
            factory.job_y = self.intersection_point(move.x, factory.job)
        factory.lock.release()
