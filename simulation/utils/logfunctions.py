import csv
from . import settings as s

def write_to_csv(experiment_list):
    with open("simulation/experiments/log_9.csv", 'a') as f:
        writer = csv.writer(f)
        writer.writerow(experiment_list)

def get_list(self, count, avg_health):
    experiment_list = list()
    # experiment_list.append(s.PERCENTAGE)
    # experiment_list.append(s.CHANCE)
    experiment_list.append(self.percentage_lazy)
    experiment_list.append(self.selfish_chance)
    # experiment_list.append(self.num_neighbors)
    experiment_list.append(count)
    experiment_list.append(avg_health)

    write_to_csv(experiment_list)
