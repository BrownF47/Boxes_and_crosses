import numpy as np
import matplotlib.pyplot as plt
import agents

class Point():

    def __init__(self, point_coords: tuple):
        self.point_coords = point_coords

class Line():

    def __init__(self, points: tuple, player=None):
        self.point_1 = points[0]
        self.point_2 = points[1]
        self.player = player
        self.orientation = self.point_1[0]==self.point_2[0]
        self.mid_point = ((self.point_1[0]+self.point_2[0])/2, (self.point_1[1]+self.point_2[1])/2)
    
    @classmethod
    def from_midpoint(cls, mid_point: tuple, orientation: bool):
        if orientation:
            point_1 = (mid_point[0], int(mid_point[1]-0.5))
            point_2 = (mid_point[0], int(mid_point[1]+0.5))
        else:
            point_1 = (int(mid_point[0]-0.5), mid_point[1])
            point_2 = (int(mid_point[0]+0.5), mid_point[1])
        return cls((point_1,point_2))

    def print_line(self, message="no message"):
        print(f"Line between {self.point_1} and {self.point_2} -- {message}")

    def __eq__(self, other):
        return isinstance(other, Line) and set([self.point_1, self.point_2]) == set([other.point_1, other.point_2])

class Box():

    def __init__(self, box_center: tuple, player):
        self.box_center = box_center
        self.player = player
        self.box_color = 'black'
        if self.player == 'player_1':
            self.box_color = 'red'
        if self.player == 'player_2':
            self.box_color = 'blue'

class Grid():

    def __init__(self, size, turn=True):
        self.size = size
        self.points = []
        self.lines = []
        self.boxes = []
        

        # If turn=True it is player_1's turn, if False it is player_2's turn.

        self.turn = True

        # init points 

        for i in range(size):
            for j in range(size):
                self.points.append(Point((i, j)))
        #self.print_points()

        # init lines 

        for point in self.points:
            for other_point in self.points:
                if self.check_line_exists((point.point_coords, other_point.point_coords)) == False and self.check_points_dist_is_one((point.point_coords, other_point.point_coords)) == True:
                    self.lines.append(Line((point.point_coords, other_point.point_coords), player=None)) 
        #self.print_unplayed_lines()

        self.played_by_1 = np.zeros(len(self.lines))
        self.played_by_2 = np.zeros(len(self.lines))

    def print_points(self):
        for point in self.points:
            print(point.point_coords)

    def print_unplayed_lines(self):
        for i,line in enumerate(self.lines):
            if (self.played_by_1[i] == 0) and (self.played_by_2[i] == 0):
                print(f"Line between {line.point_1} and {line.point_2}")

    def print_played_lines(self):
        for i,line in enumerate(self.lines):
            if (self.played_by_1[i] == 1) or ((self.played_by_2[i] == 1)):
                print(f"Line between {line.point_1} and {line.point_2}")

    def print_boxes(self):
        for box in self.boxes:
            print(f"Box at {box.box_center} for {box.player}")

    def plot_grid(self):
        for point in self.points:
            plt.scatter(point.point_coords[0], point.point_coords[1], color='black')
        for i,line in enumerate(self.lines):
            if self.played_by_1[i] == 1:
                line_color = 'red'
                linestyle = '-'
            elif self.played_by_2[i] == 1:
                line_color = 'blue'
                linestyle = '-'
            else:
                line_color = 'black'
                linestyle = ':' 
            plt.plot([line.point_1[0], line.point_2[0]], [line.point_1[1], line.point_2[1]], color=line_color, linestyle=linestyle)
            plt.text(line.mid_point[0], line.mid_point[1], f'{i}', size=16, color=line_color)
        for box in self.boxes:
            plt.scatter(box.box_center[0], box.box_center[1], color=box.box_color)
        plt.savefig('Game_state.png')

    def check_point_exists(self, coords: tuple) -> bool:
        for my_point in self.points:
            if coords == my_point.point_coords:
                return True
        
        return False

    def check_line_exists(self, points: tuple) -> bool:
        for line in self.lines:
            if set(points) == set((line.point_1, line.point_2)):
                return True
        
        return False

    def check_points_dist_is_one(self, points: tuple) -> bool: 
        if int((points[0][0] - points[1][0])**2 + (points[0][1] - points[1][1])**2) == 1:
            return True
        else: 
            return False

    def find_lines_from_box_center(self, box_center: tuple) -> tuple[Line, Line, Line, Line]:
        up = Line.from_midpoint((box_center[0], box_center[1]+0.5), False)
        down = Line.from_midpoint((box_center[0], box_center[1]-0.5), False)
        left = Line.from_midpoint((box_center[0]-0.5, box_center[1]), True)
        right = Line.from_midpoint((box_center[0]+0.5, box_center[1]), True)
        return up, down, left, right

    def check_for_full_box(self, move, player):
        did_init_box = False
        line_to_check = Line(move)
        played_lines = [obj for obj, a, b in zip(self.lines, self.played_by_1, self.played_by_2) if a == 1 or b == 1]

        if line_to_check.orientation:
            box_1_center = (line_to_check.mid_point[0]-0.5, line_to_check.mid_point[1])
            box_2_center = (line_to_check.mid_point[0]+0.5, line_to_check.mid_point[1])
            box_centers = [box_1_center, box_2_center]
            for box_center in box_centers:

                up, down, left, right = self.find_lines_from_box_center(box_center)
                if (up in played_lines) and (down in played_lines) and (left in played_lines) and (right in played_lines):
                    self.boxes.append(Box(box_center, player))
                    did_init_box = True
        else:
            box_1_center = (line_to_check.mid_point[0], line_to_check.mid_point[1]-0.5)
            box_2_center = (line_to_check.mid_point[0], line_to_check.mid_point[1]+0.5)
            box_centers = [box_1_center, box_2_center]
            for box_center in box_centers:
                

                up, down, left, right = self.find_lines_from_box_center(box_center)
                if (up in played_lines) and (down in played_lines) and (left in played_lines) and (right in played_lines):
                    self.boxes.append(Box(box_center, player))
                    did_init_box = True
        
        return did_init_box
                    
    def take_turn(self, line_index: int):
        if (self.turn == True):
            player='player_1'
        else:
            player='player_2'
            
        if line_index <= len(self.lines): 
            if (self.played_by_1[line_index] == 1) or (self.played_by_2[line_index] == 1):
                print('Move already played')

            else:
                if player=='player_1':
                    self.played_by_1[line_index] = 1
                else: 
                    self.played_by_2[line_index] = 1

            move = (self.lines[line_index].point_1, self.lines[line_index].point_2)
            did_init_box = self.check_for_full_box(move, player)
            
            if not did_init_box:
                self.turn = not self.turn
                    
        else:
            for point in self.points:
                print(point.point_coords)
            print('Play a valid move (Move index too big)')


def play_game(size):
    myGrid = Grid(size)
    Player_1 = agents.agent(agent_type='User', player='player_1')
    Player_2 = agents.agent(agent_type='Random', player='player_2')
    while sum(myGrid.played_by_1) + sum(myGrid.played_by_2) < len(myGrid.lines):
        state = list(zip(myGrid.played_by_1, myGrid.played_by_2))
        myGrid.plot_grid()
        
        player_turn = 'player_1' if myGrid.turn else 'player_2'
        
        if player_turn == 'player_1':
            user_turn = Player_1.find_move(state)
        else: 
            user_turn = Player_2.find_move(state)
        
        myGrid.take_turn(user_turn)
    
    myGrid.plot_grid()
    player_1_score = 0
    player_2_score = 0
    for box in myGrid.boxes:
        if box.player == 'player_1':
            player_1_score += 1
        else:
            player_2_score += 1
    if player_1_score == player_2_score:
        print('Draw!')
    if player_1_score > player_2_score:
        print('Player 1 wins')
    else:
        print('Player 2 wins')


play_game(4)



    

