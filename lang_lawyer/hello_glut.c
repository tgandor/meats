#include <GL/glut.h>

// Courtesy: http://kiwwito.com/installing-opengl-glut-libraries-in-ubuntu/
// compile with: -lGL -lglut
// binutils-gold linker is not a requirement.

//Drawing funciton
void draw(void)
{
  //Background color
  glClearColor(0,1,0,1);
  glClear(GL_COLOR_BUFFER_BIT );
  //Draw order
  glFlush();
}

//Main program
int main(int argc, char **argv)
{
  glutInit(&argc, argv);
  //Simple buffer
  glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB );
  glutInitWindowPosition(50,25);
  glutInitWindowSize(500,250);
  glutCreateWindow("Green window");
  //Call to the drawing function
  glutDisplayFunc(draw);
  glutMainLoop();
  return 0;
}
