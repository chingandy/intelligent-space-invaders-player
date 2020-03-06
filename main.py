import os
from multiprocessing import Pool



processes = ('alien_invasion.py', 'dqn_agent.py')

def run_process(process):
    os.system('python {}'.format(process))



pool = Pool(processes=2)
pool.map(run_process, processes)



# def game():
#     os.system("python alien_invasion.py")
#
# def agent():
#     os.system("python dqn_agent.py")
#
# if __name__ == '__main__':
#     Thread(target=game()).start()
#     Thread(target=agent()).start()
