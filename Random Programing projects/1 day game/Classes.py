import math
import numpy
import ploting
import pygame
import sys


# Define a function to check if a point is inside a rectangle
def pointInRectanlge(px, py, rw, rh, rx, ry):
    if px > rx and px < rx + rw:
        if ry < py < ry + rh:
            return True
    return False


# Create an empty list to store objects
objects = []
# Initialize the Pygame library
pygame.init()

# Define a class for drawing objects and the drwawing screen
"""
This class is where all of the drawing happens.
the entire drawing phase screen is done by this class
"""


class Drawing():
    def __init__(self, screen, objects):
        # Initialize various properties and create buttons and sliders
        self.objects = objects
        self.sliders = []
        self.Button_circle = Button(screen, 50, 50, 200, 50, "circle", self.Circle, self.objects)
        self.Button_rect = Button(screen, 50, 125, 200, 50, "rectangle", self.Rectangele, self.objects)
        self.Button_delete = Button(screen, 50, 200, 200, 50, "Undo", self.Undo, self.objects)
        self.Button_Done = Button(screen, 50, 270, 200, 50, "Done", self.Finished, self.objects)
        self.dencity_slider = Slider(self.sliders, screen, (800, 200), 100, 30, "Dencity (kg/m^3)=", (300, 100))
        self.dencity = self.dencity_slider.getValue()
        self.depth_slider = Slider(self.sliders, screen, (1150, 200), 50, 30, "depth (m)=", (300, 100))
        self.depth = self.depth_slider.getValue()
        self.angle_slider = Slider(self.sliders, screen, (50, 600), 90, 30, "Angle (deg)=", (300, 100))
        self.angle = self.angle_slider.getValue()
        self.v0_slider = Slider(self.sliders, screen, (400, 600), 100, 30, "initial Velocity (m/s)=", (300, 100))
        self.v0 = self.v0_slider.getValue()
        self.start = None
        self.end = None
        self.screen = screen
        self.canvas = pygame.Surface((400, 300))
        self.canvas.set_at((500, 200), (255, 255, 255))
        self.shapes = pygame.sprite.Group()
        self.shape_choice = "Square"
        self.Final_Object = None
        self.current_screen = "Draw"
        self.text_draw = Text(screen, "DRAW", 50, 450, 0, objects)
        self.textvariables = Text(screen, "SET YOUR VARIABLES", 50, 100, 500, objects)
        self.Set_objects_Paramaters = Text(screen, "set your objects parameters", 50, 800, 50, objects)

    # Set the shape choice to "Circle"
    def Circle(self):
        self.shape_choice = "Square"
        pass

    # Set the shape choice to "Rectangle"
    def Rectangele(self):

        self.shape_choice = "Circle"

    # Pop the last added shape from the stack
    def Undo(self):
        index = self.shapes.sprites()
        if len(index) >= 1:
            self.shapes.remove(index[-1])

    # Check if required parameters are set, and switch to the next screen
    # defencive programing
    def Finished(self):
        if self.depth and self.dencity != None and len(self.shapes.sprites()) > 0:
            self.dencity = self.dencity_slider.getValue()
            self.depth = self.depth_slider.getValue()
            self.angle = self.angle_slider.getValue()
            self.v0 = self.v0_slider.getValue()
            self.current_screen = "Dis"

    # Create a square shape and add it to the group of shapes
    def Make_Square(self, start, end):
        if start[0] > end[0]:
            x1 = start[0]
            x2 = end[0]
        else:
            x1 = end[0]
            x2 = start[0]

        if start[1] > end[1]:
            y1 = start[1]
            y2 = end[1]
        else:
            y1 = end[1]
            y2 = start[1]

        length = abs(x1 - x2)
        hight = abs(y2 - y1)
        s = Square(x2, y2, length, hight)
        self.shapes.add(s)

    # Create a circle shape and add it to the group of shapes
    def Make_Circle(self, center, edge):
        x_change = abs(center[0] - edge[0])
        y_change = abs(edge[1] - center[1])
        rad = math.sqrt((x_change ** 2) + (y_change ** 2))
        if center[1] - rad < 100 or center[1] + rad > 400 or center[0] - rad < 350 or center[0] + rad > 750:
            pass
        else:
            c = Circle((0, 0, 255), center, rad)
            self.shapes.add(c)

    # Handle mouse button down events
    def process_click_Down(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            buts = pygame.mouse.get_pressed()
            if buts[0]:
                self.start = pygame.mouse.get_pos()
                if self.start[1] < 100 or self.start[1] > 400 or self.start[0] < 350 or self.start[0] > 750:
                    pass
                else:
                    pass

    # Handle mouse button up events and create shapes
    def process_click_UP(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            buts = pygame.mouse.get_pressed()

            if not buts[0]:
                self.end = pygame.mouse.get_pos()

                if self.start[1] < 100 or self.start[1] > 400 or self.start[0] < 350 or self.start[0] > 750 or \
                        self.end[1] < 100 or self.end[
                    1] > 400 or self.end[0] < 350 or self.end[0] > 750:
                    pass
                else:
                    if self.shape_choice == "Circle":
                        self.Make_Square(self.start, self.end)

                    elif self.shape_choice == "Square":
                        self.Make_Circle(self.start, self.end)

                    else:
                        pass
            self.start, self.end = None, None

    # Display the drawing interface
    def Display(self, ):
        if self.Final_Object is None:
            self.canvas.fill((255, 255, 255))
            self.screen.fill((0, 255, 111))
            self.screen.blit(self.canvas, (350, 100))

            for object in self.objects:
                object.process()
            for slider in self.sliders:
                slider.render()
                slider.changeValue()
            if self.Final_Object != None:
                self.Final_Object.draw(self.screen)
            self.shapes.update()
            self.shapes.draw(self.screen)
            pygame.display.flip()
        else:
            self.screen.fill((0, 0, 0))


# Define a class for serten text elements that cant be blitet to the screen
class Text():
    def __init__(self, screen, text, size, x, y, objects):
        # Initialize text properties and add the text object to the objects list

        self.screen = screen
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('Comic Sans MS', size)
        self.text_surface = self.font.render(text, False, (0, 0, 0))
        objects.append(self)

    # Display the text on the screen
    def process(self, ):
        self.screen.blit(self.text_surface, (self.x, self.y))


# Define a class for sliders
class Slider:
    def __init__(self, sliders, screen, pos: tuple, upperValue: int = 10, Width: int = 30,
                 text: str = "Editing features for simulation", outlineSize: tuple = (300, 100)):
        # Initialize slider properties and add it to the list of sliders
        self.pos = pos
        self.outlineSize = outlineSize
        self.text = text
        self.Width = Width
        self.upperValue = upperValue
        self.screen = screen
        sliders.append(self)

    # returns the current value of the slider
    def getValue(self):
        num = self.Width / (self.outlineSize[0] / self.upperValue)
        if num <= 1:
            return 1
        else:
            return num

    # renders slider and the text showing the value of the slider
    def render(self, ):
        # draw outline and slider rectangles
        pygame.draw.rect(self.screen, (0, 0, 0), (self.pos[0], self.pos[1],
                                                  self.outlineSize[0], self.outlineSize[1]), 3)

        pygame.draw.rect(self.screen, (0, 0, 0), (self.pos[0], self.pos[1],
                                                  self.Width, self.outlineSize[1] - 10))

        # determite size of font
        self.font = pygame.font.Font(pygame.font.get_default_font(), int((15 / 100) * self.outlineSize[1]))

        # create text surface with value
        valueSurf = self.font.render(f"{self.text}: {round(self.getValue())}", True, (255, 0, 0))

        # centre text
        textx = self.pos[0] + (self.outlineSize[0] / 2) - (valueSurf.get_rect().width / 2)
        texty = self.pos[1] + (self.outlineSize[1] / 2) - (valueSurf.get_rect().height / 2)

        self.screen.blit(valueSurf, (textx, texty))

    # allows users to change value of the slider by dragging it.
    def changeValue(self):
        # If mouse is pressed and mouse is inside the slider
        mousePos = pygame.mouse.get_pos()
        if pointInRectanlge(mousePos[0], mousePos[1]
                , self.outlineSize[0], self.outlineSize[1], self.pos[0], self.pos[1]):
            if pygame.mouse.get_pressed()[0]:
                # the size of the slider
                self.Width = mousePos[0] - self.pos[0]

                # limit the size of the slider
                if self.Width < 1:
                    self.Width = 0
                if self.Width > self.outlineSize[0]:
                    self.Width = self.outlineSize[0]


# define class for main menu screen
class Menu():
    def __init__(self, screen, objects):
        self.width, self.hight, = pygame.display.get_surface().get_size()
        self.objects = objects
        self.Button_singleplayer = Button(screen, (self.width / 2) - 100, self.hight - 375, 200, 50, "singleplayer",
                                          self.singleplayer, self.objects)
        self.Button_leaderbored = Button(screen, (self.width / 2) - 100, self.hight - 225, 200, 50, "LeaderBored",
                                         self.leaderbord, self.objects)
        self.Button_online = Button(screen, (self.width / 2) - 100, self.hight - 300, 200, 50, "Online", self.online,
                                    self.objects)
        self.Button_quit = Button(screen, (self.width / 2) - 100, self.hight - 150, 200, 50, "Quit", self.quit,
                                  self.objects)
        self.current_screen = "Menu"
        self.text = Text(screen, "Projectile Motion", 100, (self.width / 2) - 375, (self.hight / 2) - 200, objects)

    # all these functions change which screen is displayed
    def singleplayer(self):
        self.current_screen = "Draw"

    def leaderbord(self):
        self.current_screen = "Leaderbored"
        pass

    def online(self):
        self.current_screen = "Multiplayer"
        pass

    # exit safely
    def quit(self):
        pygame.quit()
        sys.exit()
        pass

    # display buttons
    def display(self):
        for object in self.objects:
            object.process()


# Define a Button class for UI elements
class Button():
    def __init__(self, screen, x, y, width, height, buttonText, Function, objects):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Function = Function
        self.onePress = False
        self.font = pygame.font.SysFont(("Arial"), 30)
        self.screen = screen
        self.fillColors = {
            'normal': '#7FFFD4',
            'hover': '#0000FF',
            'pressed': '#000099',
        }
        # Create button surface and rect

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Render the button text

        self.buttonSurf = self.font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False
        # Add the button to a list of objects

        objects.append(self)

    def process(self):
        # Check mouse position

        mousePos = pygame.mouse.get_pos()
        # Change button color based on mouse interaction

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            # Check for button press

            # Check for button press

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.Function()

                elif not self.alreadyPressed:
                    self.Function()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False
        # Center the button text

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        self.screen.blit(self.buttonSurface, self.buttonRect)


# Define Square and Circle classes
"""these are the classes for the shapes made in the drawing class
they are usefull for geting varables easyly"""


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, length, height):
        super().__init__()
        self.shape = "Square"
        self.image = pygame.Surface([length, height])
        self.image.fill((255, 255, 255))
        pygame.draw.rect(self.image, (0, 0, 255), [0, 0, length, height], 0)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.area = length * height
        self.BR = [self.rect.x + length, self.rect.y + height]
        self.height = 0
        self.height1 = height


class Circle(pygame.sprite.Sprite):
    def __init__(self, color, center, radius):
        super().__init__()
        self.shape = "Circle"
        self.center = center
        self.color = color
        self.radius = radius
        self.height = radius
        self.height1 = self.height

        # create the image
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)

        # set the rect attributes
        self.rect = self.image.get_rect()
        self.rect.x = center[0] - radius
        self.rect.y = center[1] - radius
        self.area = math.pi * (radius * radius)


# Define Combined class, which seems to perform some calculations
"""this class calculats the combined area of the 
2d composit shape and also calls the plot function"""


class Combined(pygame.sprite.Sprite, Drawing):

    def __init__(self, shapes, depth, material, theta, v0):
        super().__init__()
        # Combine the rects o

        segment = 0
        for x in range(len(shapes.sprites()) - 1):
            for y in range((len(shapes.sprites()) - 1) - x):
                if shapes.sprites()[x].shape == "Circle" and shapes.sprites()[x + y].shape == "Circle":
                    x_change = abs(shapes.sprites()[x].center[0] - shapes.sprites()[x + y].center[0])
                    y_change = abs(shapes.sprites()[x].center[1] - shapes.sprites()[x + y].center[1])
                    length = math.sqrt((x_change ^ 2) + (y_change ^ 2))
                    if length >= shapes.sprites()[x].radius + shapes.sprites()[x + y].radius or length <= abs(
                            shapes.sprites()[x].radius - shapes.sprites()[x + y].radius):
                        sector_area = 0
                    else:
                        a1 = math.acos(
                            (shapes.sprites()[x].radius ** 2 + length ** 2 - shapes.sprites()[x + y].radius ** 2) / (
                                    2 * shapes.sprites()[x].radius * length))
                        a2 = math.acos(
                            (shapes.sprites()[x + y].radius ** 2 + length ** 2 - shapes.sprites()[x].radius ** 2) / (
                                    2 * shapes.sprites()[x + y].radius * length))
                        sector_area = 0.5 * (
                                shapes.sprites()[x].radius ** 2 * a1 - shapes.sprites()[x].radius ** 2 * math.sin(
                            a1) +
                                shapes.sprites()[x + y].radius ** 2 * a2 - shapes.sprites()[
                                    x + y].radius ** 2 * math.sin(a2))

                elif shapes.sprites()[x].shape == "Square" and shapes.sprites()[x + y].shape == "Square":
                    rect1 = [shapes.sprites()[x].rect.x, shapes.sprites()[x].rect.y, shapes.sprites()[x].BR[0],
                             shapes.sprites()[x].BR[1]]
                    rect2 = [shapes.sprites()[x + y].rect.x, shapes.sprites()[x + y].rect.y,
                             shapes.sprites()[x + y].BR[0],
                             shapes.sprites()[x + y].BR[1]]
                    x_overlap = max(0, min(rect1[2], rect2[2]) - max(rect1[0], rect2[0]))
                    y_overlap = max(0, min(rect1[3], rect2[3]) - max(rect1[1], rect2[1]))
                    sector_area = x_overlap * y_overlap

                elif shapes.sprites()[x].shape == "Square" and shapes.sprites()[x + y].shape == "Circle":
                    # Unpack rectangle coordinates
                    rect_x1, rect_y1, rect_x2, rect_y2 = shapes.sprites()[x].rect.x, shapes.sprites()[x].rect.y, \
                                                         shapes.sprites()[x].BR[0], shapes.sprites()[x].BR[1]

                    # Unpack circle coordinates and radius
                    circle_x, circle_y, circle_r = shapes.sprites()[x + y].center[0], shapes.sprites()[x + y].center[
                        1], \
                                                   shapes.sprites()[x + y].radius

                    # Calculate the closest point on the rectangle to the circle
                    closest_x = max(rect_x1, min(circle_x, rect_x2))
                    closest_y = max(rect_y1, min(circle_y, rect_y2))

                    # Check if the closest point is inside the circle
                    if math.sqrt((closest_x - circle_x) ** 2 + (closest_y - circle_y) ** 2) >= circle_r:
                        # No overlap between rectangle and circle
                        sector_area = 0

                    # Calculate the overlapping width and height
                    overlap_width = min(circle_x, rect_x2) - max(circle_x, rect_x1)
                    overlap_height = min(circle_y, rect_y2) - max(circle_y, rect_y1)

                    # Calculate the area of overlap
                    sector_area = overlap_width * overlap_height
                elif shapes.sprites()[x].shape == "Circle" and shapes.sprites()[x + y].shape == "Square":
                    # Unpack rectangle coordinates
                    rect_x1, rect_y1, rect_x2, rect_y2 = shapes.sprites()[x + y].rect.x, shapes.sprites()[
                        x + y].rect.y, \
                                                         shapes.sprites()[x + y].BR[0], shapes.sprites()[x + y].BR[1]

                    # Unpack circle coordinates and radius
                    circle_x, circle_y, circle_r = shapes.sprites()[x].center[0], shapes.sprites()[x].center[1], \
                                                   shapes.sprites()[x].radius

                    # Calculate the closest point on the rectangle to the circle
                    closest_x = max(rect_x1, min(circle_x, rect_x2))
                    closest_y = max(rect_y1, min(circle_y, rect_y2))

                    # Check if the closest point is inside the circle
                    if math.sqrt((closest_x - circle_x) ** 2 + (closest_y - circle_y) ** 2) >= circle_r:
                        # No overlap between rectangle and circle
                        sector_area = 0

                    # Calculate the overlapping width and height
                    overlap_width = min(circle_x, rect_x2) - max(circle_x, rect_x1)
                    overlap_height = min(circle_y, rect_y2) - max(circle_y, rect_y1)

                    # Calculate the area of overlap
                    sector_area = overlap_width * overlap_height

                segment += abs(sector_area)
        area = 0
        for x in range(len(shapes.sprites())):
            area += shapes.sprites()[x].area
        self.__final_area = round((area - segment))
        vol = (((self.__final_area * (depth))))
        self.mass = material * vol
        self.coords, self.Y_Max, self.X_Max, self.X_Final, self.airtime, self.igname = ploting.plot(self.mass,
                                                                                                    self.__final_area,
                                                                                                    v0,
                                                                                                    theta)


# Define TextBox class for text input

class TextBox():

    def __init__(self, x, y, w, h, screen, Function, maxlength=999, text=''):
        self.maxlenght = maxlength
        self.Function = Function
        self.screen = screen
        self.font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def get_text(self):
        return self.text

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = (255, 0, 0) if self.active else (255, 255, 255)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.Function()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) >= self.maxlenght:
                    pass
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self):
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 2)


# Define Display class to manage the main game display

class Display():
    def __init__(self, screen, shapes, coords):
        self.screen = screen
        self.objects = objects
        self.objects.clear()
        self.shapes = shapes
        self.coords = coords
        self.output_list = []
        self.set = False
        self.XSET = False
        self.YSET = False
        self.fly_set = False
        self.timer = [0, 4, -1, 0, 0, 0]
        self.current_screen = "Dis"

        self.Three = Text(screen, "3", 100, 700, 400, objects)
        self.Two = Text(screen, "2", 100, 700, 400, objects)
        self.One = Text(screen, "1", 100, 700, 400, objects)
        self.Go = Text(screen, "GO!!!", 100, 700, 400, objects)
        self.R, self.G, self.B = 0, 255, 111
        for i in range(1, len(coords)):
            diff_x = coords[i][0] - coords[i - 1][0]
            diff_y = coords[i][1] - coords[i - 1][1]
            self.output_list.append([diff_x / 5, diff_y / 10])
        # Scale font
        self.font = pygame.font.Font(None, 36)

    def end_of_Display(self):
        self.current_screen = "Final"

    def Display(self, ):

        self.screen.fill((self.R, self.G, self.B))
        self.shapes.update()
        self.shapes.draw(self.screen)
        if self.R <= 135:
            self.R += 2
        if self.G >= 206:
            self.G -= 2
        if self.B <= 235:
            self.B += 2

        if self.set == False:
            belowLine = False
            behindline = False
            for piece in self.shapes.sprites():
                if self.YSET == False:
                    if piece.rect.y + piece.height1 > 750 - piece.height:
                        belowLine = True
                    else:
                        piece.rect.y += 1
                    if belowLine == True:
                        # at least one piece is below the line
                        self.YSET = True
                if self.XSET == False:
                    if piece.rect.x <= 50:
                        behindline = True
                    else:
                        piece.rect.x -= 2
                    if behindline == True:
                        self.XSET = True
                if self.XSET == True and self.YSET == True:
                    self.set = True
        if self.timer[1] > 0:
            if self.XSET == True and self.YSET == True:
                if self.timer[0] < 60:
                    self.objects[0].process()
                    self.timer[0] += 1
                if self.timer[0] == 60:
                    self.objects.pop(0)
                    self.timer[0] = 0
                    self.timer[1] -= 1
        else:

            if self.timer[3] == len(self.coords):
                pass
            else:
                text = self.font.render(
                    str(("X: ", self.coords[self.timer[3]][0], " Y: ", self.coords[self.timer[3]][1])), True,
                    (255, 255, 255))
                self.timer[3] += 1
                self.screen.blit(text, (500, 500))

                if self.timer[4] < (len(self.coords) / 2):
                    for Y in self.shapes.sprites():
                        Y.rect.y -= 1
                        Y.rect.x += 1
                    self.timer[4] += 1
                elif self.timer[4] >= (len(self.coords) / 2) and self.timer[4] <= len(self.coords):
                    for Y in self.shapes.sprites():
                        Y.rect.y += 1
                        Y.rect.x += 1
                    self.timer[4] += 1
                if self.timer[4] >= len(self.coords):
                    self.end_of_Display()
            self.shapes.update()
            self.shapes.draw(self.screen)
            pygame.display.flip()


# Define Final_screen class for the final screen
class Final_screen():
    def __init__(self, screen, objects, Y_Max, X_Max, X_Final, air_time, igName):
        self.screen = screen
        self.objects = objects
        self.objects = []
        self.Button_Play_again = Button(self.screen, 50, 650, 200, 50, "TRY AGAIN", self.Try_again, self.objects)
        font = pygame.font.Font(None, 60)
        text_1 = f"Highest point on the ark: {numpy.round(Y_Max, 2)}"
        text_2 = f"Highest displacement: {numpy.round(X_Max, 2)}"
        text_3 = f"Final displacement: {numpy.round(X_Final, 2)}"
        text_6 = f"Air Time: {numpy.round(air_time, 2)}"
        self.Text_1 = font.render(text_1, True, (0, 0, 0))
        self.Text_2 = font.render(text_2, True, (0, 0, 0))
        self.Text_3 = font.render(text_3, True, (0, 0, 0))
        self.Text_6 = font.render(text_6, True, (0, 0, 0))
        self.arc = pygame.image.load(igName)
        self.current_screen = "Final"
        self.input_box1 = TextBox(1250, 700, 140, 32, screen, None, 3, )
        self.inputBoxes = [self.input_box1]
        self.data_to_send = {"Y_max": numpy.round(Y_Max, 2),
                             "Air_Time": numpy.round(air_time, 2),
                             "X_Final": numpy.round(X_Final, 2),
                             "igName": igName
                             }

    def add_to_databece(self, text):
        pass

    def Try_again(self):
        self.current_screen = "Menu"

    def Display(self):
        self.screen.fill((34, 233, 111))
        self.screen.blit(self.Text_1, (50, 100))
        self.screen.blit(self.Text_2, (50, 200))
        self.screen.blit(self.Text_3, (50, 300))
        self.screen.blit(self.arc, (850, 50))
        self.screen.blit(self.Text_6, (50, 400))
        for object in self.objects:
            object.process()

        pygame.display.flip()


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]
