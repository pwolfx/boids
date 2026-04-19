import pygame
import random

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 77
BACKGROUND_COLOR = (255, 0, 255)
BOID_COLOR = (25, 225, 225)
BOID_SIZE = 5
NEARBY_RADIUS = 50
COHESION_WEIGHT = 0.01
SEPARATION_WEIGHT = 1
ALIGNMENT_WEIGHT = 0.01
MAX_VELOCITY = 2

class Boid:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

    def update(self, flock):
        # TODO: separation, alignment, cohesion
        sx, sy = self.separation(flock)
        self.vx += (sx * SEPARATION_WEIGHT)
        self.vy += (sy * SEPARATION_WEIGHT)

        ax, ay = self.alignment(flock)
        self.vx += (ax * ALIGNMENT_WEIGHT)
        self.vy += (ay * ALIGNMENT_WEIGHT)

        cx, cy = self.cohesion(flock)
        self.vx += (cx * COHESION_WEIGHT)
        self.vy += (cy * COHESION_WEIGHT)

        # cap velocity to max
        velocitysq = self.vx**2 + self.vy**2
        maxvelsq = MAX_VELOCITY**2
        if velocitysq > maxvelsq and velocitysq > 0:
            scale = maxvelsq / velocitysq
            self.vx *= scale
            self.vy *= scale

        self.x += self.vx
        self.y += self.vy
        # wrap around screen edges
        self.x %= WIDTH
        self.y %= HEIGHT

    def draw(self, screen):
        pygame.draw.circle(screen, BOID_COLOR, (int(self.x), int(self.y)), BOID_SIZE)

    def separation(self, flock):
        # each boid steers away from its neighbors that are too close. "Don't crash into anyone."
        count = 0
        sx, sy = 0, 0
        for neighbor in self.nearby(flock):
            count += 1
            distance = (neighbor.x - self.x)**2 + (neighbor.y - self.y)**2
            weight = 1
            if distance != 0:
                weight = 1 / distance
            sx -= weight * (neighbor.x - self.x)
            sy -= weight * (neighbor.y - self.y)

        if count == 0:
            return 0, 0

        return sx, sy

    def cohesion(self, flock):
        # each boid steers toward the average position of its neighbors. "Move toward the crowd." 

        # get the locations of nearby boids
        count = 0
        cx, cy = 0, 0
        for neighbor in self.nearby(flock):
            count += 1
            cx += neighbor.x
            cy += neighbor.y

        # special case; poor boid has no neighbors
        if count == 0:
            return 0, 0
        
        # compute average location of neighbors
        cx /= count
        cy /= count

        # compute average neighbors' location in relation to self
        cx -= self.x
        cy -= self.y
        return cx, cy

    def alignment(self, flock):
        # each boid steers toward the average velocity of its neighbors. "Fly where the crowd is flying."
        count = 0
        ax, ay = 0, 0
        for neighbor in self.nearby(flock):
            count += 1
            ax += neighbor.vx
            ay += neighbor.vy

        # special case; poor boid has no neighbors
        if count == 0:
            return 0, 0
        
        ax /= count
        ay /= count

        ax -= self.vx
        ay -= self.vy
        return ax, ay

    def nearby(self, flock):
        return [b for b in flock if b is not self and ((self.x - b.x)**2 + (self.y - b.y)**2 < NEARBY_RADIUS**2)]



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boids")
    clock = pygame.time.Clock()

    boids = [Boid() for _ in range(NUM_BOIDS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(BACKGROUND_COLOR)

        for boid in boids:
            boid.update(boids)
            boid.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()