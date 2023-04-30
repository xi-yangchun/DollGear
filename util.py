import math
import pygame

class Utils:
    def __init__(self):
        pass
    def getimg(self,imgname):
        img=pygame.image.load(imgname)
        return img
    def rpos2lpos(self,x,y,cx,cy):
        return (cx+x,cy-y)
    def force(self,parent,child,jname:str):
        targj=parent.joints[jname]
        dx0=-parent.basex+parent.joints[jname].x
        dy0=-parent.basey+parent.joints[jname].y
        dx=dx0*math.cos(math.radians(parent.deg))\
+dy0*math.cos(math.radians(parent.deg+90))
        dy=dx0*math.sin(math.radians(parent.deg))\
+dy0*math.sin(math.radians(parent.deg+90))
        child.set_abspos(parent.absx+dx,parent.absy+dy)
        child.set_deg(parent.deg+targj.deg)
    def sigmoid(self,num):
        s=1/(1+math.exp(-num))
        return s

class Joint:
    def __init__(self,x=0,y=0,deg=0):
        self.x=x;self.y=y
        self.deg=deg
    def set_pos(self,x,y):
        self.x=x;self.y=y
    def set_deg(self,deg):
        self.deg=deg
    def rotate(self,delta):
        self.deg+=delta

class Part:
    def __init__(self,absx=0,absy=0,basex=0,basey=0,deg=0,
                 img=None):
        #ベースポイントの絶対座標
        self.absx=absx;self.absy=absy
        #ベースポイントの相対座標
        self.basex=basex;self.basey=basey
        self.deg=deg
        self.img=img
        self.w=0;self.h=0
        self.memdic={}
        self.joints={}
    def set_abspos(self,absx,absy):
        self.absx=absx;self.absy=absy
    def set_basepos(self,basex,basey):
        self.basex=basex;self.basey=basey
    def set_deg(self,deg):
        self.deg=deg
    def set_img(self,imgname):
        img=Utils.getimg(Utils,imgname)
        self.img=img
        self.set_size()
    def reg_joint(self,name:str,joint:Joint):
        self.joints[name]=joint
    def get_size(self):
        return (self.w,self.h)
    def set_size(self):
        self.w=self.img.get_width()
        self.h=self.img.get_height()
    def draw(self,screen:pygame.Surface,scale:float,dx:int,dy:int):
        thetax=math.radians(self.deg)
        thetay=math.radians(self.deg+90)
        bx=self.basex
        by=self.basey
        dx0=-math.cos(thetax)*bx-math.cos(thetay)*by
        dy0=-math.sin(thetax)*bx-math.sin(thetay)*by
        nx=self.absx+dx0;ny=self.absy+dy0
        targi=pygame.transform.rotozoom(self.img,self.deg,scale)
        dstx,dsty=Utils.rpos2lpos(Utils,
        int(nx*scale)-targi.get_width()//2+dx,
        int(ny*scale)+targi.get_height()//2+dy,
        screen.get_width()//2,screen.get_height()//2)
        screen.blit(targi,(dstx,dsty))
    def get_resized_child(self,size_rate):
        w,h=self.get_size()
        p=Part(self.absx,self.absy,
               int(self.basex*size_rate),int(self.basey*size_rate),
               self.deg,pygame.transform.scale(self.img,
                    (int(w*size_rate),int(h*size_rate))))
        for i in self.joints.items():
            p.reg_joint(i[0],
            Joint(int(i[1].x*size_rate),
                  int(i[1].y*size_rate),self.deg))
        return p

class Doll:
    def __init__(self,parts={},memdic={}):
        self.parts=parts
        self.memdic=memdic
    def det_pose(self,params):
        pass
    def draw(self,scale,dx,dy):
        pass

class ParamConverter:
    def __init__(self):
        pass
    def get_mouth_openess(self,params):
        ux=params[51][0];uy=params[52][1]
        dx=params[57][0];dy=params[57][1]
        rx=params[48][0];ry=params[48][1]
        lx=params[54][0];ly=params[54][1]
        tatedis=((ux-dx)**2+(uy-dy)**2)**(0.5)
        yokodis=((lx-rx)**2+(ly-ry)**2)**(0.5)
        return tatedis/(yokodis+0.001)
    
    def get_face_deg(self,params):
        ux=params[27][0];uy=params[27][1]
        dx=params[8][0];dy=params[8][1]
        d_x=ux-dx;d_y=uy-dy
        #d=(d_x**2+d_y**2)**0.5
        if d_y==0:
            d_y+=0.01
        at=math.atan(d_x/d_y)
        at=math.degrees(at)
        return (at)
    
    def get_left_eye_openess(self,params):
        ux=params[37][0];uy=params[37][1]
        dx=params[41][0];dy=params[41][1]
        rx=params[39][0];ry=params[39][1]
        lx=params[36][0];ly=params[36][1]
        tatedis=((ux-dx)**2+(uy-dy)**2)**(0.5)
        yokodis=((lx-rx)**2+(ly-ry)**2)**(0.5)
        return tatedis/(yokodis+0.001)