import math
import random

class Queue:
    '''
    Defines a simple queue of type M/M/s/infty. The rate in is not a attribute since it is given
    in the corresponing Jackson network.
    '''
    def __init__(self, std_rate_out, n_services = 1):
        self.type = 'normal'
        self.std_rate_out = std_rate_out
        self.n_services = n_services
        self.queue_length = 0

    def __str__(self):
        return f'Queue object:\n\tType:\t\t{self.type}\n\tBase rate out:\t{self.std_rate_out}\n\tNº services:\t{self.n_services}\n\tCurrent length:\t{self.queue_length}\n'

    def get_rate_out(self):
        return self.std_rate_out * min(self.queue_length, self.n_services)

    def decrease_queue_length(self):
        self.queue_length -= 1
        assert(self.queue_length >= 0)

    def increase_queue_length(self):
        self.queue_length += 1


class Entrance(Queue):
    def __init__(self, std_rate_out):
        self.std_rate_out = std_rate_out
        self.n_services = 1
        self.queue_length = 0
        self.type = 'entrance'

    def get_rate_out(self):
        return self.std_rate_out

    def decrease_queue_length(self):
        pass

    def increase_queue_length(self):
        pass


class JacksonNetwork:
    '''
    Defines a Jacskon network, given by a rate of entrance to the network, 
    a list of queues and a list with the destination of people.
    '''
    def __init__(self, rate_in, queue_list, queue_distribution, initial_length = 0):
        
        entrance = Entrance(rate_in)

        self.queue_list = [entrance] + queue_list
        self.queue_distribution = queue_distribution
        self.n_queues = len(self.queue_list)
        self.current_time = 0

        self.total_time_person = [0 for i in self.queue_list]

        if initial_length:
            if type(initial_length) == list:
                for i in range(1, len(initial_length)):
                    self.queue_list[i].queue_length = initial_length[i]
            else:
                for i in range(1, len(initial_length)):
                    self.queue_list[i].queue_length = initial_length

        for queue_rates in self.queue_distribution:
            current_value = 0
            for i in range(len(queue_rates)):
                current_value += queue_rates[i]
                queue_rates[i] = current_value

    def step(self, verbose=False):
        total_change_rate = 0
        rate_out_list = []
        for queue in self.queue_list:
                rate_out = queue.get_rate_out()
                total_change_rate += rate_out
                rate_out_list.append(total_change_rate)

        exit_probability_list = [i/total_change_rate for i in rate_out_list]

        time_factor = random.random()
        delta_time = (1/total_change_rate) * math.log(1/(1-time_factor))

        for i in range(1, len(self.queue_list)):
            self.total_time_person[i] += delta_time * self.queue_list[i].queue_length

        exit_queue_factor = random.random()

        for i in range(self.n_queues):
            if exit_queue_factor < exit_probability_list[i]:
                exit_queue_index = i
                break
        
        next_queue_probability = self.queue_distribution[exit_queue_index]

        entry_queue_factor = random.random()
        for i in range(self.n_queues):
            if entry_queue_factor < next_queue_probability[i]:
                entry_queue_index = i
                break

        self.queue_list[exit_queue_index].decrease_queue_length()
        self.queue_list[entry_queue_index].increase_queue_length()
        self.current_time += delta_time

        if verbose:
            text = f'T: {self.current_time:.5f}'
            for queue in self.queue_list[1:]:
                text += f'\t{queue.queue_length}'

            print(text)

    def get_mean_length(self):
        for index, queue in enumerate(self.queue_list[1:]):
            index += 1
            print(f"Queue {index}:\t{self.total_time_person[index]/self.current_time}")


    def __str__(self):
        
        text =  f'Jacskon network with {self.n_queues-1} queues, rate_in = {self.queue_list[0].get_rate_out()}:\n'
        text += f'\tTime:\t{self.current_time}\n'
        text += f'Queue\t\tStd_rate_out\tCurrent length\n'
        for index, queue in enumerate(self.queue_list[1:]):
            text += f'{index+1}\t\t{queue.std_rate_out}\t\t{queue.queue_length}\n'

        return text
        


if __name__=='__main__':
    queue1 = Queue(40)
    queue2 = Queue(40)

    distribution = [[0, 0.5, 0.5],
                    [0.1, 0.5, 0.4],
                    [0.6, 0.2, 0.2]]

    system = JacksonNetwork(20, [queue1, queue2], distribution)


    for i in range(40000):
        system.step()


    system.get_mean_length()
