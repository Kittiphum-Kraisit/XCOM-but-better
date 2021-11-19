import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()


def blitRotate2(surf, images, top_left, angles):
    rotated_image = pygame.transform.rotate(images, angles)
    new_rect = rotated_image.get_rect(center=images.get_rect(topleft=top_left).center)
    surf.blit(rotated_image, new_rect.topleft)


image = pygame.image.load("pic/dice.png")
w, h = image.get_size()
start = False
angle = 0
done = True
start_time = pygame.time.get_ticks()
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            start = True

    pos = (screen.get_width() / 2, screen.get_height() / 2)
    elapsed = pygame.time.get_ticks() - start_time
    if elapsed <= 3000:
        screen.fill(0)
        pygame.draw.rect(screen, [255, 0, 0], pygame.Rect((120, 80), (50, 500)), 1)
        blitRotate2(screen, image, (175, 200), angle)
        angle += 1
        pygame.display.flip()
pygame.quit()
exit()
