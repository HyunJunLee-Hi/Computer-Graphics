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

fp = None

root_joint = []
joint_num = 0
hierarchy = []
hierarchy_num = 0
offset = []
motions = []
cnt = 0
frame_num = 0
frame_time = 0
act = 0

flag = -1

def init():
    global root_joint, joint_num, hierarchy, hierarchy_num, offset, motions, cnt, frame_num, frame_time, flag
    root_joint = []
    joint_num = 0
    hierarchy = []
    hierarchy_num = 0
    offset = []
    motions = []
    cnt = 0
    frame_num = 0
    frame_time = 0
    flag = -1
    
def drawChess():
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    for i in range(-100, 101):
        glVertex3fv(np.array([i,0,100]))
        glVertex3fv(np.array([i,0,-100]))
        glVertex3fv(np.array([100,0,i]))
        glVertex3fv(np.array([-100,0,i]))
    glEnd()

def drawCube(p1, p2, width):
	
	glColor3f(1, 1, 1)
	
	pt = [[[None]] * 4, [None] * 4]
	p1 = np.array(p1)
	p2 = np.array(p2)
	v1 = p1 - p2
	v1 = v1 / (np.sqrt(np.dot(v1, v1)))
	up = np.array([0.0, 1, 0.0])
        
	if 1.0 - v1[1] < 0.001:
		up[2] += 0.1

	v2 = np.cross(v1, up)
	v2 = v2 / (np.sqrt(np.dot(v2, v2)))
	
	v3 = np.cross(v1, v2)
	v3 = v3 / (np.sqrt(np.dot(v3, v3)))

	v2 *= width
	v3 *= width

	pt[0][0] = p1 + v2
	pt[0][2] = p1 - v2
	pt[0][1] = p1 + v3
	pt[0][3] = p1 - v3
	pt[1][0] = p2 + v2
	pt[1][2] = p2 - v2
	pt[1][1] = p2 + v3
	pt[1][3] = p2 - v3

	glBegin(GL_QUADS)
	for i in range(2):
		glNormal3f(v1[0], v1[0], v1[0])
		for p in pt[i]:
			glVertex3f(p[0], p[1], p[2])
	
	n1 = v2 + v3
	n1 = n1 / (np.sqrt(np.dot(n1, n1)))
	n2 = v2 - v3
	n2 = n2 / (np.sqrt(np.dot(n2, n2)))	

	glNormal3f(n1[0], n1[1], n1[2])
	glVertex3f(pt[0][0][0], pt[0][0][1], pt[0][0][2])
	glVertex3f(pt[1][0][0], pt[1][0][1], pt[1][0][2])
	glVertex3f(pt[1][1][0], pt[1][1][1], pt[1][1][2])
	glVertex3f(pt[0][1][0], pt[0][1][1], pt[0][1][2])

	glNormal3f(n2[0], n2[1], n2[2])
	glVertex3f(pt[0][1][0], pt[0][1][1], pt[0][1][2])
	glVertex3f(pt[1][1][0], pt[1][1][1], pt[1][1][2])
	glVertex3f(pt[1][2][0], pt[1][2][1], pt[1][2][2])
	glVertex3f(pt[0][2][0], pt[0][2][1], pt[0][2][2])

	glNormal3f(-n1[0], -n1[1], -n1[2])
	glVertex3f(pt[0][2][0], pt[0][2][1], pt[0][2][2])
	glVertex3f(pt[1][2][0], pt[1][2][1], pt[1][2][2])
	glVertex3f(pt[1][3][0], pt[1][3][1], pt[1][3][2])
	glVertex3f(pt[0][3][0], pt[0][3][1], pt[0][3][2])

	glNormal3f(-n2[0], -n2[1], -n2[2])
	glVertex3f(pt[0][3][0], pt[0][3][1], pt[0][3][2])
	glVertex3f(pt[1][3][0], pt[1][3][1], pt[1][3][2])
	glVertex3f(pt[1][0][0], pt[1][0][1], pt[1][0][2])
	glVertex3f(pt[0][0][0], pt[0][0][1], pt[0][0][2])

	glEnd()

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

def drawJoint():
    global root_joint, joint_num, hierarchy, hierarchy_num, offset, motions, frame_num, frame_time, flag, act

    t = 0
    k = 0
    
    for i in range(hierarchy_num):
        if hierarchy[i] == '{':
            glPushMatrix()
            p1 = np.array(offset[0])
            p2 = p1 + np.array(offset[t])
            drawCube(p1, p2, 0.1)
            arr = np.array(offset[t])
            glTranslatef(arr[0], arr[1], arr[2])
            t += 1

            if hierarchy[i+1] == '}':
                continue
            elif i == 0:
                if motions[k][0] == 1.0:
                    if motions[k+1][0] == 2.0:
                        if motions[k+2][0] == 3.0:
                            glTranslatef(float(motions[k][act]), float(motions[k+1][act]), float(motions[k+2][act]))                      
                    elif motions[k+1][0] == 3.0:
                        if motions[k+2][0] == 2.0:
                            glTranslatef(float(motions[k][act]), float(motions[k+2][act]), float(motions[k+1][act]))
                if motions[k][0] == 2.0:
                    if motions[k+1][0] == 1.0:
                        if motions[k+2][0] == 3.0:
                            glTranslatef(float(motions[k+1][act]), float(motions[k][act]), float(motions[k+2][act]))   
                    elif motions[k+1][0] == 3.0:
                        if motions[k+2][0] == 1.0:
                            glTranslatef(float(motions[k+2][act]), float(motions[k][act]), float(motions[k+1][act]))
                if motions[k][0] == 3.0:
                    if motions[k+1][0] == 1.0:
                        if motions[k+2][0] == 2.0:
                            glTranslatef(float(motions[k+1][act]), float(motions[k+2][act]), float(motions[k][act]))
                    elif motions[k+1][0] == 2.0:
                        if motions[k+2][0] == 1.0:
                            glTranslatef(float(motions[k+2][act]), float(motions[k+1][act]), float(motions[k][act]))
                if motions[k+3][0] == 6.0:
                    if motions[k+4][0] == 4.0:
                        if motions[k+5][0] == 5.0:
                            glRotatef(float(motions[k+3][act]), 0,0,1)
                            glRotatef(float(motions[k+4][act]), 1,0,0)
                            glRotatef(float(motions[k+5][act]), 0,1,0)
                    elif motions[k+4][0] == 5.0:
                        if motions[k+5][0] == 4.0:
                            glRotatef(float(motions[k+3][act]), 0,0,1)
                            glRotatef(float(motions[k+4][act]), 0,1,0)
                            glRotatef(float(motions[k+5][act]), 1,0,0)
                if motions[k+3][0] == 4.0:
                    if motions[k+4][0] == 6.0:
                        if motions[k+5][0] == 5.0:
                            glRotatef(float(motions[k+3][act]), 1,0,0)
                            glRotatef(float(motions[k+4][act]), 0,0,1)
                            glRotatef(float(motions[k+5][act]), 0,1,0)
                    elif motions[k+4][0] == 5.0:
                        if motions[k+5][0] == 6.0:
                            glRotatef(float(motions[k+3][act]), 1,0,0)
                            glRotatef(float(motions[k+4][act]), 0,1,0)
                            glRotatef(float(motions[k+5][act]), 0,0,1)
                if motions[k+3][0] == 5.0:
                    if motions[k+4][0] == 6.0:
                        if motions[k+5][0] == 4.0:
                            glRotatef(float(motions[k+3][act]), 0,1,0)
                            glRotatef(float(motions[k+4][act]), 0,0,1)
                            glRotatef(float(motions[k+5][act]), 1,0,0)
                    elif motions[k+4][0] == 4.0:
                        if motions[k+5][0] == 6.0:
                            glRotatef(float(motions[k+3][act]), 0,1,0)
                            glRotatef(float(motions[k+4][act]), 1,0,0)
                            glRotatef(float(motions[k+5][act]), 0,0,1)
                
                k += 6

            else:
                if motions[k][0] == 4.0:
                    if motions[k+1][0] == 6.0:
                        if motions[k+2][0] == 5.0:
                            glRotatef(float(motions[k][act]), 1,0,0)
                            glRotatef(float(motions[k+1][act]), 0,0,1)
                            glRotatef(float(motions[k+2][act]), 0,1,0)
                    elif motions[k+1][0] == 5.0:
                        if motions[k+2][0] == 6.0:
                            glRotatef(float(motions[k][act]), 1,0,0)
                            glRotatef(float(motions[k+1][act]), 0,1,0)
                            glRotatef(float(motions[k+2][act]), 0,0,1)
                if motions[k][0] == 5:
                    if motions[k+1][0] == 6.0:
                        if motions[k+2][0] == 4.0:
                            glRotatef(float(motions[k][act]), 0,1,0)
                            glRotatef(float(motions[k+1][act]), 0,0,1)
                            glRotatef(float(motions[k+2][act]), 1,0,0)
                    elif motions[k+1][0] == 4.0:
                        if motions[k+2][0] == 6.0:
                            glRotatef(float(motions[k][act]), 0,1,0)
                            glRotatef(float(motions[k+1][act]), 1,0,0)
                            glRotatef(float(motions[k+2][act]), 0,0,1)
                if motions[k][0] == 6.0:
                    if motions[k+1][0] == 4.0:
                        if motions[k+2][0] == 5.0:
                            glRotatef(float(motions[k][act]), 0,0,1)
                            glRotatef(float(motions[k+1][act]), 1,0,0)
                            glRotatef(float(motions[k+2][act]), 0,1,0)                
                    elif motions[k+1][0] == 5.0:
                        if motions[k+2][0] == 4.0:
                            glRotatef(float(motions[k][act]), 0,0,1)
                            glRotatef(float(motions[k+1][act]), 0,1,0)
                            glRotatef(float(motions[k+2][act]), 1,0,0)

                k += 3
                    
        elif hierarchy[i] == '}':
            glPopMatrix()

    if flag == 1:
        act += 1
    if flag == -1:
        act = 1
    if act == int(frame_num) + 1:
        act = 2

def render():
    global fp, azimuth, elevation, scrollx, scrolly, zoom, xtranslation, ytranslation
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
    glLoadIdentity()

    gluLookAt(0, 0, -5, 0, 0, 0, 0., .1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(zoom, 1, 10,  2000)
    glTranslatef(0., 0., -70)

    glMatrixMode(GL_MODELVIEW)


    glTranslatef(-xtranslation, -ytranslation, 0)

    glRotatef(elevation/2., 1., 0., 0.)
    glRotatef(azimuth/2., 0., 1., 0.)

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
    lightPos = (3., 4., 5., 1.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    # light intensity for each color channel
    lightColor = (1.,0.,0.5,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)


    lightPos = (-3., -4., 5., 0.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos)

    lightColor = (0.,1.,0.5,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor)


    lightPos = (3., 4., -5., 0.)    # try to change 4th element to 0. or 1.
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos)

    lightColor = (0.5,1.,0.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor)
    
    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)
    
    glPushMatrix()

    glColor3ub(0, 0, 255) # glColor*() is ignored if lighting is enabled
    glPopMatrix()

    drawJoint()
    
    glDisable(GL_LIGHTING)


    
def key_callback(window, key, scancode, action, mods):
    global flag
    if key==glfw.KEY_A:
        if action==glfw.PRESS:
            print('press a')
        elif action==glfw.RELEASE:
            print('release a')
        elif action==glfw.REPEAT:
            print('repeat a')
    elif key==glfw.KEY_SPACE and action==glfw.PRESS:
        flag *= -1
        

def cursor_callback(window, xpos, ypos):
    global azimuth, elevation, right_button_flag, oldX, oldY, xtranslation, ytranslation
    #print('mouse cursor moving: (%d, %d)'%(xpos, ypos))
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
    #print('mouse wheel scroll: %d, %d'%(xoffset, yoffset))
    zoom -= yoffset

def drop_callback(window, paths):
    global fp, root_joint, joint_num, hierarchy, hierarchy_num, offset, motions, cnt, frame_num, frame_time, flag
    fp = paths[0]
    init()

    file = open(fp, 'r')
    lines = file.readlines()

    for i in lines:
        elements = i.split()
        if elements[0] == "HIERARCHY":
            continue
        elif elements[0] == "ROOT" or elements[0] == "JOINT":
            root_joint.append(elements[1])
            joint_num += 1
        elif elements[0] == '{':
            hierarchy.append('{')
            hierarchy_num += 1
        elif elements[0] == "OFFSET":
            offset.append(np.array([elements[1], elements[2], elements[3]], 'float32'))
        elif elements[0] == "CHANNELS":
            for j in range(int(elements[1])):
                motions.append([])
                if elements[j+2].upper() == "XPOSITION":
                    motions[cnt].append(1.0)
                    motions[cnt].append(0.0)
                elif elements[j+2].upper() == "YPOSITION":
                    motions[cnt].append(2.0)
                    motions[cnt].append(0.0)
                elif elements[j+2].upper() == "ZPOSITION":
                    motions[cnt].append(3.0)
                    motions[cnt].append(0.0)
                elif elements[j+2].upper() == "XROTATION":
                    motions[cnt].append(4.0)
                    motions[cnt].append(0.0)
                elif elements[j+2].upper() == "YROTATION":
                    motions[cnt].append(5.0)
                    motions[cnt].append(0.0)
                elif elements[j+2].upper() == "ZROTATION":
                    motions[cnt].append(6.0)
                    motions[cnt].append(0.0)
                cnt += 1
        elif elements[0] == "End":
            continue
        elif elements[0] == '}':
            hierarchy.append('}')
            hierarchy_num += 1
        elif elements[0] == "MOTION":
            continue
        elif elements[0] == "Frames:":
            frame_num = elements[1]
        elif elements[0] == "Frame":
            frame_time = 1.0 / float(elements[2])
        else:
            for j in range(cnt):
                motions[j].append(elements[j])

    file.close()
    
    print("\n----------------------------\n\n")
    print("1. File name : " + fp)
    print("2. Number of frames : " + str(frame_num))
    print("3. FPS (which is 1/FrameTime) : " + str(frame_time))
    print("4. Number of joints (including root) : " + str(joint_num))
    print("5. List of all joint names : ")
    for i in range(joint_num):
        print(str(root_joint[i]))
    print("\n\n----------------------------\n")
            
def main():
    global gVertexArrayIndexed, gIndexArray
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 640, "2016025887", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    
    # Make the window's context current
    glfw.make_context_current(window)

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
