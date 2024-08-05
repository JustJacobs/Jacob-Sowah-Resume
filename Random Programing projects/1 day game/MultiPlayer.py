import Classes
import json
import pygame
import socket
import threading

"""
this  class is just the screen that asks you if
you want to join or host
"""


class MultiPlayer_Menu:
    def __init__(self, screen, objects):
        self.objects = objects
        self.current_screen = "Multiplayer"
        self.Button_Host = Classes.Button(screen, 50, 50, 400, 400, "Host", self.Host, self.objects)
        self.Name_box = Classes.TextBox(1000, 100, 100, 30, screen, self.Join, 3, )
        self.screen = screen
        self.Name = None
        self.inputbox = [self.Name_box]

    def Join(self):
        if len(self.Name_box.get_text()) > 0:
            self.Name = self.Name_box.get_text()
            self.current_screen = "Join"

    def Host(self):
        self.current_screen = "Host"
        self.objects = []

    def display(self):
        font = pygame.font.Font(None, 60)
        self.screen.blit(font.render("Type in name and hit enter to Join ", True, (0, 0, 0)), (800, 50))

        for object in self.objects:
            object.process()

        pygame.display.flip()


"""this class is realy thoe only class that has functions
and rescve from the server. This class is inherated by the next 2 classes"""


class Client:
    def __init__(self, host, port, current_screen):
        self.objects = []
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.conected = False
        self.current_screen = current_screen

    def send_message(self, message):
        self.socket.sendall(json.dumps(message).encode())

    def receive_message(self):
        data = self.socket.recv(1024)
        return json.loads(data.decode())

    def close(self):
        self.socket.close()


"""
This class inherets from the Client class and is like
the main screen that all the clients look at when checing if 
they are in the top 6
"""


class Host(Client):
    def __init__(self, host, port, screen, current_screen):
        super().__init__(host, port, current_screen)
        self.objects.clear()
        self.screen = screen
        self.joined_clients = []
        self.current_screen = "Host"
        self.Button_Start = Classes.Button(self.screen, 50, 700, 100, 50, "Start", self.start, self.objects)
        self.receive_thread = threading.Thread(target=self.receive_from_server, daemon=True)
        self.receive_thread.start()
        self.send_message({"command": "Host", "info": "test"})
        self.Names = []
        self.V_start = False
        self.unsorted = []
        self.sorted_Y_Max, self.sorted_X_Max, self.sorted_X_Final = [], [], []

    def start(self):
        self.send_message({"command": "Start"})
        self.V_start = True

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.receive_thread.start()
        self.send_message({"command": "Host"})

    def add_joined_client(self, client):
        self.joined_clients.append(client)

    def get_joined_clients(self):
        return self.joined_clients

    def receive_from_server(self):
        while True:
            try:
                data = self.receive_message()

                if not data:
                    break

                print(f"Received data: {data}")
                if data.get("command") == "name":
                    self.Names.append(data.get("info"))
                if data.get("command") == "Finished":
                    self.unsorted.append(data)
                    print(self.unsorted)
                    self.V_start = True




            # Handle incoming data here based on the specific client type
            except Exception as e:
                print(f"Error: {e}")
                break

    def sort_data(self, data):
        sorted_lists = {"Y_max": [], "Air_Time": [], "X_Final": []}
        sorted_Y_max = []
        sorted_Air_Time = []
        sorted_X_Final = []
        for d in data:
            for key, value in d.items():
                if key == "Y_max":
                    sorted_lists["Y_max"].append((d["Name"], d["igName"], value))
                elif key == "Air_Time":
                    sorted_lists["Air_Time"].append((d["Name"], d["igName"], value))
                elif key == "X_Final":
                    sorted_lists["X_Final"].append((d["Name"], d["igName"], value))
        for key, value in sorted_lists.items():
            for item in value:
                if key == "Y_max":
                    sorted_Y_max.append(item)
                if key == "Air_Time":
                    sorted_Air_Time.append(item)
                if key == "X_Final":
                    sorted_X_Final.append(item)
        print(sorted(sorted_Y_max, key=lambda x: x[2])[::-1])
        print(sorted(sorted_Air_Time, key=lambda x: x[2])[::-1])
        print(sorted(sorted_X_Final, key=lambda x: x[2])[::-1])
        return sorted(sorted_Y_max, key=lambda x: x[2])[::-1], sorted(sorted_Air_Time, key=lambda x: x[2])[
                                                               ::-1], sorted(sorted_X_Final, key=lambda x: x[2])[::-1]

    def display(self):
        self.screen.fill((34, 233, 111))

        font = pygame.font.Font(None, 60)
        list_of_names = []
        for Joined in self.Names:
            list_of_names.append(font.render(Joined, True, (0, 0, 0)))
        if not self.V_start:
            if len(self.Names) == 0:
                pass
            elif len(self.Names) == 1:
                self.screen.blit(list_of_names[0], (100, 100))
            elif len(self.Names) == 2:
                self.screen.blit(list_of_names[0], (100, 100))
                self.screen.blit(list_of_names[1], (100, 200))
            elif len(self.Names) == 3:
                self.screen.blit(list_of_names[0], (100, 100))
                self.screen.blit(list_of_names[1], (100, 200))
                self.screen.blit(list_of_names[2], (100, 300))
            elif len(self.Names) == 4:
                self.screen.blit(list_of_names[0], (100, 100))
                self.screen.blit(list_of_names[1], (100, 200))
                self.screen.blit(list_of_names[2], (100, 300))
                self.screen.blit(list_of_names[3], (100, 400))
        else:
            self.objects = []
            if len(self.unsorted) > len(self.sorted_Y_Max):
                self.sorted_Y_Max, self.sorted_X_Max, self.sorted_X_Final = self.sort_data(self.unsorted)
            for x in range(len(self.sorted_Y_Max)):
                self.screen.blit(font.render("highest Y Value ", True, (0, 0, 0)), (10, 450))
                self.screen.blit(font.render("Most air time ", True, (0, 0, 0)), (510, 450))
                self.screen.blit(font.render("Highest final x value ", True, (0, 0, 0)), (1010, 450))
                self.screen.blit(
                    font.render(f"{self.sorted_Y_Max[x][0]}      {self.sorted_Y_Max[x][2]}", True, (0, 0, 0)),
                    (10, 500 + (x * 50)))
                self.screen.blit(
                    font.render(f"{self.sorted_X_Max[x][0]}      {self.sorted_X_Max[x][2]}", True, (0, 0, 0)),
                    (510, 500 + (x * 50)))
                self.screen.blit(
                    font.render(f"{self.sorted_X_Final[x][0]}      {self.sorted_X_Final[x][2]}", True, (0, 0, 0)),
                    (1010, 500 + (x * 50)))

                self.screen.blit(pygame.image.load(self.sorted_Y_Max[0][1]), (10, 10))
                self.screen.blit(pygame.image.load(self.sorted_X_Max[0][1]), (510, 10))
                self.screen.blit(pygame.image.load(self.sorted_X_Final[0][1]), (1010, 10))
        for object in self.objects:
            object.process()
        pygame.display.flip()


"""
This class also inherets from the Client class and 
is how the players tall to the Server.
"""


class Join(Client):
    def __init__(self, host, port, user_info, screen, current_screen, ):
        super().__init__(host, port, current_screen)
        self.user_info = user_info
        self.receive_thread = threading.Thread(target=self.receive_from_server, daemon=True)
        self.receive_thread.start()
        self.screen = screen
        self.send_message({"command": "Join",
                           "info": self.user_info})
        self.current_screen = "Join"
        self.data_to_send = None
        self.sent = False

    def set_data(self, data):
        self.data_to_send = data
        print(1)

    def set_current_screen(self, data):
        self.current_screen = data

    def connect(self):
        self.socket.connect((self.host, self.port))
        self.receive_thread.start()
        self.send_message({"command": "Join",
                           "info": self.user_info})

    def receive_from_server(self):
        while True:
            try:
                data = self.receive_message()
                print(f"Received data: {data}")
                # Handle incoming data here based on the specific client type
                if data.get("command") == "start":
                    self.start()
            except Exception as e:
                print(f"Error: {e}")

                break

    def start(self):
        self.current_screen = "Draw"

    def display(self):
        font = pygame.font.Font(None, 60)
        if self.data_to_send == None:
            self.screen.blit(font.render(f"look for your name:{self.user_info} on the screen", True, (0, 0, 0)),
                             (50, 50))
        else:
            if not self.sent:
                self.data_to_send["Name"] = self.user_info
                self.data_to_send["command"] = "Finished"
                self.send_message(self.data_to_send)
                self.sent = True
            self.screen.blit(
                font.render(f"look for your name:{self.user_info} and score on the screen", True, (0, 0, 0)),
                (50, 50))
