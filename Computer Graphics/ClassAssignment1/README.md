# Basic OpenGL viewer & drawing a hierarchical model
## 1. Manipulate the camera with mouse movement
##### Right, left button은 button callback으로 입력을 받은 뒤 global 변수인 right_button_flag, left_button_flag의 값을 각각 True, False로 변경하는 방식을 통해서 입력이 눌린 상태에서만 작동
##### 커서를 이용해 x, y 좌표를 받아 그 값(xpos, ypos)을 그 전의 원래 위치 값(oldX, oldY)과의 차이 값(azimuth, elevation)만큼 glRotatef 함수를 이용해 회전시켜주고 비슷한 방식으로 xtranslation, ytranslation 값을 구해 glTranslatef 함수를 이용하여 이동
##### Scroll callback 함수를 이용하여 변환된 값 만큼 전역변수인 zoom 값을 변환 시키고 gluPerspective 함수를 이용하여 확대, 축소가 가능
## 2. Create an animating hierarchical model using OpenGL matrix stacks
##### drawCube_glDrawElements() 함수를 이용하여 정육면체를 제작하였으며 glScalef를 이용하여 사이즈를 조절하고 glTranslate로 위치
##### 계층은 5계층으로 하였으며 body를 기준으로 head / hip -> right leg 1 -> right leg 2 -> foot / hip -> left leg 1 -> left leg 2 -> foot / right arm 1 -> right arm 2 -> hand -> weapon / left arm 1 -> left arm 2 -> hand 형태를 구성
