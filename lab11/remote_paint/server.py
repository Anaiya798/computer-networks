from base_object import PaintObject

import pygame
import socket


class PaintServer(PaintObject):
    def __init__(self, caption, host, port):
        super().__init__(caption)
        self.socket_init(host, port)

    def socket_init(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.settimeout(1)
        self.server_socket.bind((self.host, self.port))

    def receive_action(self):
        request, _ = self.server_socket.recvfrom(1024)
        request = request.decode().split()
        if request[0] == 'quit':
            return request, None
        else:
            length = len(request)
            action = request[:length - 4]
            draw_config = request[length - 4:]
            return action, draw_config

    def make_point(self, x, y, color, brush_thickness):
        pygame.draw.circle(self.window, color, (x, y), brush_thickness)

    def draw_line(self, x0, y0, x1, y1, color, brush_thickness):
        pygame.draw.line(self.window, color, (x0, y0), (x1, y1), brush_thickness + 1)

    def painting_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                break
        try:
            action, draw_config = self.receive_action()
        except socket.timeout:
            return

        if action[0] == 'quit':
            self.is_running = False

        if action[0] == 'point':
            x, y = map(int, action[1:])
            draw_config = list(map(int, draw_config))
            color = (draw_config[0], draw_config[1], draw_config[2])
            brush_thickness = draw_config[3]
            self.make_point(x, y, color, brush_thickness)

        if action[0] == 'line':
            x0, y0, x1, y1 = map(int, action[1:])
            draw_config = list(map(int, draw_config))
            color = (draw_config[0], draw_config[1], draw_config[2])
            brush_thickness = draw_config[3]
            self.draw_line(x0, y0, x1, y1, color, brush_thickness)


if __name__ == '__main__':
    PaintServer('Server', 'localhost', 8088).run()
