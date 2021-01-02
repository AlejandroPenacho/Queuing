import math

class Queue:
    def __init__(self, rate_out = 0, n_service = 1):
        self.rate_in = rate_in
        self.rate_out = rate_out
        self.n_service = n_service
        self.queue_length = 0

    def get_simulation_data(self):
        return [self.rate_in, self.rate_out]


class JacksonSystem:
    def __init__(self, queue_list, queue_distribution):
        self.queue_list = queue_list
        self.queue_distribution = queue_distribution

    def step_initialization(self):
        change_rate = 0
        state_change_list = {}
        for queue in self.queue_list:
            for value,change in zip(queue.get_simulation_data(), ['in','out']):
                change_rate += value
                state_change_list.append([change_rate, [queue, change]])

        for state_change in state_change_list: 
            state_change[0] /= change_rate
