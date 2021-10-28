# Obj Viewer
##### Obj file drag-and-drop 방식으로 실행
##### glfwSetDropCallback을 사용하여 obj file을 읽어 내용을 저장하고 그 값을 바탕으로 window에 보일 수 있도록 구현
##### 각 vertex positions, vertex normal, faces information을 glDrawArrays() 방식을 통하여 triangle meshes로 render
##### Z key를 입력 시 toggle wireframe과 solid mode를 변경
##### File name, total number of faces, number of faces with 3vertices, number of faces with 4vertices, number of faces more than 4vertices 출력
##### Lighting의 경우 3개의 light sources를 이용
##### S key를 입력 받아 Toggle [shading using normal data in obj file] / [forced smooth shading] 전환이 가능
