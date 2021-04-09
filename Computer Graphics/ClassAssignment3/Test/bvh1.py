import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *
import math

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

flag = False
skeleton = None
count = 0

class Joint:
    def __init__(self):
        self.name = None
        self.channels = []
        self.offset = []
        self.parent = None
        self.frames = []
        self.children = []
        self.idx = [0, 0]
        self.rot_mat = np.identity(4)
        self.trans_mat = np.identity(4)
        self.strans_mat = np.identity(4)
        self.localtoworld = np.identity(4)
        self.trtr = np.identity(4)
        self.worldpos = np.array([0, 0, 0, 0])

    def update_frame(self, frame):
        pos = [0., 0., 0.]
        rot = [0., 0., 0.]
        
        rot_mat = np.identity(4)
        trans_mat = np.identity(4)
        
        for idx, channel in enumerate(self.channels):
            if channel == 'Xposition':
                pos[0] = self.frames[frame][idx]
                trans_mat[0, 3] = pos[0]
            elif channel == 'Yposition':
                pos[1] = self.frames[frame][idx]
                trans_mat[1, 3] = pos[1]
            elif channel == 'Zposition':
                pos[2] = self.frames[frame][idx]
                trans_mat[2, 3] = pos[2]
            elif channel == 'Xrotation':
                rot[0] = self.frames[frame][idx]
                cos = np.cos(np.radians(rot[0]))
                sin = np.sin(np.radians(rot[0]))
                rot_mat2 = np.identity(4)
                rot_mat2[1, 1] = cos
                rot_mat2[1, 2] = -sin
                rot_mat2[2, 1] = sin
                rot_mat2[2, 2] = cos
                rot_mat = np.dot(rot_mat, rot_mat2)
            elif channel == 'Yrotation':
                rot[0] = self.frames[frame][idx]
                cos = np.cos(np.radians(rot[0]))
                sin = np.sin(np.radians(rot[0]))
                rot_mat2 = np.identity(4)
                rot_mat2[0, 0] = cos
                rot_mat2[0, 2] = sin
                rot_mat2[2, 0] = -sin
                rot_mat2[2, 2] = cos
                rot_mat = np.dot(rot_mat, rot_mat2)
            elif channel == 'Zrotation':
                rot[0] = self.frames[frame][idx]
                cos = np.cos(np.radians(rot[0]))
                sin = np.sin(np.radians(rot[0]))
                rot_mat2 = np.identity(4)
                rot_mat2[0, 0] = cos
                rot_mat2[0, 1] = -sin
                rot_mat2[1, 0] = sin
                rot_mat2[1, 1] = cos
                rot_mat = np.dot(rot_mat, rot_mat2)
        self.rot_mat = rot_mat
        self.trans_mat = trans_mat
        if self.parent:
            self.localtoworld = np.dot(self.parent.trtr, self.strans_mat)
        else:
            self.localtoworld = np.dot(self.strans_mat, self.trans_mat)
            
        self.trtr = np.dot(self.localtoworld, self.rot_mat)
        
        self.worldpos = np.array([self.localtoworld[0, 3],
                                  self.localtoworld[1, 3],
                                  self.localtoworld[2, 3],
                                  self.localtoworld[3, 3]])
        for child in self.children:
            child.update_frame(frame)

class bvhreader:
    def __init__(self, filename):
        self.filename = filename
        self.__root = None
        self.__stack = []
        self.channel_num = 0
        self.frame_time = 0.3
        self.frames = 0
        self.motions = []
        self.loadbvh(self.filename)
        
    @property
    def root(self):
        return self.__root
    
    def loadbvh(self, filename):
        f = open(filename)
        lines = f.readlines()
        parent = None
        current = None
        motion = False
        
        jointName = []
        
        for line in lines[1:len(lines)]:
            tokens = line.split()
            if len(tokens) == 0:
                continue
            if tokens[0] in ["ROOT", "JOINT", "End"]:
                if current is not None:
                    parent = current
                    
                current = Joint()
                current.name = tokens[1]
                jointName.append(current.name)
                
                current.parent = parent
                if len(self.__stack) == 0:
                    self.__root = current
                    
                if current.parent is not None:
                    current.parent.children.append(current)
                
                self.__stack.append(current)
                
            elif "{" in tokens[0]:
                ...
            elif "OFFSET" in tokens[0]:
                offset = []
                for i in range(1, len(tokens)):
                    offset.append(float(tokens[i]))
                current.offset = offset
                current.strans_mat[0, 3] = offset[0]
                current.strans_mat[1, 3] = offset[1]
                current.strans_mat[2, 3] = offset[2]
                
            elif "CHANNELS" in tokens[0]:
                current.channels = tokens[2:len(tokens)]
                current.idx = [self.channel_num, self.channel_num + len(current.channels)]
                self.channel_num += len(current.channels)
                
                
            elif "}" in tokens[0]:
                current = current.parent
                if current:
                    parent = current.parent
                    
            elif "MOTION" in tokens[0]:
                motion = True
            elif "Frames:" in tokens[0]:
                self.frames = int(tokens[1])
                print("2. Number of Frames : " + str(self.frames))
            elif "Frame" in tokens[0]:
                self.frame_time = float(tokens[2])
                print("3. FPS : " + str(1/self.frame_time))
            elif motion:
                data = [float(token) for token in tokens]
                self.get_channel_data(self.__root, data)
                vals = []
                for token in tokens:
                    vals.append(float(token))
                self.motions.append(vals)
        print("4: Number of joints : " + str(len(jointName)))
        print("5. Joint names : ")
        for i in jointName:
            print(i + " ")

    def get_channel_data(self, joint, data):
        channels = len(joint.channels)
        joint.frames.append(data[0:channels])
        data = data[channels:]
        
        for child in joint.children:
            data = self.get_channel_data(child, data)
        return data
    
    def update_frame(self, frame):
        self.root.update_frame(frame)

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
    
def drawCube(p1, p2, width):
    glColor3f(0.9, 0.9, 0.0)
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
    
def drawJoint(joint, skeleton, count, d_flag):
    global flag
    offset = joint.offset
    pos = [0, 0, 0]
    rot_mat = np.array([[1., 0., 0., 0.],
                        [0., 1., 0., 0.],
                        [0., 0., 1., 0.],
                        [0., 0., 0., 1.]])
    offset = np.array([float(offset[0]), float(offset[1]), float(offset[2])])
    if flag == True:
        for j in range(len(joint.channels)):
            i = joint.idx[0] + j
            channel = joint.channels[j]

            if channel.lower() == "xposition":
                pos[0] = skeleton.motions[count][i]
            elif channel.lower() == "yposition":
                pos[1] = skeleton.motions[count][i]
            elif channel.lower() == "zposition":
                pos[2] = skeleton.motions[count][i]
            if channel.lower() == "xrotation":
                rot = skeleton.motions[count][i]
                x = math.radians(rot)
                cos = math.cos(x)
                sin = math.sin(x)
                rot_mat2 = np.array([[1., 0., 0., 0.],
                                     [0., cos, -sin, 0.],
                                     [0., sin, cos, 0.],
                                     [0., 0., 0., 1.]])
                rot_mat = np.dot(rot_mat, rot_mat2)
            elif channel.lower() == "yrotation":
                rot = skeleton.motions[count][i]
                x = math.radians(rot)
                cos = math.cos(x)
                sin = math.sin(x)
                rot_mat2 = np.array([[cos, 0., sin, 0.],
                                     [0., 1., 0, 0.],
                                     [-sin, 0, cos, 0.],
                                     [0., 0., 0., 1.]])
                rot_mat = np.dot(rot_mat, rot_mat2)
            elif channel.lower() == "zrotation":
                rot = skeleton.motions[count][i]
                x = math.radians(rot)
                cos = math.cos(x)
                sin = math.sin(x)
                rot_mat2 = np.array([[cos, -sin, 0., 0.],
                                     [sin, cos, 0., 0.],
                                     [0., 0., 1., 0.],
                                     [0., 0., 0., 1.]])
                rot_mat = np.dot(rot_mat, rot_mat2)
    glPushMatrix()

    glTranslatef(pos[0], pos[1], pos[2])

    if d_flag is True:
        drawCube([0, 0, 0], offset, 0.05)

    glTranslatef(offset[0], offset[1], offset[2])
    glMultMatrixf(rot_mat.T)
    for child in joint.children:
        drawJoint(child, skeleton, count, True)
    glPopMatrix()


def render(count):
    global azimuth, elevation, scrollx, scrolly, zoom, xtranslation, ytranslation, skeleton
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_FILL )
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



    if skeleton is not None:
        glPushMatrix()
        if count == skeleton.frames:
            count = 0
        drawJoint(skeleton.root, skeleton, int(count/2) % skeleton.frames, False)
        glPopMatrix()
    
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
    elif key==glfw.KEY_SPACE:
        if action==glfw.PRESS or action==glfw.REPEAT:
            if flag:
                count = 0
            flag = not flag

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
	global skeleton, flag, count
	flag = False
	count = 0
	print("1. File name: " + paths[0])
	skeleton = bvhreader(paths[0])

def main():
    global count, flag, skeleton
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

    count = 0
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll for and process events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        render(count)
        # Swap front and back buffers
        glfw.swap_buffers(window)
        if flag == True:
            count += 1

    glfw.terminate()
if __name__ == "__main__":
    main()

