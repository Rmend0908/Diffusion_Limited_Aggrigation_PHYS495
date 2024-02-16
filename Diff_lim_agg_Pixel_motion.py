#pixel motion 495
#Save Seed data!

import numpy
import random
from PIL import Image

n=256
data = numpy.zeros((n,n,3),dtype=numpy.uint8)
danger_zone=numpy.zeros((n,n,1),dtype=numpy.uint8)

live_points_count = 7000
particles = []

#Create random set of live points, and make them visible
i=0
x=numpy.random.randint(0,n-1,size=live_points_count)
y=numpy.random.randint(0,n-1,size=live_points_count)

while i < live_points_count:
    data[x[i]][y[i]] = [255,255,255]
    coord = (x[i],y[i])
    #TODO create a far list and a near list.
    #The near list should only be particles that are within a certain x by x square and are updated every single step
    #The far list are updated every 20 steps.
    particles.append(coord)
    i+=1

center = n//2
#set center to red

data[center][center]=[255,0,0]

#Look at the points around the center, and set them as 'killer' space
danger_zone[center][center]=1

#left and right
danger_zone[center-1][center]=1
danger_zone[center+1][center]=1
data[center-1][center]=[0,255,0]
data[center+1][center]=[0,255,0]

#Up and Down
danger_zone[center][center-1]=1
danger_zone[center][center+1]=1
data[center][center-1]=[0,255,0]
data[center][center+1]=[0,255,0]

image = Image.fromarray(data)
image.show()

for frame in range(100000):
    live_points_count = len(particles)
    rand_motion = numpy.random.randint(0,4,live_points_count)
    movement = list(zip(particles,rand_motion))
    
    if frame % 100 == 0:
        print('iteration: ' + str(frame) + ' Particle Count: ' + str(live_points_count))

    for idx, pixel in enumerate(movement):
        #set current spot to black, pixel[0] is the particle and pixel[1] is the random motion for particle
        x=pixel[0][0]
        y=pixel[0][1]
        data[x][y] = [0,0,0]

        if(pixel[1]==0):
            #Particle moves upwards!
            y+=1

            if(y>=256):
                y=0   
            data[x][y]=[255,255,255]
            particles[idx] = (x,y)

        elif(pixel[1]==1):
            #Particle moves downwards!
            y-=1
            if(y<=-1):
                y=255
            data[x][y]=[255,255,255]
            particles[idx] = (x,y)


        elif(pixel[1]==2):
            #Particle moves left!
            x-=1
            if(x<=-1):
                x=255
            data[x][y]=[255,255,255]
            particles[idx] = (x,y)

        elif(pixel[1]==3):
            #Particle moves right!
            x+=1
            if(x>=256):
                x=0
            data[x][y]=[255,255,255]
            particles[idx] = (x,y)

        else:
            print('error!!!')

        #make the danger-zone check
        if(danger_zone[x][y]==1):
            #print('Danger Zoned!')
            data[x][y] = [255,0,0]
            if(frame>10000/2): data[x][y] = [0,0,255]
            elif(frame>10000/3): data[x][y] = [0,255,0]
            
            particles.pop(idx) # WARNING probably O(N)
            movement.pop(idx)

            danger_zone[x-1][y]=1
            danger_zone[x+1][y]=1
            #data[x-1][y]=[0,255,0]
            #data[x+1][y]=[0,255,0]

            #Up and Down
            danger_zone[x][y-1]=1
            danger_zone[x][y+1]=1
            #data[x][y-1]=[0,255,0]
            #data[x][y+1]=[0,255,0]



        
image = Image.fromarray(data)
image.show()
        
        
