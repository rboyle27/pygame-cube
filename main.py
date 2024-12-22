import pygame
import numpy as np

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIDTH = 800
HEIGHT = 800

SCALE = 100
OFFSET = WIDTH // 2

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

projection_matrix = [[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 0]]

cube_points = [np.array([[-1], [-1], [-1]]),
               np.array([[ 1], [-1], [-1]]),
               np.array([[ 1], [ 1], [-1]]),
               np.array([[-1], [ 1], [-1]]),
               np.array([[-1], [-1], [ 1]]),
               np.array([[ 1], [-1], [ 1]]),
               np.array([[ 1], [ 1], [ 1]]),
               np.array([[-1], [ 1], [ 1]])]

projection_matrix = np.array(projection_matrix)

angle_x = 0
angle_y = 0
angle_z = 0

def connect(i: int, j: int, points: list):
    start = (points[i][0], points[i][1])
    end = (points[j][0], points[j][1])
    pygame.draw.line(window, WHITE, start, end)

while True:
    clock.tick(60)
    window.fill(BLACK)

    rotation_x = np.array([[1, 0, 0],
                           [0, np.cos(angle_x), -np.sin(angle_x)],
                           [0, np.sin(angle_x), np.cos(angle_x)]])
    rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                           [0, 1, 0],
                           [-np.sin(angle_y), 0, np.cos(angle_y)]])
    rotation_z = np.array([[np.cos(angle_z), -np.sin(angle_z), 0],
                           [np.sin(angle_z), np.cos(angle_z), 0],
                           [0, 0, 1]])

    points = [0 for e in range(len(cube_points))]
    i = 0

    for point in cube_points:
        rotate_x = rotation_x.dot(point)
        rotate_y = rotation_y.dot(rotate_x)
        rotate_z = rotation_z.dot(rotate_y)

        point_2d = projection_matrix.dot(rotate_z)
        x = (point_2d[0][0] * SCALE) + OFFSET
        y = (point_2d[1][0] * SCALE) + OFFSET

        points[i] = (x, y)
        i += 1

        pygame.draw.circle(window, RED, (x, y), 5)
    
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), # Front face
             (4, 5), (5, 6), (6, 7), (7, 4), # Back face
             (0, 4), (1, 5), (2, 6), (3, 7)] # Connections
    
    for edge in edges:
        connect(edge[0], edge[1], points)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        angle_x += 0.1
    if keys[pygame.K_a]:
        angle_y -= 0.1
    if keys[pygame.K_s]:
        angle_x -= 0.1
    if keys[pygame.K_d]:
        angle_y += 0.1

    pygame.display.update()