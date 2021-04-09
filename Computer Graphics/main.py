import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *


azimuth = 0.
elevation = 0.

oldX = 0.
oldY = 0.

right_button_flag = False
left_button_flag = False

xtranslation = 0.
ytranslation = 0.

scrollx = 5.
scrolly = 10.

zoom = 10.

Move_FB = 0
Move_LR = 0

Rot_Q = 0
Rot_E = 0
Reflection = 1

n = np.identity(4)

fp = "cube-tri.obj"

v_arr = np.array([[]], 'float32')
n_arr = np.array([[]], 'float32')
f_arr = np.array([[[]]])
i_arr = np.array([[]], 'int32')

face_3 = 0
face_4 = 0
face_n = 0

toggle_solid = 1
smooth_flag = 1

smooth_shade = list()

Scale = 1

View_mode = 1

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()
    
def drawChess():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-10, 11):
        glVertex3fv(np.array([i,0,10]))
        glVertex3fv(np.array([i,0,-10]))
        glVertex3fv(np.array([10,0,i]))
        glVertex3fv(np.array([-10,0,i]))
    glEnd()

def drawCube():

    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0) 
                             
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0) 
                             
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
                             
    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)
 
    glVertex3f(-1.0, 1.0, 1.0) 
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0) 
    glVertex3f(-1.0,-1.0, 1.0) 
                             
    glVertex3f( 1.0, 1.0,-1.0) 
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

def drawSphere(numLats=12, numLongs=12):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
        # Use Quad strips to draw the sphere glBegin(GL_QUAD_STRIP)
        glBegin(GL_QUAD_STRIP)
        for j in range(0, numLongs + 1):
            lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
            x = np.cos(lng)
            y = np.sin(lng)
            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()
        
def drawLego():
    t = glfw.get_time()
    
    #body
    glPushMatrix()
    glScale(.6, 1, .3)
    glTranslatef(0,np.sin(6*t)*0.7,0)
    drawCube()
    #head
    glPushMatrix()
    glScalef(.7, .5, .7)
    glTranslatef(0,3.5,0)
    drawCube()
    glPopMatrix()
    #right arm_1
    glPushMatrix()
    glScale(.3, .7, .5) 
    glTranslatef(5,.3,0)
    glRotate(-np.sin(3*t)*45,1,0,0)
    drawCube()
    #right arm_2
    glPushMatrix()
    glScale(1, 1, .7)
    glTranslatef(0,-2.1,0)
    glRotate(-np.sin(3*t)*20 + 20 ,1,0,0)
    drawCube()
    #hand
    glPushMatrix()
    glScale(1, .3, .7)
    glTranslatef(0, -5, 0)
    drawCube()
    #weapon
    glPushMatrix()
    glScale(1, .3, 7)
    glTranslatef(0, -5, -1)
    glColor3ub(200, 100, 255)
    drawCube()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()
    #left arm_1
    glPushMatrix()
    glScale(.3, .7, .5) 
    glTranslatef(-5,.3,0)
    glRotate(np.sin(3*t)*45,1,0,0)
    glColor3ub(255, 0, 0)
    drawCube()
    #left arm_2
    glPushMatrix()
    glScale(1, 1, .7)
    glTranslatef(0,-2.1,0)
    glRotate(np.sin(3*t)*20 + 20 ,1,0,0)
    drawCube()
    #hand
    glPushMatrix()
    glScale(1, .3, .7)
    glTranslatef(0, -5, 0)
    drawCube()
    glPopMatrix()
    glPopMatrix()    
    
    glPopMatrix()
    #hip
    glPushMatrix()
    glScalef(1, .3, 1)
    glTranslatef(0,-4,0)
    drawCube()
    #right leg_1
    glPushMatrix()
    glScale(.4, 3, .5) 
    glTranslatef(1.5,-1.3,0)
    glRotate(np.sin(3*t)*45,1,0,0)
    drawCube()
    #right leg_2
    glPushMatrix()
    glScale(1, 1, .6)
    glTranslatef(0, -2.1, 0)
    glRotate(-np.sin(3*t)*10 - 20, 1, 0, 0)
    drawCube()
    #foot
    glPushMatrix()
    glScale(1, .3, 2)
    glTranslatef(0, -5, 0)
    drawCube()
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()
    #left leg_1
    glPushMatrix()
    glScale(.4, 3, .5) 
    glTranslatef(-1.5,-1.3,0)
    glRotate(-np.sin(3*t)*45,1,0,0)
    drawCube()
    #left leg_2
    glPushMatrix()
    glScale(1, 1, .6)
    glTranslatef(0, -2.1, 0)
    glRotate(np.sin(3*t)*10 - 20, 1, 0, 0)
    drawCube()
    #foot
    glPushMatrix()
    glScale(1, .3, 2)
    glTranslatef(0, -5, 0)
    drawCube()
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()


def drawBounced():
    t = glfw.get_time()

    glColor3ub(255, 0, 0)

    glPushMatrix()
    glScale(.3, .3, .3)
    glTranslatef(3, 0, -10)
    glTranslatef(0, np.sin(3*t)*0.4, 0)
    drawLego()
    glPopMatrix()

def drawBounced2():
    t = glfw.get_time()

    glColor3ub(255, 0, 0)

    glPushMatrix()
    glScale(.3, .3, .3)
    glTranslatef(3, 0, -10)
    glTranslatef(np.sin(3*t)*2, 0, 0)
    drawLego()
    glPopMatrix()
    
def drawColliding():
    t = glfw.get_time()

    glColor3ub(255, 255, 0)

    glPushMatrix()
    glScale(.7, .7, .7)
    glTranslatef(-10, 10, 0)
    #자전
    glRotatef(t*(180/np.pi), 0, 1, 0)
    drawSphere()
    glPushMatrix()
    glScale(.5, .5, .5)
    glTranslatef(-5, 0, 0)
    glRotatef(t*(180/np.pi), 0, 1, 0)
    drawSphere()
    glPopMatrix()
    glPopMatrix()

def First_Person_View():
    global azimuth, elevation, scrollx, scrolly, zoom, xtranslation, ytranslation
    global Move_FB, Move_LR

    zoom = 2

    gluLookAt((Move_LR), .8, 0.1 + (Move_FB), (Move_LR), .8,  0.3 + (Move_FB), 0., .1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(zoom, 1, .1, 200)
    glTranslatef(0., 0., -70)

    glMatrixMode(GL_MODELVIEW)   

    glTranslatef(-xtranslation, -ytranslation, 0)

    glRotatef(elevation/2., 1., 0., 0.)
    glRotatef(azimuth/2., 0., 1., 0.)

    
def Quarter_View():
    global zoom
    global Move_FB, Move_LR

    zoom = 10.

    gluLookAt(-5+(Move_LR), -5, -5-(Move_FB), (Move_LR), 0, -(Move_FB), 0., .1, 0)
    #gluLookAt(0, 0, -5, 0, 0, 0, 0., .1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(zoom, 1, .1, 200)
    glTranslatef(0., 0., -70)

    glMatrixMode(GL_MODELVIEW)    
    
def render():
    global azimuth, elevation, scrollx, scrolly, zoom, xtranslation, ytranslation
    global fp, v_arr, i_arr, gVertexArraySeparate, toggle_solid
    global Move_FB, Move_LR
    global Rot_Q, Rot_E, Scale, Reflection, View_mode, n


    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glLoadIdentity()

    if View_mode == 1:
        Quarter_View()
    elif View_mode == -1:
        First_Person_View()

    #glTranslatef(-xtranslation, -ytranslation, 0)

    #glRotatef(elevation/2., 1., 0., 0.)
    #glRotatef(azimuth/2., 0., 1., 0.)

    t = glfw.get_time()

    drawFrame()
    glColor3ub(255, 255, 255)
    drawChess()

    if fp == None:
        return

    glEnable(GL_LIGHTING)   # try to uncomment: no lighting
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

    glEnable(GL_NORMALIZE)  # try to uncomment: lighting will be incorrect if you scale the object
    #glEnable(GL_RESCALE_NORMAL)

    # light position
    glPushMatrix()
    glRotatef(t*(180/np.pi),0,1,0)
    lightPos = (3., 4., 5., 1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    # light intensity for each color channel
    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    glPopMatrix()

    lightPos = (-3., -4., 5., 0.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)

    lightColor = (0.,0.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)


    lightPos = (3., 4., -5., 0.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)

    lightColor = (0.,1.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)


    if toggle_solid == 1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    elif toggle_solid == -1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )

    glPushMatrix()
    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    drawBounced()
    glPopMatrix()

    glPushMatrix()
    objectColor = (0.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    glTranslatef(5., 0., 5.)
    drawBounced2()
    glPopMatrix()

    glPushMatrix()
    glRotatef(t*(180/np.pi), 0, 1, 0)
    objectColor = (1.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    drawColliding()
    glPopMatrix()    

    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    varr = gVertexArraySeparate

    glPushMatrix()

    glColor3ub(0, 0, 255) # glColor*() is ignored if lighting is enabled
    glPushMatrix()
    if View_mode == 1:
        glTranslatef((Move_LR), 0 , -(Move_FB))
    elif View_mode == -1:
        glTranslatef((Move_LR), 0 , (Move_FB))
    glRotate((Rot_Q + Rot_E), 0, 1, 0)
    glScale(Scale, Scale, Scale)
    if Reflection == -1:
        glMultMatrixf(n.T)
    glMultMatrixf(n.T)
    drawPolygon_glDrawArray()
    glPopMatrix()
    glPopMatrix()

    glDisable(GL_LIGHTING)

    
    
 
def key_callback(window, key, scancode, action, mods):
    global toggle_solid, smooth_flag
    global Move_FB, Move_LR
    global Rot_Q, Rot_E, Scale, Reflection, View_mode, n
    if key==glfw.KEY_W:
        if action==glfw.PRESS or action==glfw.REPEAT:
            Move_FB += 0.5
    elif key==glfw.KEY_S:
        if action==glfw.PRESS or action==glfw.REPEAT:
            Move_FB -= 0.5
    elif key==glfw.KEY_A:
        if action==glfw.PRESS or action==glfw.REPEAT:
            Move_LR += 0.5
    elif key==glfw.KEY_D:
        if action==glfw.PRESS or action==glfw.REPEAT:
            Move_LR -= 0.5
    elif key==glfw.KEY_Q:
        if action==glfw.PRESS or action==glfw.REPEAT:
            Rot_Q += -10
    elif key==glfw.KEY_E:
        if action==glfw.PRESS or action==glfw.REPEAT:
            Rot_E += 10
    elif key==glfw.KEY_R and action==glfw.PRESS:
        n = np.array([[-1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]]) @ n
    elif key==glfw.KEY_P and action==glfw.PRESS:
        Scale += .1
    elif key==glfw.KEY_O and action==glfw.PRESS:
        Scale -= .1
    elif key==glfw.KEY_V and action==glfw.PRESS:
        View_mode *= -1
    elif key == glfw.KEY_U and action == glfw.PRESS:
        n = np.array([[1.0, -0.1, -0.1, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]]) @ n
    elif key == glfw.KEY_I and action == glfw.PRESS:
        n = np.array([[1.0, 0.1, 0.1, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]]) @ n


    elif key==glfw.KEY_SPACE and action==glfw.PRESS:
        Move_FB = 0
        Move_LR = 0
        Rot_Q = 0
        Rot_E = 0
        n = np.identity(4)
        Scale = 1
        Reflection = 1
        View_mode = 1
        azimuth = 0.
        elevation = 0.
        xtranslation = 0.
        ytranslation = 0.
        oldX = 0.
        oldY = 0.

    elif key==glfw.KEY_Z:
        if action==glfw.PRESS or action==glfw.REPEAT:
            toggle_solid *= -1
    elif key==glfw.KEY_X:
        if action==glfw.PRESS or action==glfw.REPEAT:
            smooth_flag *= -1

def cursor_callback(window, xpos, ypos):
    global azimuth, elevation, right_button_flag, oldX, oldY, xtranslation, ytranslation
    if right_button_flag == True:
        azimuth += xpos - oldX
        elevation += ypos - oldY
    elif left_button_flag == True:
        xtranslation += (xpos - oldX)/50
        ytranslation += (ypos - oldY)/50
        
        
    oldX = xpos
    oldY = ypos

def button_callback(window, button, action, mod):
    global right_button_flag, left_button_flag
    if button==glfw.MOUSE_BUTTON_LEFT:
        if action==glfw.PRESS:
            right_button_flag = True
        elif action==glfw.RELEASE:
            right_button_flag = False
    if button==glfw.MOUSE_BUTTON_RIGHT:
        if action==glfw.PRESS:
            left_button_flag = True
        elif action==glfw.RELEASE:
            left_button_flag = False
     
def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom -= yoffset

def obj_drop():
    global fp, face_3, face_4, face_n, v_arr, n_arr, f_arr, i_arr, gVertexArraySeparate, smooth_gVertexArraySeparate, toggle_solid, smooth_flag, smooth_shade
    
    gVertexArraySeparate = None
    smooth_gVertexArraySeparate = None

    face_3 = 0
    face_4 = 0
    face_n = 0

    file = open(fp, 'r')
    lines = file.readlines()

    v_arr = np.array([[0., 0., 0.]], 'float32')
    n_arr = np.array([[0., 0., 0.]], 'float32')
    f_arr = np.array([[[0, 0, 0], [0, 0, 0], [0, 0, 0]]])
    i_arr = np.array([[0, 0, 0]], 'int32')

    toggle_solid = 1
    smooth_flag = 1

    smooth_shade = list()
    
    for i in lines:
        if i[0] == '#':
            continue
        elements = i.split(' ')
        elements = [_ for _ in elements if _]
        if elements[0] == 'v':
            v_input = np.array([[float(elements[1]), float(elements[2]), float(elements[3])]], 'float32')
            v_arr = np.append(v_arr, v_input, axis = 0)
            smooth_shade.append([])
        elif elements[0] == 'vn':
            vn_input = np.array([[float(elements[1]), float(elements[2]), float(elements[3])]], 'float32')
            n_arr = np.append(n_arr, vn_input, axis = 0)
        elif elements[0] == 'f':
            if elements[len(elements) - 1] == '\n':
                elements = np.delete(elements, len(elements) - 1, 0)
            if len(elements) == 4:
                face_3 += 1
            elif len(elements) == 5:
                face_4 += 1
            elif len(elements) > 5:
                face_n += 1

            v1 = elements[1].split('/')
            v2 = elements[2].split('/')
            v3 = elements[3].split('/')

            v1, v2, v3 = forming(v1, v2, v3)

            
            f_input = np.array([[[int(v1[0])-1, int(v1[1]), int(v1[2])], [int(v2[0])-1, int(v2[1]), int(v2[2])], [int(v3[0])-1, int(v3[1]), int(v3[2])]]])
            f_arr = np.append(f_arr, f_input, axis = 0)
            get_idx(v1, v2, v3, i_arr)
            i_input = np.array([[int(v1[0])-1, int(v2[0])-1, int(v3[0])-1]])
            i_arr = np.append(i_arr, i_input, axis = 0)
            

        else:
            continue
    
    v_arr = np.delete(v_arr, 0, 0)
    n_arr = np.delete(n_arr, 0, 0)
    f_arr = np.delete(f_arr, 0, 0)
    i_arr = np.delete(i_arr, 0, 0)
    
    gVertexArraySeparate, smooth_gVertexArraySeparate = createVertexArraySeparate()

    file.close()
    
def get_idx(v1, v2, v3, i_arr):
    global smooth_shade
    smooth_shade[int(v1[0])-1].append(len(i_arr)-1)
    smooth_shade[int(v2[0])-1].append(len(i_arr)-1)
    smooth_shade[int(v3[0])-1].append(len(i_arr)-1)
    
def forming(v1, v2, v3):
    while len(v1) < 3:
        v1.append(-1)
    for i in range(3):
        if v1[i] == '':
            v1[i] = -1
    while len(v2) < 3:
        v2.append(-1)
    for i in range(3):
        if v2[i] == '':
            v2[i] = -1
    while len(v3) < 3:
        v3.append(-1)
    for i in range(3):
        if v3[i] == '':
            v3[i] = -1
            
    return v1, v2, v3
                    
def createVertexArraySeparate():
    global v_arr, f_arr, n_arr, i_arr, smooth_flag, smooth_shade
    varr = np.array([[0., 0., 0.]], 'float32')
    fn_arr = np.array([[0., 0., 0.]], 'float32')
    vn_arr = np.array([[0., 0., 0.]], 'float32')

    for i in range(len(f_arr)):
        v1 = v_arr[f_arr[i][1][0]] - v_arr[f_arr[i][0][0]]
        v2 = v_arr[f_arr[i][2][0]] - v_arr[f_arr[i][0][0]]

        n0 = np.array([np.cross(v1, v2)], 'float32')
        n1 = np.array([np.cross(v1, v2)], 'float32')
        n2 = np.array([np.cross(v1, v2)], 'float32')

        fn_arr = np.append(fn_arr, n0, axis = 0)
        
        if f_arr[i][0][2] != -1.0:
            n0 = np.array([n_arr[f_arr[i][0][2]-1]], 'float32')
            n1 = np.array([n_arr[f_arr[i][1][2]-1]], 'float32')
            n2 = np.array([n_arr[f_arr[i][2][2]-1]], 'float32')
            
        varr = np.append(varr, n0, axis = 0)
        varr = np.append(varr, np.array([v_arr[f_arr[i][0][0]]], 'float32'), axis = 0)
        varr = np.append(varr, n1, axis = 0)
        varr = np.append(varr, np.array([v_arr[f_arr[i][1][0]]], 'float32'), axis = 0)
        varr = np.append(varr, n2, axis = 0)
        varr = np.append(varr, np.array([v_arr[f_arr[i][2][0]]], 'float32'), axis = 0)
    
    varr = np.delete(varr, 0, 0)
    fn_arr = np.delete(fn_arr, 0, 0)

    smooth_varr = np.array(varr)
    for i in range(len(v_arr)):
        avg = np.array([0., 0., 0.], 'float32')
        for j in smooth_shade[i]:
            avg += fn_arr[j]
        avg /= len(smooth_shade[i])
        avg = np.array([avg])
        vn_arr = np.append(vn_arr, avg, axis = 0)
    vn_arr = np.delete(vn_arr, 0, 0)
    for i in range(len(f_arr)):
        smooth_varr[i*6 + 0] = vn_arr[f_arr[i][0][0]]
        smooth_varr[i*6 + 2] = vn_arr[f_arr[i][1][0]]
        smooth_varr[i*6 + 4] = vn_arr[f_arr[i][2][0]]

    return varr, smooth_varr

def drawPolygon_glDrawArray():
    global gVertexArraySeparate, smooth_gVertexArraySeparate, smooth_flag
    if smooth_flag == 1:
        varr = gVertexArraySeparate
    else:
        varr = smooth_gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))
    

gVertexArraySeparate = None
smooth_gVertexArraySeparate = None

def main():
    global gVertexArraySeparate
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 640, "2016025887", None, None)
    if not window:
        glfw.terminate()
        return
    # Make the window's context current
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    
    glfw.swap_interval(1)    

    obj_drop()

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render()
        # Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()
if __name__ == "__main__":
    main()

