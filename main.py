import os
from multiprocessing import Pool


processes = ("space_invaders.py", "dqn_agent.py")


def run_process(process):
    os.system("python {}".format(process))


if __name__ == "__main__":
    pool = Pool(processes=2)
    pool.map(run_process, processes)
