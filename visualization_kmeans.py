import pygame
from random import randint
import math
from sklearn.cluster import KMeans


def distance(p1,p2):
	return math.sqrt((p1[0]-p2[0]) * (p1[0]-p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("kmeans visualization")

running = True

clock = pygame.time.Clock()

BLACK = (0,0,0) 
BLACK_1 = (26, 26, 26)
WHITE = (230, 230, 230)
WHITE_1 = (204, 204, 204)
BACKGROUND = (214, 214, 214)
BACKGROUND_PANEL = (26, 26, 26)
RED = (255, 77, 77)
GREY = (77, 77, 77)
GREY_1 =(51, 51, 51)
GREY_2 = (128, 128, 128)
GREEN = (0, 153, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]

font = pygame.font.SysFont('sans', 30)
font_small = pygame.font.SysFont('sans', 15, 2)
font_mouse = pygame.font.SysFont('arial', 14, 1)
font_error = pygame.font.SysFont('arial', 20, 1)

text_plus = font.render('+', True, WHITE)
text_minus = font.render('-', True, WHITE)
text_run = font_small.render('RUN', True, WHITE)
text_random = font_small.render('RANDOM', True, WHITE)
text_algorithm = font_small.render('ALGORITHM', True, WHITE)
text_reset = font_small.render('RESET', True, WHITE)

K = 0
Error = 0
points = []
clusters = []
labels = []

while running:
    clock.tick(60)
    screen.fill(BACKGROUND)
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Start draw interface ---------------------

    # Draw background
    pygame.draw.rect(screen, GREY_1, (0, 0, WIDTH, HEIGHT))

    # Draw panel
    pygame.draw.rect(screen, BACKGROUND_PANEL, (10, 10, 980, 500))
    pygame.draw.rect(screen, GREY_2, (10, 10, 980, 500), 3)

    # K button - 
    pygame.draw.rect(screen, GREY, (40, 550, 25, 25))
    pygame.draw.rect(screen, GREY_2, (40, 550, 25, 25), 1)
    screen.blit(text_minus, (49, 542))

    # K value
    pygame.draw.rect(screen, BLACK_1, (65, 550, 85, 25))
    pygame.draw.rect(screen, GREY_2, (65, 550, 85, 25), 1)
    text_K = font_small.render(f'K  =  {K}', True, RED)
    screen.blit(text_K, (90, 553))

    # K button +
    pygame.draw.rect(screen, GREY, (150, 550, 25, 25))
    pygame.draw.rect(screen, GREY_2, (150, 550, 25, 25), 1)
    screen.blit(text_plus, (155, 543))

    # Run button
    pygame.draw.rect(screen, GREY, (210, 540, 60, 35))
    pygame.draw.rect(screen, GREY_2, (210, 540, 60, 35) , 2)
    screen.blit(text_run, (224, 548))

    # Random button
    pygame.draw.rect(screen, GREY, (300, 540, 100, 35))
    pygame.draw.rect(screen, GREY_2, (300, 540, 100, 35) , 2)
    screen.blit(text_random, (317, 548))

    # Error text
    pygame.draw.rect(screen, BLACK_1, (475, 532, 150, 50))
    pygame.draw.rect(screen, GREY_2, (475, 532, 150, 50), 1)
    text_Error = font_error.render(f'ERROR = {int(Error)}', True, RED)
    screen.blit(text_Error, (550 - text_Error.get_width()/2, 548))

    # Algorith button
    pygame.draw.rect(screen, GREY, (700, 540, 120, 35))
    pygame.draw.rect(screen, GREY_2, (700, 540, 120, 35) , 2)
    screen.blit(text_algorithm, (715, 548))

    # Reset button
    pygame.draw.rect(screen, GREY, (860, 540, 80, 35))
    pygame.draw.rect(screen, GREY_2, (860, 540, 80, 35) , 2)
    screen.blit(text_reset, (878, 548))

    # Draw mouse position when mouse is in panel
    if 10 < mouse_x < 990 and 10 < mouse_y < 510:
        text_coordinates = font_mouse.render(f'{mouse_x - 10, mouse_y - 10}', True, GREEN)
        screen.blit(text_coordinates, (mouse_x +10, mouse_y -10))

    # Draw points
    for i in range(len(points)):	
        pygame.draw.circle(screen, GREEN, (points[i][0] + 10, points[i][1] + 10), 4, 1)

        if labels:
            pygame.draw.circle(screen, COLORS[labels[i]], (points[i][0] + 10, points[i][1] + 10), 4)

    # Draw cluster
    for i in range(len(clusters)):
        x = int(clusters[i][0]) + 10
        y = int(clusters[i][1]) + 10
        pygame.draw.circle(screen, COLORS[i], (x, y), 7)
        
    # Calculate and Draw Error
    Error = 0
    if clusters != [] and labels != []:
        for i in range(len(points)):
            Error += distance(points[i], clusters[labels[i]])**2

    # Draw hiệu ứng chạm vào
    # K - button
    if 40 < mouse_x < 65 and 550 < mouse_y < 575:
        pygame.draw.rect(screen, RED, (40, 550, 25, 25))
        screen.blit(text_minus, (49, 542))
    # K + button
    if 150 < mouse_x < 175 and 550 < mouse_y < 575:
        pygame.draw.rect(screen, RED, (150, 550, 25, 25))
        screen.blit(text_plus, (155, 543))
    # Run button
    if 210 < mouse_x < 270 and 540 < mouse_y < 575:
        pygame.draw.rect(screen, RED, (210, 540, 60, 35))
        screen.blit(text_run, (224, 548))
    # Random button
    if 300 < mouse_x < 400 and 540 < mouse_y < 575:
        pygame.draw.rect(screen, RED, (300, 540, 100, 35))
        screen.blit(text_random, (317, 548))
    # Algorith button
    if 700 < mouse_x < 820 and 540 < mouse_y < 575:
        pygame.draw.rect(screen, RED, (700, 540, 120, 35))
        screen.blit(text_algorithm, (715, 548))
    # Reset button
    if 860 < mouse_x < 940 and 540 < mouse_y < 575:
        pygame.draw.rect(screen, RED, (860, 540, 80, 35))
        screen.blit(text_reset, (878, 548))


    # End draw interface -----------------------------


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Create point on panel
            if 10 < mouse_x < 990 and 10 < mouse_y < 510:
                labels = []
                points.append((mouse_x -10, mouse_y - 10))

            # Change K button -
            if 40 < mouse_x < 65 and 550 < mouse_y < 575:
                pygame.draw.rect(screen, WHITE, (40, 550, 25, 25))
                if K > 0:
                    K -= 1

            # Change K button +
            if 150 < mouse_x < 175 and 550 < mouse_y < 575:
                pygame.draw.rect(screen, WHITE, (150, 550, 25, 25))
                if K < len(COLORS):
                    K += 1

            # Run button
            if 210 < mouse_x < 270 and 540 < mouse_y < 575:
                pygame.draw.rect(screen, WHITE, (210, 540, 60, 35))
                labels = []
                if clusters == []:
                    continue
                # Assign points to closest clusters
                for p in points:
                    distances_to_cluster = []
                    for c in clusters:
                        dis = distance(p, c)
                        distances_to_cluster.append(dis)
                    min_distance = min(distances_to_cluster)
                    label = distances_to_cluster.index(min_distance)
                    labels.append(label)
                
                # Update clusters
                for i in range(K):
                    sum_x = 0
                    sum_y = 0
                    count = 0
                    for j in range(len(points)):
                        if labels[j] == i:
                            sum_x += points[j][0]
                            sum_y += points[j][1]
                            count += 1
                    if count > 0:
                        new_cluster_x = sum_x / count
                        new_cluster_y = sum_y / count
                        clusters[i] = (new_cluster_x, new_cluster_y)

            # Random button
            if 300 < mouse_x < 400 and 540 < mouse_y < 575:
                pygame.draw.rect(screen, WHITE, (300, 540, 100, 35))
                labels = []
                clusters = []
                for i in range(K):
                    clusters.append((randint(0, 970), randint(0, 490)))

            # Algorithm button
            if 700 < mouse_x < 820 and 540 < mouse_y < 575:
                pygame.draw.rect(screen, WHITE, (700, 540, 120, 35))
                try:
                    kmeans = KMeans(n_clusters= K).fit(points)
                    labels = list(kmeans.labels_)
                    clusters = list(kmeans.cluster_centers_)
                except:
                    print("Error")
            # Reset button
            if 860 < mouse_x < 940 and 540 < mouse_y < 575:
                pygame.draw.rect(screen, WHITE, (860, 540, 80, 35))
                K = 0
                Error = 0
                points = []
                clusters = []
                lables = []
            
    pygame.display.flip()

pygame.quit()