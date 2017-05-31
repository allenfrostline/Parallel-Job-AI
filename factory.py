# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import pygame as pg
import numpy as np
from copy import deepcopy
from threading import Lock
np.random.seed(123)

# Factory config
MACHINES = 6
SCHEDULE = 28
BOTTLENECK = 12

AVG_DAILY_JOB = 2

MIN_HOURS = 1
MAX_HOURS = 4

MIN_DAYS = 1
MAX_DAYS = 5


# Game config
CELL_SIZE = 30
COLS = MACHINES
ROWS = SCHEDULE
MAX_FPS = 20
DROP_TIME = 20
DRAW = True
FONT = 'Chalkboard.ttc'


COLORS = [
    [0, 0, 0],
    [255, 255, 255],
    [255, 195, 0],
    [100, 100, 100],
    [35, 35, 35]
]


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


def remove_row(board, row):
    del board[row]
    return [[0] * COLS] + board


def join_matrices(mat1, mat2, mat2_off):
    mat3 = deepcopy(mat1)
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            mat3[cy + off_y - 1][cx + off_x] += val
    return mat3


class FactoryApp(object):
    def __init__(self):
        self.DROPEVENT = pg.USEREVENT + 1

        pg.init()
        pg.display.set_caption('Factory')
        pg.key.set_repeat(250, 25)
        self.width = CELL_SIZE * (COLS + 13)
        self.height = CELL_SIZE * ROWS
        self.rlim = CELL_SIZE * COLS
        self.bground_grid = [[0 if (x - y) % 2 else -1 for x in range(COLS)] for y in range(ROWS)]
        self.default_font = pg.font.Font(FONT, int(CELL_SIZE * 0.7))
        self.large_font = pg.font.Font(FONT, int(CELL_SIZE))
        self.screen = pg.display.set_mode((self.width, self.height))
        self.next_job = np.array([[-2] * np.random.randint(MIN_DAYS, MAX_DAYS + 1)]).T
        self.next_job_val = np.random.randint(MIN_HOURS, MAX_HOURS + 1)
        self.next_job[np.random.randint(0, len(self.next_job))] = self.next_job_val
        self.gameover = False
        self.ai = None
        self.lock = Lock()
        self.init_game()

    def end(self):
        self.gameover = True

    def new_job(self):
        self.job = self.next_job
        self.next_job = np.array([[-2] * np.random.randint(MIN_DAYS, MAX_DAYS + 1)]).T
        self.next_job[np.random.randint(0, len(self.next_job))] = np.random.randint(MIN_HOURS, MAX_HOURS + 1)
        self.job_x = COLS // 2 - len(self.job[0]) // 2
        self.job_y = 0
        self.totaljobs += 1
        self.rest_jobs -= 1

        if check_collision(self.board, self.job, (self.job_x, self.job_y)):
            self.end()
            self.gameovercause = 'upper bound exceeded'

    def new_board(self):
        board = [[0 for x in range(COLS)] for y in range(ROWS)]
        board += [[1 for x in range(COLS)]]
        return board

    def init_game(self):
        self.board = self.new_board()
        self.days = 0
        self.totaljobs = -1
        self.rest_jobs = np.random.poisson(AVG_DAILY_JOB) + 2
        self.new_job()

        self.hours = 0
        self.maxhours = 0
        self.avghours = 0
        self.scvhours = 0
        self.totalhours = np.array([])
        
        self.machines = 0
        self.maxmachines = 0
        self.avgmachines = 0
        self.scvmachines = 0
        self.totalmachines = np.array([])
        
        self.gameovercause = 'keyboard interruption'
        pg.time.set_timer(self.DROPEVENT, DROP_TIME)

    def disp_msg(self, msg, topleft, color = [255, 255, 255]):
        x, y = topleft
        for line in msg.splitlines():
            self.screen.blit(self.default_font.render(line, False, color, None), (x, y))
            y += 14

    def draw_matrix(self, matrix, offset):
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    if val < 0:
                        pg.draw.rect(self.screen, COLORS[val], pg.Rect((off_x + x) * CELL_SIZE, (off_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                    if val > 0:
                        pg.draw.rect(self.screen, COLORS[2], pg.Rect((off_x + x) * CELL_SIZE, (off_y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
                        self.screen.blit(self.default_font.render(str(val), False, COLORS[0], None), ((off_x + x + 0.3) * CELL_SIZE, (off_y + y) * CELL_SIZE))

    def move_to(self, x):
        self.move(x - self.job_x)

    def move(self, delta_x):
        if not self.gameover:
            new_x = self.job_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > COLS - len(self.job[0]):
                new_x = COLS - len(self.job[0])
            if not check_collision(self.board, self.job, (new_x, self.job_y)):
                self.job_x = new_x

    def drop(self):
        self.lock.acquire()
        if not self.gameover:
            self.job_y += 1
            if check_collision(self.board, self.job, (self.job_x, self.job_y)):  # when a job arrives the factory (and will move in tomorrow)
                self.board = join_matrices(self.board, self.job, (self.job_x, self.job_y))
                if self.rest_jobs == 1:  # if this is the last job today
                    self.hours = sum([r for r in self.board[-2] if r > 0])  # compute the total operation hours for tomorrow
                    self.machines = len([r for r in self.board[-2] if r == -2 or r > 0])  # compute the total number of machines to be occupied tomorrow
                    self.totalhours = np.append(self.totalhours, self.hours)  # update the total daily operation hours
                    self.totalmachines = np.append(self.totalmachines, self.machines)  # update the total daily machines using
                    self.board = remove_row(self.board, -2)  # delete the last row in the board
                    self.days += 1  # update the total number of days
                    self.rest_jobs = np.random.poisson(AVG_DAILY_JOB) + 1  # reset the number of jobs for tomorrow
                    while self.rest_jobs == 1:  # if no job tomorrow, skip the day
                        self.hours = sum([r for r in self.board[-2] if r > 0])  # compute the total operation hours for tomorrow
                        self.machines = len([r for r in self.board[-2] if r == -2 or r > 0])  # compute the total number of machines to be occupied tomorrow
                        self.totalhours = np.append(self.totalhours, self.hours)  # update the total daily operation hours
                        self.totalmachines = np.append(self.totalmachines, self.machines)  # update the total daily machines using
                        self.board = remove_row(self.board, -2)  # remove the last row of the board
                        self.days += 1  # update the total number of days
                        self.rest_jobs = np.random.poisson(AVG_DAILY_JOB) + 1  # reset the number of jobs for the next day
                if self.rest_jobs > 1:  # if this not yet the last job today
                    self.new_job()  # welcome another job

                self.hours = sum([r for r in self.board[-2] if r > 0])  # compute the total operation hours for tomorrow
                self.machines = len([r for r in self.board[-2] if r == -2 or r > 0])  # compute the total number of machines to be occupied tomorrow

                self.maxmachines = self.totalmachines.max() if len(self.totalmachines) else 0
                self.avgmachines = self.totalmachines.mean() if len(self.totalmachines) else 0
                self.scvmachines = (self.totalmachines.std() + 1e-2)**2 / (self.totalmachines.mean() + 1e-2)**2 if len(self.totalmachines > 1) else 0
                self.maxhours = self.totalhours.max() if len(self.totalhours) else 0
                self.avghours = self.totalhours.mean() if len(self.totalhours) else 0
                self.scvhours = (self.totalhours.std() + 1e-2)**2 / (self.totalhours.mean() + 1e-2)**2 if len(self.totalhours > 1) else 0

                self.lock.release()

                if self.maxhours > BOTTLENECK:
                	self.end()
                	self.gameovercause = 'hour bottleneck exceeded'
                	return True

                if self.ai:
                    self.ai.make_move()

                return True
        self.lock.release()
        return False

    def insta_drop(self):
        if not self.gameover:
            while not self.drop():
                pass

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def ai_toggle_instant_play(self):
        if self.ai:
            self.ai.instant_play = not self.ai.instant_play

    def run(self):
        key_actions = {
            'ESCAPE': self.end,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'SPACE': self.start_game,
            'RETURN': self.insta_drop,
            'p': self.ai_toggle_instant_play,
            'q': sys.exit,
        }

        clock = pg.time.Clock()
        # self.rest_jobs = np.random.poisson(AVG_DAILY_JOB)
        while True:
            if DRAW:
                self.screen.fill(COLORS[0])
                if self.gameover:
                    tmp = 3
                    self.screen.blit(self.large_font.render('Game Over!', False, COLORS[1], COLORS[0]), (self.width / 2 - CELL_SIZE * 2.5, CELL_SIZE))
                    self.disp_msg('Game over cause: {}'.format(self.gameovercause), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Days: {}'.format(self.days), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    tmp += 1
                    self.disp_msg('Total jobs: {}'.format(self.totaljobs), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Avg. jobs: {:.2f} per day'.format(self.totaljobs / (self.days + 0.) if len(self.totalhours) else 0), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    tmp += 1
                    self.disp_msg('Max machines: {:.0f} (bottleneck: {})'.format(self.maxmachines, COLS), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Avg. machines: {:.2f} per day'.format(self.avgmachines), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('SCV of machines: {:.2f}'.format(self.scvmachines), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    tmp += 1
                    self.disp_msg('Max operation hours: {:.0f} (bottleneck: {})'.format(self.maxhours, BOTTLENECK), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Avg. operation hours: {:.2f} per day'.format(self.avghours), (CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('SCV of operation hours: {:.2f}'.format(self.scvhours), (CELL_SIZE, tmp * CELL_SIZE))
                else:
                    pg.draw.line(self.screen, COLORS[1], (self.rlim + 0.99, 0), (self.rlim + 0.99, self.height - 1))
                    self.disp_msg('Next:', (self.rlim + 8.5 * CELL_SIZE, CELL_SIZE))
                    tmp = 1
                    self.disp_msg('Days: {}'.format(self.days), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    tmp += 1
                    self.disp_msg('Rest jobs: {}'.format(self.rest_jobs), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Total jobs: {}'.format(self.totaljobs), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Avg. jobs: {:.2f}'.format(self.totaljobs / (self.days + 0.) if len(self.totalhours) else 0), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    tmp += 1
                    self.disp_msg('Tomorrow machines: {}'.format(self.machines), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Total machines: {:.0f}'.format(self.totalmachines.sum()), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Avg. machines: {:.2f}'.format(self.avgmachines), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('SCV machines: {:.2f}'.format(self.scvmachines), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Max machines: {:.0f}'.format(self.maxmachines), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Bottleneck machines: {}'.format(COLS), (self.rlim + CELL_SIZE, tmp * CELL_SIZE), [180, 0, 0]); tmp += 1
                    tmp += 1
                    self.disp_msg('Tomorrow hours: {}'.format(self.hours), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Total hours: {:.0f}'.format(self.totalhours.sum()), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Avg. hours: {:.2f}'.format(self.avghours), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('SCV hours: {:.2f}'.format(self.scvhours), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Max hours: {:.0f}'.format(self.maxhours), (self.rlim + CELL_SIZE, tmp * CELL_SIZE)); tmp += 1
                    self.disp_msg('Bottleneck hours: {}'.format(BOTTLENECK), (self.rlim + CELL_SIZE, tmp * CELL_SIZE), [180, 0, 0])

                    self.draw_matrix(self.bground_grid, (0, 0))
                    self.draw_matrix(self.board, (0, 0))
                    self.draw_matrix(self.job, (self.job_x, self.job_y))
                    self.draw_matrix(self.next_job, (COLS + 11, 1))
                pg.display.update()

            for event in pg.event.get():
                if event.type == self.DROPEVENT:
                    self.drop()
                elif event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval('pg.K_' + key):
                            key_actions[key]()
            clock.tick(MAX_FPS)


if __name__ == '__main__':
    from ai import AI
    app = FactoryApp()
    app.ai = AI(app)
    app.ai.instant_play = False
    app.run()
