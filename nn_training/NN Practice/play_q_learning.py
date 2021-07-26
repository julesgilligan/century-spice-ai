from tensorflow.python.types.core import Value
from deep_q_learning import *

"""
Still need to:
- Translate an integer action into something the environment understands.
- Extract the features meant for a model from the state, which often contains other metadata.
- Implement additional logic for detecting and handling the beginnings and endings of episodes.
"""
EPISODE_NUM = 1000
SHOW_EVERY = 100
LEARNING_DISCOUNT = .99

class Environment():
    """ [0-5] Play from hand
        [6-11] Buy from trades
        [12] Reclaim
        [13-17] Score from points """

    action_len = 18
    state_len = 110

    def __init__(self, gamestate: GameState, player: Player):
        self.gs = gamestate
        self.p1 = player
    
    def state(self, player):
        state: str = self.gs.compress()
        if player == 'p1':
            state += self.p1.compress()
        if len(state) != Environment.state_len:
            raise ValueError("state is the wrong length")
        return state.split()
    
    def do_action(self, action, player) -> int:
        if not (13 <= action and action <= 17):
            return 0 
        return self.gs.point_list[action - 13].worth
        # Obviously, do the actual changing of the game too

    def is_winner(self):
        return self.p1.score_count == 5

for episode in range(EPISODE_NUM):
    gs, p = random_game()
    env = Environment(gs, p)

    p1: Agent = Agent(Environment.state_len, Environment.action_len, target_update_freq = 100, batch_size = 3,
    replay_memory_size = 200, replay_start_size = 200, discount = LEARNING_DISCOUNT)

    # p2: Agent = Agent(STATE_LEN, ACTION_LEN, target_update_freq = 100, batch_size = 3,
    # replay_memory_size = 200, replay_start_size = 200, discount = LEARNING_DISCOUNT)
    
    p1.handle_episode_start()
    # p2.handle_episode_start()
    
    if episode % SHOW_EVERY == 0:
        # print episode code
        pass
    
    #
    # Start game
    #
    p1_last_reward = 0
    p1_last_state = env.state('p1')
    winner = False
    
    while not winner:
        # Player 1 go
        observation = {
            'state' : p1_last_state,
            'reward': p1_last_reward
        }
        action = p1.step(observation)

        p1_last_reward = env.do_action(action, 'p1')
        p1_last_state = env.state('p1')

        winner = env.is_winner()
        if p1.steps > 100:
            break
    print(f"episode {episode} got to {p.score} in {p1.steps} steps")


