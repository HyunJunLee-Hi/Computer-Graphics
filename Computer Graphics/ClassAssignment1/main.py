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

zoom = 5.

def drawLego():
    t = glfw.get_time()
    glColor3ub(255, 255, 255)

    #body
    glPushMatrix()
    glScale(.6, 1, .3)
    glTranslatef(0,np.sin(6*t)*0.7,0)
    drawCube_glDrawElements()


    #head
    glPushMatrix()
    glScalef(.7, .5, .7)
    glTranslatef(0,3.5,0)
    drawCube_glDrawElements()
    glPopMatrix()

    #right arm_1
    glPushMatrix()
    glScale(.3, .7, .5) 
    glTranslatef(5,.3,0)
    glRotate(-np.sin(3*t)*45,1,0,0)
    drawCube_glDrawElements()
    #right arm_2
    glPushMatrix()
    glScale(1, 1, .7)
    glTranslatef(0,-2.1,0)
    glRotate(-np.sin(3*t)*20 + 20 ,1,0,0)
    drawCube_glDrawElements()
    #hand
    glPushMatrix()
    glScale(1, .3, .7)
    glTranslatef(0, -5, 0)
    drawCube_glDrawElements()
    #weapon
    glPushMatrix()
    glScale(1, .3, 7)
    glTranslatef(0, -5, -1)
    glColor3ub(200, 100, 255)
    drawCube_glDrawElements()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()

    #left arm_1
    glPushMatrix()
    glScale(.3, .7, .5) 
    glTranslatef(-5,.3,0)
    glRotate(np.sin(3*t)*45,1,0,0)
    glColor3ub(255, 255, 255)
    drawCube_glDrawElements()
    #left arm_2
    glPushMatrix()
    glScale(1, 1, .7)
    glTranslatef(0,-2.1,0)
    glRotate(np.sin(3*t)*20 + 20 ,1,0,0)
    drawCube_glDrawElements()
    #hand
    glPushMatrix()
    glScale(1, .3, .7)
    glTranslatef(0, -5, 0)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()    
    
    glPopMatrix()

    #hip
    glPushMatrix()
    glScalef(1, .3, 1)
    glTranslatef(0,-4,0)
    drawCube_glDrawElements()

    #right leg_1
    glPushMatrix()
    glScale(.4, 3, .5) 
    glTranslatef(1.5,-1.3,0)
    glRotate(np.sin(3*t)*45,1,0,0)
    drawCube_glDrawElements()
    #right leg_2
    glPushMatrix()
    glScale(1, 1, .6)
    glTranslatef(0, -2.1, 0)
    glRotate(-np.sin(3*t)*10 - 20, 1, 0, 0)
    drawCube_glDrawElements()
    #foot
    glPushMatrix()
    glScale(1, .3, 2)
    glTranslatef(0, -5, 0)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()

    #left leg_1
    glPushMatrix()
    glScale(.4, 3, .5) 
    glTranslatef(-1.5,-1.3,0)
    glRotate(-np.sin(3*t)*45,1,0,0)
    drawCube_glDrawElements()
    #left leg_2
    glPushMatrix()
    glScale(1, 1, .6)
    glTranslatef(0, -2.1, 0)
    glRotate(np.sin(3*t)*10 - 20, 1, 0, 0)
    drawCube_glDrawElements()
    #foot
    glPushMatrix()
    glScale(1, .3, 2)
    glTranslatef(0, -5, 0)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()
    
    

def drawSphere(numLats, numLongs):
    for i in range(0, numLats + 1):
        lat0 = np.pi * (-0.5 + float(float(i - 1) / float(numLats)))
        z0 = np.sin(lat0)
        zr0 = np.cos(lat0)

        lat1 = np.pi * (-0.5 + float(float(i) / float(numLats)))
        z1 = np.sin(lat1)
        zr1 = np.cos(lat1)
    # Use Quad strips to draw the sphere
    glBegin(GL_QUAD_STRIP)

    for j in range(0, numLongs + 1):
        lng = 2 * np.pi * float(float(j - 1) / float(numLongs))
        x = np.cos(lng)
        y = np.sin(lng)
        glVertex3f(x * zr0, y * zr0, z0)
        glVertex3f(x * zr1, y * zr1, z1)
    glEnd()    
    


def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -1 ,  1 ,  1 ), # v0
            (  1 ,  1 ,  1 ), # v1
            (  1 , -1 ,  1 ), # v2
            ( -1 , -1 ,  1 ), # v3
            ( -1 ,  1 , -1 ), # v4
            (  1 ,  1 , -1 ), # v5
            (  1 , -1 , -1 ), # v6
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr


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

def drawBounced():
    t = glfw.get_time()

    glColor3ub(255, 0, 0)

    glPushMatrix()
    glScale(.5, .5, .5)
    glTranslatef(5, 5, 0)
    glTranslatef(0, np.sin(3*t)*0.4, 0)
    drawCube()
    glPushMatrix()
    glTranslatef(0, 2, 0)
    drawCube()
    glPopMatrix()
    glPopMatrix()

def drawColliding():
    t = glfw.get_time()

    glColor3ub(0, 0, 255)

    glPushMatrix()
    glScale

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
    
def render():
    global azimuth, elevation, scrollx, scrolly, zoom, xtranslation, ytranslation
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    ###
    t = glfw.get_time()
    gluLookAt(0, 0, -5, 0, 0, 0, 0., .1, 0)
    ###
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(zoom, 1, 50,  200)
    glTranslatef(0., 0., -70)

    glMatrixMode(GL_MODELVIEW)


    glTranslatef(-xtranslation, -ytranslation, 0)

    glRotatef(elevation/2., 1., 0., 0.)
    glRotatef(azimuth/2., 0., 1., 0.)

    drawFrame()
    drawBounced()

    glColor3ub(255, 255, 255)
    
    drawLego()
    drawChess()


def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)


    
def key_callback(window, key, scancode, action, mods):
    if key==glfw.KEY_A:
        if action==glfw.PRESS:
            print('press a')
        elif action==glfw.RELEASE:
            print('release a')
        elif action==glfw.REPEAT:
            print('repeat a')
    elif key==glfw.KEY_SPACE and action==glfw.PRESS:
        print ('press space: (%d, %d)'%glfw.get_cursor_pos(window))

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


gVertexArrayIndexed = None
gIndexArray = None

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

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()

    
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
