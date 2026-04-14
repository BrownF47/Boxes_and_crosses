import random

class agent():

    def __init__(self, agent_type: str, player: str):
        self.agent_type = agent_type
        self.player = player

    def find_move(self, state):
        
        if self.agent_type == 'Random':
            turn = self.find_random_turn(state)
        
        elif self.agent_type == 'User':
            turn = self.find_user_turn()
           
        return turn

    def find_user_turn(self):
        turn = input(f"It is {self.player}'s turn: \n")
        turn = int(turn)
        return turn
    
    def find_random_turn(self, state):
        unplayed_indexes = [i for i, (a, b) in enumerate(state) if a == 0 and b == 0]
        turn = random.choice(unplayed_indexes)
        return turn

    def find_learned_turn(self, state):

        # take in state #

        input_vector = state.flatten()

        # use policy to make move #





