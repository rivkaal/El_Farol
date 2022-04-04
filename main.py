# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import numpy as np
import math
import matplotlib.pyplot as plt
K = 10
M = 5
T = 60


class Agent:
    def __init__(self, num_of_strategies, memory_size):
        self.memory_size = memory_size
        self.predictions = []
        self.strategies = [[random.uniform(-1, 1) for _ in range(memory_size)] for _ in range(
            num_of_strategies)]
        self.current_strategy = random.choice(self.strategies)
        # self.scores = {str(strategy): 0 for strategy in self.strategies}

    def score_strategies(self, previous_events):
        min_score = math.inf
        for strategy in self.strategies:
            # prev_score = self.scores.get(str(strategy), 0)
            t = min(self.memory_size, len(self.predictions))
            score = np.sum(abs(np.round(self.predictions) - previous_events[-t:]))
            # self.scores[str(strategy)] = score
            if score < min_score:
                self.current_strategy = strategy
                min_score = score

    def predict(self, previous_events):
        # if len(previous_events) == 0:
        #     self.predictions.append(random.uniform(0, 200))
        #     return self.predictions[-1]
        events = previous_events[-self.memory_size:]
        if len(self.predictions) >= self.memory_size:
            self.predictions.pop(0)
        self.predictions.append(np.dot(self.current_strategy, events))
        return self.predictions[-1]


class El_Faro:
    def __init__(self, num_of_strategies, city_size, max_capacity, memory_size):
        self.agents = [Agent(num_of_strategies, memory_size) for _ in range(city_size)]
        self.max_capacity = max_capacity
        self.events = random.sample(range(1, 200), memory_size)

    def do_event(self):
        arrived = 0
        for agent in self.agents:
            if agent.predict(self.events) < self.max_capacity:
                arrived += 1
        self.events = np.append(self.events, arrived)
        for agent in self.agents:
            agent.score_strategies(self.events)


def is_converges(events):
    if len(events) < M:
        return False
    if len(events) == 100:
        print(events)
        return True
    return np.all(np.asarray(events[-M:] == events[-1]))


def main():
    hypotheses = [2, 5, 7, 8, 10, 15, 20]
    result = []
    for k in hypotheses:
        final_nums = []
        for _ in range(10):
            my_el_faro = El_Faro(k, 200, T, M)
            while not is_converges(my_el_faro.events):
                my_el_faro.do_event()
            final_nums.append(my_el_faro.events[-1])
        result.append(np.mean(final_nums))
    plt.scatter(hypotheses, result)
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
