import Classes
import MultiPlayer
import pygame
import sys

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1500, 800
screen = pygame.display.set_mode((width, height))
multiplayer = MultiPlayer.MultiPlayer_Menu(screen, [])
font = pygame.font.SysFont('Arial', 40)
TextBoxes = []
data_to_send = None
onlile_Mode = False


def start():
    main_menu = Classes.Menu(screen, [])
    Canvas = Classes.Drawing(screen, [])

    current_screen = "Menu"
    return main_menu, Canvas, current_screen


main_menu, Canvas, current_screen = start()
"""
This entire while loop is the mai gameplay loop,
everytime a classes display function is used it 
check what that same function's current_screen is.
if it is different it will change the main current
screen to that current screen unless it on line where
it differs slightly.
"""
run = True
while True:

    screen.fill((0, 255, 111))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if len(TextBoxes) != 0:
            for box in TextBoxes:
                box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            if current_screen == "Draw":
                if Canvas.Final_Object == None:
                    if Canvas.start == None:
                        Canvas.process_click_Down(event)
                    if Canvas.start != None:
                        Canvas.process_click_UP(event)

    if len(TextBoxes) != 0:
        for box in TextBoxes:
            box.update()
            box.draw()

    if current_screen == "Menu":
        main_menu.display()
        if main_menu.current_screen != "Menu":
            current_screen = main_menu.current_screen
    elif current_screen == "Multiplayer":
        multiplayer.display()
        TextBoxes = multiplayer.inputbox
        if multiplayer.current_screen != "Multiplayer":
            current_screen = multiplayer.current_screen
            if current_screen == "Host":
                Client = MultiPlayer.Host('127.0.0.1', 5050, screen, current_screen)
            elif current_screen == "Join":
                Client = MultiPlayer.Join('127.0.0.1', 5050, multiplayer.Name_box.get_text(), screen, current_screen, )
            TextBoxes = []
            onlile_Mode = True
    elif current_screen == "Host":
        Client.display()
        if Client.current_screen != "Host":
            current_screen = Client.current_screen
    elif current_screen == "Join":
        Client.display()

        if data_to_send != None:
            Client.set_data(data_to_send)
            Client.set_current_screen("Join")
            data_to_send = None
        if Client.current_screen != "Join":
            current_screen = Client.current_screen

    elif current_screen == "Draw":
        Canvas.Display()
        if Canvas.current_screen != "Draw":
            current_screen = Canvas.current_screen
            Final_object = Classes.Combined(Canvas.shapes, Canvas.depth, Canvas.dencity, Canvas.angle, Canvas.v0)

            Show_Arc = Classes.Display(screen, Canvas.shapes, Final_object.coords)
    elif current_screen == "Dis":
        Show_Arc.Display()
        if Show_Arc.current_screen != "Dis":
            current_screen = Show_Arc.current_screen
            Final_screen = Classes.Final_screen(screen, Canvas.objects, Final_object.Y_Max, Final_object.X_Max,
                                                Final_object.X_Final, Final_object.airtime, Final_object.igname)
    elif current_screen == "Final":
        Final_screen.Display()
        TextBoxes = Final_screen.inputBoxes

        if Final_screen.current_screen != "Final":
            if onlile_Mode:
                data_to_send = Final_screen.data_to_send
                current_screen = "Join"
                TextBoxes = []

            else:
                current_screen = Final_screen.current_screen
                main_menu.current_screen = "Menu"
                Canvas.current_screen = "Draw"
                Show_Arc.current_screen = "Dis"
                main_menu, Canvas, current_screen = start()
                TextBoxes = []


    else:
        pass

    pygame.display.flip()
    fpsClock.tick(fps)
