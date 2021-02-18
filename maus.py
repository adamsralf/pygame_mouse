import pygame
from pygame.constants import (
    QUIT, K_ESCAPE, KEYDOWN, KEYUP, MOUSEBUTTONDOWN
)
import os


class Settings:
    """Container of project global settings.
    """
    window = {'width': 600, 'height': 600}
    path = {}
    path['file'] = os.path.dirname(os.path.abspath(__file__))
    path['image'] = os.path.join(path['file'], "images")
    inner_rect = pygame.Rect(
        100, 100, window['width'] - 200, window['height'] - 200)

    @staticmethod
    def get_dim():
        return (Settings.window['width'], Settings.window['height'])


class Ball(pygame.sprite.Sprite):
    """Simple ball sprite. 

    This class is derived from pygame.sprite.Sprite and
    its only purpose is to demonstrade the mouse interaction.
    """
    def __init__(self):
        """Constructor.

        There are 2 images: The originale image and the current image. 
        The current image is a scaled version of the original one. The scaling parameters
        are stored in self.scale.
        """
        super().__init__()
        fullfilename = os.path.join(Settings.path['image'], "blue2.png")
        self.image_orig = pygame.image.load(fullfilename).convert_alpha()
        self.image = pygame.transform.scale(self.image_orig, (10, 10))
        self.rect = self.image.get_rect()
        self.scale = {'width': self.rect.width, 'height': self.rect.height}

    def update(self):
        """Computes the new status of the ball.

        There are 2 requirements implemented: 
        To ensure that the ball doesn't leave the inner rectangle and 
        scaling the ball from the center and not from the left upper corner.
        """
        if self.rect.left < Settings.inner_rect.left:
            self.rect.left = Settings.inner_rect.left
        if self.rect.right > Settings.inner_rect.right:
            self.rect.right = Settings.inner_rect.right
        if self.rect.top < Settings.inner_rect.top:
            self.rect.top = Settings.inner_rect.top
        if self.rect.bottom > Settings.inner_rect.bottom:
            self.rect.bottom = Settings.inner_rect.bottom

        c = self.rect.center        # remember old center
        self.image = pygame.transform.scale(self.image_orig, (self.get_scale()))
        self.rect = self.image.get_rect()
        self.rect.center = c        # set center to old position

    def rotate_left(self):
        """Rotates the ball 90 degrees to the left.
        """
        self.image_orig = pygame.transform.rotate(self.image, 90)

    def rotate_right(self):
        """Rotates the ball 90 degrees to the right.
        """
        self.image_orig = pygame.transform.rotate(self.image, -90)

    def scale_up(self):
        """Increase the radius by one pixel.

        The diameter of the ball is limited by the width of the inner rectangle.
        """
        if self.rect.width < Settings.inner_rect.width:
            self.scale['width'] += 2
            self.scale['height'] += 2

    def scale_down(self):
        """Decrease the radius by one pixel.

        The diameter of the ball is limited by the 6.
        """
        if self.rect.width > 5:
            self.scale['width'] -= 2
            self.scale['height'] -= 2

    def get_scale(self):
        """Get the scale parameter as a tupel.

        Returns:
            (int, int): target width and target height of the ball.
        """
        return (self.scale['width'], self.scale['height'])

    def set_center(self, center):
        """Sets the center position of the ball.

        Args:
            center ((int, int)): centerx, centery
        """
        self.rect.centerx, self.rect.centery = center


if __name__ == '__main__':

    # Preparation
    os.environ['SDL_VIDEO_WINDOW_POS'] = "650, 70"

    #pylint: disable=no-member
    pygame.init()
    #pylint: enable=no-member
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(Settings.get_dim())
    ball = pygame.sprite.GroupSingle(Ball())

    running = True
    while running:
        clock.tick(60)
        ball.sprite.set_center(pygame.mouse.get_pos())  # this differs from the video solution
        pygame.mouse.set_visible(not Settings.inner_rect.collidepoint(ball.sprite.rect.center))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:               # left 
                    ball.sprite.rotate_left()
                elif event.button == 2:             # middle
                    running = False
                elif event.button == 3:             # right
                    ball.sprite.rotate_right()
                elif event.button == 4:             # scroll up
                    ball.sprite.scale_up()
                elif event.button == 5:             # scroll down
                    ball.sprite.scale_down()

        # update
        ball.update()

        # draw
        screen.fill((0, 0, 0))
        ball.draw(screen)
        pygame.display.flip()

    # bye bye
    #pylint: disable=no-member
    pygame.quit()
    #pylint: enable=no-member
