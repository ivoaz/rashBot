from Bot import Process


class Agent:
   def __init__(self, name, team, index):
        self.index = index

   def get_output_vector(self, game):
        return Process(self, game)


class agent:
    def __init__(self, team):
        self.index = team != 'blue'

    def get_output_vector(self, game):
        return Process(self, game.GameTickPacket, 2)
