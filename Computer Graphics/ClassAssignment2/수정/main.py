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

M = np.identity(4)

fp = None

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

def render():
    global azimuth, elevation, scrollx, scrolly, zoom, xtranslation, ytranslation
    global fp, v_arr, i_arr, gVertexArraySeparate, smooth_gVertexArraySeparate, toggle_solid, smooth_flag
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()

    gluLookAt(0, 0, -5, 0, 0, 0, 0., .1, 0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(zoom, 1, 50,  200)
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
    

    if toggle_solid == 1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    elif toggle_solid == -1:
        glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )


    objectColor = (1.,1.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    glPushMatrix()

    glColor3ub(0, 0, 255) # glColor*() is ignored if lighting is enabled

    drawPolygon_glDrawArray()
    glPopMatrix()

    glDisable(GL_LIGHTING)

    
    
 
def key_callback(window, key, scancode, action, mods):
    global toggle_solid, smooth_flag
    if key==glfw.KEY_A:
        if action==glfw.PRESS:
            print('press a')
        elif action==glfw.RELEASE:
            print('release a')
        elif action==glfw.REPEAT:
            print('repeat a')
    elif key==glfw.KEY_SPACE and action==glfw.PRESS:
        print ('press space: (%d, %d)'%glfw.get_cursor_pos(window))

    elif key==glfw.KEY_Z:
        if action==glfw.PRESS or action==glfw.REPEAT:
            toggle_solid *= -1

    elif key==glfw.KEY_S:
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

def drop_callback(window, paths):
    global fp
    fp = paths[0]
    obj_drop()

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
    
    print("\n\n\nFile name : ", fp)
    print("Total number of faces : ", face_3 + face_4 + face_n)
    print("Number of faces with 3 vertices : ", face_3)
    print("Number of faces with 4 vertices : ", face_4)
    print("Number of faces with more than 4 vertices : ", face_n, "\n\n")

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
    glDrawArrays(GL_QUADS, 0, int(varr.size/6))
    

gVertexArraySeparate = None
smooth_gVertexArraySeparate = None

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480, 480, "2016025887", None, None)
    if not window:
        glfw.terminate()
        return
    # Make the window's context current
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.swap_interval(1)    


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

