import cv2
import numpy as np
import os
import json
import random

def extract(img,pointmaps,scale):
    points={}
    x=np.tile(np.arange(img.shape[1]),(img.shape[0],1))
    y=np.tile(np.arange(img.shape[0]),(img.shape[1],1)).T
    lux=np.min(x[img[:,:,3]>0])
    luy=np.min(y[img[:,:,3]>0])
    rdx=np.max(x[img[:,:,3]>0])
    rdy=np.max(y[img[:,:,3]>0])
    chip=img[luy:rdy+1,lux:rdx+1,:]

    h,w,c=chip.shape
    print(h,w)
    chip=cv2.resize(chip,
            (int(w*scale),int(h*scale)),chip)

    ptx=x[pointmaps[:,:,3]>0]
    pty=y[pointmaps[:,:,3]>0]
    is_in_chip_x=(ptx>=lux)&(ptx<=rdx)
    is_in_chip_y=(pty>=luy)&(pty<=rdy)
    is_in_chip=is_in_chip_x&is_in_chip_y
    ptx=ptx[is_in_chip]
    pty=pty[is_in_chip]
    points=[]
    for i in range(ptx.shape[0]):
        point={
            "x":int((ptx[i]-lux-w/2)*scale),
            "y":int(-(pty[i]-luy-h/2)*scale),
            "r":int(pointmaps[pty[i],ptx[i],2]),
            "g":int(pointmaps[pty[i],ptx[i],1]),
            "b":int(pointmaps[pty[i],ptx[i],0])
        }
        points.append(point)
    '''
    for i in range(ptx.shape[0]):
        print(pointmaps[pty[i],ptx[i],0])
        cv2.circle(chip,(ptx[i]-lux,pty[i]-luy),15,
                   (int(pointmaps[pty[i],ptx[i],0]),
                    int(pointmaps[pty[i],ptx[i],1]),
                    int(pointmaps[pty[i],ptx[i],2]),255),thickness=-1)
    '''
    #chip[:,:,2]=255
    #chip[:,:,3]=255
    #r=random.randint(0,256)
    #g=random.randint(0,256)
    #b=random.randint(0,256)
    #chip[:,:,0]=r
    #chip[:,:,1]=g
    #chip[:,:,2]=b

    return {"img":chip,"points":points}

preferences=None
with open('settings.json','r') as f:
    preferences=json.load(f)

source=preferences['source']
dest=preferences['dest']
pointmaps=cv2.imread('{}{}'.format(source,preferences['pointmaps']),-1)
scale=preferences['scale']

list_imgname=os.listdir(source)
log_points={}
for imgname in list_imgname:
    print(imgname)
    img=cv2.imread('{}{}'.format(source,imgname),-1)
    result=extract(img,pointmaps,scale)
    cv2.imwrite('{}{}'.format(dest,imgname),result['img'])
    log_points[imgname]=result['points']
with open('{}log_points.json'.format(dest),'w') as f:
    json.dump(log_points,f,indent=2)
