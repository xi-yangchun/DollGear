from util import *
import math
#振動などの特殊な変換は独自のメソッドで対応する。
class AlienDoll(Doll):
    def __init__(self):
        self.parts={}
        assetdir='alien_parted_025/'

        body=Part(0,0,0,-40,0)
        body.set_img('{}body.png'.format(assetdir))
        body.reg_joint('arm_r',Joint(-111,60,0))
        body.reg_joint('arm_l',Joint(50,60,0))
        body.reg_joint('neck',Joint(0,154,0))
        body.reg_joint('tentacle_r_0',Joint(0,-90,30))
        body.reg_joint('tentacle_r_1',Joint(0,-90,45))
        body.reg_joint('tentacle_r_2',Joint(0,-90,60))
        body.reg_joint('tentacle_r_3',Joint(0,-90,60))
        body.reg_joint('tentacle_l_0',Joint(0,-90,-30))
        body.reg_joint('tentacle_l_1',Joint(0,-90,-45))
        body.reg_joint('tentacle_l_2',Joint(0,-90,-60))
        body.reg_joint('tentacle_l_3',Joint(0,-90,-60))
        self.parts['body']=body

        neck=Part(0,0,0,-48,0)
        neck.set_img('{}neck.png'.format(assetdir))
        neck.reg_joint('head',Joint(0,52,0))
        self.parts['neck']=neck

        head=Part(0,0,0,-25)
        head.set_img('{}head.png'.format(assetdir))
        head.reg_joint('ear_right',Joint(-53,20))
        head.reg_joint('ear_left',Joint(53,20))
        head.reg_joint('antenna_right',Joint(-32,-19))
        head.reg_joint('antenna_left',Joint(32,-19))
        head.reg_joint('eyes',Joint(-67,-9,0))
        self.parts['head']=head

        eyes_0=Part(0,0,-67,0,0)
        eyes_0.set_img('{}eyes_0.png'.format(assetdir))
        self.parts['eyes_0']=eyes_0

        eyes_1=Part(0,0,-67,0,0)
        eyes_1.set_img('{}eyes_1.png'.format(assetdir))
        self.parts['eyes_1']=eyes_1
        
        eyes_2=Part(0,0,-67,0,0)
        eyes_2.set_img('{}eyes_2.png'.format(assetdir))
        self.parts['eyes_2']=eyes_2

        eyes_3=Part(0,0,-67,0,0)
        eyes_3.set_img('{}eyes_3.png'.format(assetdir))
        self.parts['eyes_3']=eyes_3

        eyes_4=Part(0,0,-67,0,0)
        eyes_4.set_img('{}eyes_4.png'.format(assetdir))
        self.parts['eyes_4']=eyes_4

        ear_right=Part(0,0,64,22,0)
        ear_right.set_img('{}ear_right.png'.format(assetdir))
        self.parts['ear_right']=ear_right

        ear_left=Part(0,0,-64,22,0)
        ear_left.set_img('{}ear_left.png'.format(assetdir))
        self.parts['ear_left']=ear_left

        antenna_right=Part(0,0,22,81)
        antenna_right.set_img('{}antenna_right.png'.format(assetdir))
        self.parts['antenna_right']=antenna_right

        antenna_left=Part(0,0,-22,81)
        antenna_left.set_img('{}antenna_left.png'.format(assetdir))
        self.parts['antenna_left']=antenna_left

        tentacle_unit=Part(0,0,0,-45)
        tentacle_unit.set_img('{}tentacle_unit.png'.format(assetdir))
        tentacle_unit.reg_joint('next',Joint(0,45,0))
        
        for j in range(4):
            tlis=[]
            c=0.90
            rate=1.0
            for i in range(16):
                p_ten=tentacle_unit.get_resized_child(rate)
                tlis.append(p_ten)
                rate*=c
            self.parts['tentacle_r_{}'.format(j)]=tlis
        
        for j in range(4):
            tlis=[]
            c=0.90
            rate=1.0
            for i in range(16):
                p_ten=tentacle_unit.get_resized_child(rate)
                tlis.append(p_ten)
                rate*=c
            self.parts['tentacle_l_{}'.format(j)]=tlis

        self.memdic={}
        self.memdic['i']=0
        self.memdic['face_deg']=[]
        self.memdic['eye_stack_l']=[]
        self.memdic['mouth_deg']=[]
        self.memdic['tent_deg_r']=[5,15,25,35]
        self.memdic['tent_deg_l']=[-5,-15,-25,-35]
        self.memdic['eye_mode']=0
    
    def draw(self,screen,scale,dx,dy):
        for j in range(4):
            for i in range(16):
                self.parts['tentacle_r_{}'.format(j)][15-i].draw(screen,scale,dx,dy)
        for j in range(4):
            for i in range(16):
                self.parts['tentacle_l_{}'.format(j)][15-i].draw(screen,scale,dx,dy)
        self.parts['neck'].draw(screen,scale,dx,dy)
        self.parts['body'].draw(screen,scale,dx,dy)
        self.parts['ear_right'].draw(screen,scale,dx,dy)
        self.parts['ear_left'].draw(screen,scale,dx,dy)
        self.parts['antenna_right'].draw(screen,scale,dx,dy)
        self.parts['antenna_left'].draw(screen,scale,dx,dy)
        self.parts['head'].draw(screen,scale,dx,dy)
        if self.memdic['eye_mode']==0:
            self.parts['eyes_0'].draw(screen,scale,dx,dy)
        elif self.memdic['eye_mode']==1:
            self.parts['eyes_1'].draw(screen,scale,dx,dy)
        elif self.memdic['eye_mode']==2:
            self.parts['eyes_2'].draw(screen,scale,dx,dy)
        elif self.memdic['eye_mode']==3:
            self.parts['eyes_3'].draw(screen,scale,dx,dy)
        elif self.memdic['eye_mode']==4:
            self.parts['eyes_4'].draw(screen,scale,dx,dy)

    def det_pose(self, params,converter:ParamConverter):
        mouthd=converter.get_mouth_openess(params)
        mouthd=(mouthd-0.75)*3+0.5
        mouthd=self.smooth_mouth_deg(mouthd,4)
        face_deg=converter.get_face_deg(params)
        face_deg=self.smooth_face_deg(face_deg,10)
        eye_l_deg=converter.get_left_eye_openess(params)
        self.memdic['eye_mode']=self.smooth_eye_mode_l(eye_l_deg)
        self.parts['body'].deg=-face_deg*0.25
        self.parts['body'].joints['neck'].deg=-face_deg*0.25
        self.parts['neck'].joints['head'].deg=-face_deg*0.5
        self.parts['head'].joints['antenna_right'].deg=-mouthd*10
        self.parts['head'].joints['antenna_left'].deg=mouthd*10
        self.parts['head'].joints['ear_right'].deg=-mouthd*3
        self.parts['head'].joints['ear_left'].deg=mouthd*3

        self.memdic['i']+=1;self.memdic['i']%=360
        
        for j in range(4):
            avgdeg=0
            d1=0
            d2=0
            d2=math.sin(math.radians(self.memdic['i']*2+20*(16)+j*45)*2)*60
            avgdeg+=d2
            self.parts['body'].joints['tentacle_r_{}'.format(j)].deg\
                =d2-d1+self.memdic['tent_deg_r'][j];d1=d2
            for i in range(16):
                k=i+1
                d2=math.sin(math.radians(self.memdic['i']*2+20*(16-k))*2)*60
                avgdeg+=d2
                self.parts['tentacle_r_{}'.format(j)][i].joints['next'].deg\
                =d2-d1;d1=d2
            avgdeg/=17
            delta=avgdeg-self.memdic['tent_deg_r'][j]
            self.parts['body'].joints['tentacle_r_{}'.format(j)].deg+=delta
            #=self.memdic['i']**2*3
        
        
        for j in range(4):
            avgdeg=0
            d1=0
            d2=0
            d2=-math.sin(math.radians(self.memdic['i']*2+20*(16)+j*45)*2)*60
            avgdeg+=d2
            self.parts['body'].joints['tentacle_l_{}'.format(j)].deg\
                =d2-d1+self.memdic['tent_deg_l'][j];d1=d2
            for i in range(16):
                k=i+1
                d2=-math.sin(math.radians(self.memdic['i']*2+20*(16-k))*2)*60
                avgdeg+=d2
                self.parts['tentacle_l_{}'.format(j)][i].joints['next'].deg\
                =d2-d1;d1=d2
            avgdeg/=17
            delta=avgdeg-self.memdic['tent_deg_l'][j]
            self.parts['body'].joints['tentacle_l_{}'.format(j)].deg+=delta

        #self.parts['body_upper'].joints['arm_r'].deg=i
    
        Utils.force(Utils,self.parts['body'],
                    self.parts['neck'],'neck')
        Utils.force(Utils,self.parts['neck'],
                    self.parts['head'],'head')
        Utils.force(Utils,self.parts['head'],
                    self.parts['ear_right'],'ear_right')
        Utils.force(Utils,self.parts['head'],
                    self.parts['ear_left'],'ear_left')
        Utils.force(Utils,self.parts['head'],
                    self.parts['antenna_right'],'antenna_right')
        Utils.force(Utils,self.parts['head'],
                    self.parts['antenna_left'],'antenna_left')
        
        for i in range(5):
            Utils.force(Utils,self.parts['head'],
                        self.parts['eyes_{}'.format(i)],'eyes')

        for j in range(4):
            Utils.force(Utils,self.parts['body'],
                        self.parts['tentacle_r_{}'.format(j)][0],
                        'tentacle_r_{}'.format(j))
            for i in range(15):
                Utils.force(Utils,self.parts['tentacle_r_{}'.format(j)][i],
                        self.parts['tentacle_r_{}'.format(j)][i+1],'next')
        
        for j in range(4):
            Utils.force(Utils,self.parts['body'],
                        self.parts['tentacle_l_{}'.format(j)][0],
                        'tentacle_l_{}'.format(j))
            for i in range(15):
                Utils.force(Utils,self.parts['tentacle_l_{}'.format(j)][i],
                        self.parts['tentacle_l_{}'.format(j)][i+1],'next')
    
    def smooth_face_deg(self,new_param,period):
        lis=self.memdic['face_deg']
        if len(lis)<period:
            lis.append(new_param)
        else:
            lis.pop(0)
            lis.append(new_param)
        ret=0
        for i in range(len(lis)):
            ret+=lis[i]
        ret=ret/len(lis)
        return ret
    
    def smooth_mouth_deg(self,new_param,period):
        lis=self.memdic['mouth_deg']
        if len(lis)<period:
            lis.append(new_param)
        else:
            lis.pop(0)
            lis.append(new_param)
        ret=0
        for i in range(len(lis)):
            ret+=lis[i]
        ret=ret/len(lis)
        return ret

    def smooth_eye_mode_l(self,eye_l_deg):
        if eye_l_deg<=0.15:
            ml=4
        elif eye_l_deg>=0.15 and eye_l_deg<=0.20:
            ml=3
        elif eye_l_deg>=0.20 and eye_l_deg<=0.21:
            ml=2
        elif eye_l_deg>=0.21 and eye_l_deg<=0.23:
            ml=1
        else:
            ml=0
        stack=self.memdic['eye_stack_l']
        if len(stack)<5:
            stack.append(ml)
        else:
            stack.pop(0)
            stack.append(ml)
        vote=[0 for i in range(5)]
        for i in range(len(stack)):
            vote[stack[i]]+=1
        mode=0
        for i in range(5):
            if vote[i]>vote[mode]:
                mode=i
        return mode

import pygame
import numpy
import random
from pygame.locals import*
import sys
import os

import cv2
import dlib
import numpy as np

#フィールド：70*140くらいの大きさで

pygame.init()                                             # Pygameの初期化
screen = pygame.display.set_mode((600,600))
clock = pygame.time.Clock() # クロックの設定。異なるPCで異なる速さの動作になることを防ぐ
pygame.display.set_caption("test")                        # タイトルバーに表示する文字

scaler = 0.5
detector = dlib.get_frontal_face_detector()
landmark_predictor = dlib.shape_predictor('model/shape_predictor_68_face_landmarks.dat')
cap = cv2.VideoCapture(0) #内臓カメラ

zd=AlienDoll()
pc=ParamConverter()

while (1):
    # read frame buffer from video
    ret, img = cap.read()
    shape=img.shape
    img=cv2.resize(img,(int(shape[1]*scaler),int(shape[0]*scaler)))
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
        continue
    # detect faces
    faces = detector(img)
    #例外処理　顔が検出されなかった時
    if len(faces) == 0:
        print('no faces')
        img_rec = img
        params=None
    else:
        dlib_shape = landmark_predictor(img,faces[0])
        params = [[p.x, p.y] for p in dlib_shape.parts()]

    screen.fill((0,0,0))

    if params!=None:
        zd.det_pose(params,pc)
    zd.draw(screen,0.8,0,-150)
    pygame.display.update()     # 画面を更新
    clock.tick(40)
    for event in pygame.event.get():
        if event.type == QUIT:  # 閉じるボタンが押されたら終了
            pygame.quit()       # Pygameの終了(画面閉じられる)

            sys.exit()