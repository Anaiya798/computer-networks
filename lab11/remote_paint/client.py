from base_object import PaintObject

import pygame
import socket


class PaintClient(PaintObject):

    def __init__(self, caption, host, port, timeout):
        super().__init__(caption)
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket_init()
        self.draw_config()

    def socket_init(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket.settimeout(self.timeout)

    def draw_config(self):
        self.color = (0, 0, 0)
        self.brush_thickness = 1
        self.last_point = None
        self.mouse_pressed = False

    def send_action(self, action):
        try:
            self.client_socket.sendto(action.encode(), (self.host, self.port))
        except socket.gaierror:
            print('Invalid server address')
            pygame.quit()
            return

    def make_point(self, x, y):
        if self.last_point is None:
            pygame.draw.circle(self.window, self.color, (x, y), self.brush_thickness)
            self.send_action(f'point {x} {y} {self.color[0]} {self.color[1]} {self.color[2]} {self.brush_thickness}')
        else:
            pygame.draw.line(self.window, self.color, self.last_point, (x, y), self.brush_thickness + 1)
            self.send_action(
                f'line {self.last_point[0]} {self.last_point[1]} {x} {y} {self.color[0]} {self.color[1]} {self.color[2]} '
                f'{self.brush_thickness}')
        self.last_point = (x, y)

    def painting_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                self.send_action('quit')
                break

            if event.type == pygame.MOUSEBUTTONUP:
                self.last_point = None
                self.mouse_pressed = False

            if event.type == pygame.MOUSEMOTION and self.mouse_pressed:
                x, y = pygame.mouse.get_pos()
                self.make_point(x, y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                x, y = pygame.mouse.get_pos()
                self.make_point(x, y)


if __name__ == '__main__':
    PaintClient('Client', 'localhost', 8088, 1).run()
