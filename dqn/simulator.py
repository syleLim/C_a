import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cv2
import time
import random


class Sim :
    def __init__(self, screen_width, screen_height, show_game=True): 
        self.screen_width = screen_width       #Set Camera width == 640
        self.screen_height = screen_height     #Set Camera height == 640

        self.player_point = {'x' : self.screen_width/2, 'y' : self.scr
        een_height}
        self.target_point = {'x' : self.screen_width/2, 'y' : self.screen_height/2 }  #trace point
        self.obstacles = list()    #using obstacle class?
        #TODO : obstcle initial
        self.middle_point = { 'x' : self.screen_height/2, 'y' : self.screen_height/2 }  #goal point

        # target moving effect
        self.is_target_move = False
        self.speed = 5

        # for reward
        self.start_time = 0
        self.target_time = 0

        self.total_reward = 0.
        self.current_reward = 0.
        self.total_game = 0
        self.show_game = show_game

        if show_game:
            self.fig, self.axis = self._prepare_display()

    
    #Target is random move
    def Target_move(self) :
        if is_target_move :
            self.target_point['x'] += random.randrange(-4, 4)
            self.target_point['y'] += random.randrange(0, -2)

        # TODO : if target disappear (out of window range or to backside of obstacle) -> have to arrage model


    def Move_right(self) : 
        # all point turn 


    def Move_left(self) :
        # all point turn 


    def Move_front(self) :
        # all point move
        for obstacle in self.obstacles :
            obstacle['x'] +=1
            obstacle['y'] +=1

        self.target_point['x'] +=1
        self.target_point['y'] +=1


    def Move_back(self) :
        # all point move
        for obstacle in self.obstacles :
            obstacle['x'] -=1
            obstacle['y'] -=1

        self.target_point['x'] -=1
        self.target_point['y'] -=1


    def Check_goal(self) :
        reward = 0

        if self.middle_point['x'] == self.target_point['x'] and self.middle_point['y'] == self.target_point['y'] :
            print('point meet')
            reward = time.time() - self.start_time
            self.start_time = 0

        return reward


    def Update_car(self, flag) : 
        if flag == 1:
            self.Move_front()
        elif flag == 2 :
            self.Move_back()
        elif flag == 3 :
            self.Move_left()
        elif flag == 4 :
            self.Move_right()
        else :
            pass
                        
    def Get_state(self) :
        state = np.zeros(self.screen_width, self.screen_height)

        
        
        for obstacle in self.obstacles :
            for i in obstacle['x'] :
                for j in obstacle['y'] :
                    state[i, j] = 2

                    if state[self.target_point['x'], self.target_point['y']] == 2 :
                        pass
                    else :
                        state[self.target_point['x'], self.target_point['y']] = 1

        return state
        
    # if meet the obstacle, it is die
    def Is_game_over(self) :
        for obstacle in self.obstacles :
            for obstacle in self.obstacles :
                for i in obstacle['x'] :
                    for j in obstacle['y'] :
                        if i == self.player_point['x'] and j == self.player_point['y'] :
                            self.total_reward += self.current_reward
                            return True
        return False            


    def Update(self, flag) :
        # car and target move
        self.Target_move()
        self.Update_car(flag)

        stable_reward = self.Check_goal()
        avoid_reward = 0   #TODO : avoid obstalce point
        is_game_over = Is_game_over()

        if is_game_over : 
            #TODO : Maybe score return
        else :
            reward = stable_reward + avoid_reward
            self.current_reward += reward

        return self.Get_state(), reward, is_game_over
        #TODO : retrun reward and something


    #TODO : show display
    #TODO : Obstacle Initial
    #TODO : Obstacle update
    #TODO : how to count the reward when avoid obstacles

    def Reset() :
        self.current_reward = 0
        self.total_game += 1

        self.player_point = {'x' : self.screen_width/2, 'y' : self.screen_height}
        self.target_point = {'x' : self.screen_width/2, 'y' : self.screen_height/2 }  #trace point
        self.obstacles = list()    #using obstacle class?
        self.middle_point = { 'x' : self.screen_height/2, 'y' : self.screen_height/2 }  #goal point        
        #if game over = data reset
        #TODO : obstcle initial

        retrun self.Get_state()  # Why???

   

    def reset(self):
        """자동차, 장애물의 위치와 보상값들을 초기화합니다."""
        self.current_reward = 0
        self.total_game += 1

        self.car["col"] = int(self.screen_width / 2)

        self.block[0]["col"] = random.randrange(self.road_left, self.road_right + 1)
        self.block[0]["row"] = 0
        self.block[1]["col"] = random.randrange(self.road_left, self.road_right + 1)
        self.block[1]["row"] = 0

        self._update_block()

        return self._get_state()

    





    def _is_gameover(self):
        # 장애물과 자동차가 충돌했는지를 파악합니다.
        # 사각형 박스의 충돌을 체크하는 것이 아니라 좌표를 체크하는 것이어서 화면에는 약간 다르게 보일 수 있습니다.
        if ((self.car["col"] == self.block[0]["col"] and
             self.car["row"] == self.block[0]["row"]) or
            (self.car["col"] == self.block[1]["col"] and
             self.car["row"] == self.block[1]["row"])):

            self.total_reward += self.current_reward

            return True
        else:
            return False

    def step(self, action):
        # action: 0: 좌, 1: 유지, 2: 우
        # action - 1 을 하여, 좌표를 액션이 0 일 경우 -1 만큼, 2 일 경우 1 만큼 옮깁니다.
        self._update_car(action - 1)
        # 장애물을 이동시킵니다. 장애물이 자동차에 충돌하지 않고 화면을 모두 지나가면 보상을 얻습니다.
        escape_reward = self._update_block()
        # 움직임이 적을 경우에도 보상을 줘서 안정적으로 이동하는 것 처럼 보이게 만듭니다.
        stable_reward = 1. / self.screen_height if action == 1 else 0
        # 게임이 종료됐는지를 판단합니다. 자동차와 장애물이 충돌했는지를 파악합니다.
        gameover = self._is_gameover()

        if gameover:
            # 장애물에 충돌한 경우 -2점을 보상으로 줍니다. 장애물이 두 개이기 때문입니다.
            # 장애물을 회피했을 때 보상을 주지 않고, 충돌한 경우에만 -1점을 주어도 됩니다.
            reward = -2
        else:
            reward = escape_reward + stable_reward
            self.current_reward += reward

        if self.show_game:
            self._draw_screen()

        return self._get_state(), reward, gameover

    def _draw_screen(self):
        title = " Avg. Reward: %d Reward: %d Total Game: %d" % (
                        self.total_reward / self.total_game,
                        self.current_reward,
                        self.total_game)

        # self.axis.clear()
        self.axis.set_title(title, fontsize=12)

        road = patches.Rectangle((self.road_left - 1, 0),
                                 self.road_width + 1, self.screen_height,
                                 linewidth=0, facecolor="#333333")
        # 자동차, 장애물들을 1x1 크기의 정사각형으로 그리도록하며, 좌표를 기준으로 중앙에 위치시킵니다.
        # 자동차의 경우에는 장애물과 충돌시 확인이 가능하도록 0.5만큼 아래쪽으로 이동하여 그립니다.
        car = patches.Rectangle((self.car["col"] - 0.5, self.car["row"] - 0.5),
                                1, 1,
                                linewidth=0, facecolor="#00FF00")
        block1 = patches.Rectangle((self.block[0]["col"] - 0.5, self.block[0]["row"]),
                                   1, 1,
                                   linewidth=0, facecolor="#0000FF")
        block2 = patches.Rectangle((self.block[1]["col"] - 0.5, self.block[1]["row"]),
                                   1, 1,
                                   linewidth=0, facecolor="#FF0000")

        self.axis.add_patch(road)
        self.axis.add_patch(car)
        self.axis.add_patch(block1)
        self.axis.add_patch(block2)

        self.fig.canvas.draw()
        # 게임의 다음 단계 진행을 위해 matplot 의 이벤트 루프를 잠시 멈춥니다.
        plt.pause(0.0001)

    def _prepare_display(self):
        """게임을 화면에 보여주기 위해 matplotlib 으로 출력할 화면을 설정합니다."""
        fig, axis = plt.subplots(figsize=(4, 6))
        fig.set_size_inches(4, 6)
        # 화면을 닫으면 프로그램을 종료합니다.
        fig.canvas.mpl_connect('close_event', exit)
        plt.axis((0, self.screen_width, 0, self.screen_height))
        plt.tick_params(top='off', right='off',
                        left='off', labelleft='off',
                        bottom='off', labelbottom='off')

        plt.draw()
        # 게임을 진행하며 화면을 업데이트 할 수 있도록 interactive 모드로 설정합니다.
        plt.ion()
        plt.show()

        return fig, axis