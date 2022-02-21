from .position import Position
from .graphs import G
import time

class WrongStep(Exception):
    pass


class Stepper():  # With Position inherenting G

    # def __init__(self, *args):
    #     super(Stepper, self).__init__(*args)

    @classmethod
    def path_interpreter(cls, node1, cor_list, last_map = True):

        """" Iterate over coordinates list. And check and step in parallel. Before every step the check function checks the
        previous step and throws and exception. The cor_list argument is used to do the steps, the node1_id argument is
        used to check the previous step"""

        from .orientation import get_orientation
        # from graphs import df_edges_lvl1
        import threading
        from time import sleep

        # this has to be an immutable object
        ori = []
        ori.append(get_orientation())
        # create an immutable object to save the result of the check job
        status = []
        status.append(True)

        if isinstance(node1, int):
            # if a int (node1_id) was given transform it to an name
            node1_id = node1
            node1_name = G.df_edges_lvl1[(G.df_edges_lvl1['from_id'] == node1_id)].iloc[0]['from_name']
        else:
            node1_name = node1

        for num in range(len(cor_list) - 1):

            current = (node1_name, *cor_list[num], ori[0])  # variable that represents the current position

            # check if current is the same as previous next step
            sleep(0.001)
            t_check = threading.Thread(target=cls.check, args=(current, status))
            print(f'Check complete: {current} ')

            t_check.start()
            #sleep(0.01)

            # do next
            t_step = threading.Thread(target=cls.next_step, args=(current, cor_list[num + 1], ori))
            t_step.start()

            # waiting for both to be done
            t_step.join()
            t_check.join()

            # we did a miss step. Lets break
            if status[0] == False:
                raise WrongStep

        if last_map: # if we change map we do not want to check the step because it wil certainly fail
            # check for the last step
            current = (node1_name, *cor_list[-1], ori[0])  # final element of cor_list
            sleep(0.01)
            cls.check(current, status)

    @classmethod
    def next_step(cls, current, next, ori):
        """ press the buttons to perform the next turn and step. input:
         current: triple tuple (. . .)
         next: tuple (. .)
         ori: string like 'up' """

        from ..fundamentals import turnleft, turnright, turndown, turnup, goup, goright, godown, goleft

        (_, x_current, y_current, ori_current) = current  # ignore map
        (x_next, y_next) = next

        if x_current < x_next:
            if ori_current != 'right':
                turnright()
                ori_current = 'right'
            start_time = time.time()
            goright()
            print(f"Go right Step took: {time.time()-start_time}")
        elif x_current > x_next:
            if ori_current != 'left':
                turnleft()
                ori_current = 'left'
            start_time = time.time()
            goleft()
            print(f"Go left Step took: {time.time()-start_time}")
        elif y_current > y_next:
            if ori_current != 'up':
                turnup()
                ori_current = 'up'
            start_time = time.time()
            goup()
            print(f"Go up Step took: {time.time()-start_time}")
        elif y_current < y_next:
            if ori_current != 'down':
                turndown()
                ori_current = 'down'
            start_time = time.time()
            godown()
            print(f"Go down Step took: {time.time()-start_time}")

        # return ori
        ori[0] = ori_current

    @classmethod
    def check(cls, current, status):
        # from position import Position

        try:
            _, _, x, y = Position.eval_position()  # ignore map, id. get position can throw a LocationNotFoundError
        except:
            status[0] = False
            return
        # actual check
        if (x, y) != (current[1], current[2]):
            status[0] = False
            print(f"step check not satisfied")