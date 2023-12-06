import pygame
import math
import time

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.orbit.clear()  # Clear any old points in the orbit list

    def draw_grid(win, width, height, scale, font):
        grid_color = (200, 200, 200)  # Light grey
        for x in range(0, width, scale):
            pygame.draw.line(win, grid_color, (x, 0), (x, height))
            if x != width // 2:
                label = font.render(f"{(x - width // 2) // scale}", 1, grid_color)
                win.blit(label, (x, height // 2))

        for y in range(0, height, scale):
            pygame.draw.line(win, grid_color, (0, y), (width, y))
            if y != height // 2:
                label = font.render(f"{(height // 2 - y) // scale}", 1, grid_color)
                win.blit(label, (width // 2, y))

    def is_mouse_over(self, mouse_x, mouse_y, width, height):
        planet_screen_x = self.x * self.SCALE + width // 2
        planet_screen_y = self.y * self.SCALE + height // 2
        distance = math.sqrt((mouse_x - planet_screen_x) ** 2 + (mouse_y - planet_screen_y) ** 2)
        return distance < self.radius

    def draw_trail(self, win, width, height, trail_fade_time=3):
        if len(self.orbit) > 2:
            trail_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            current_time = time.time()

            for i in range(len(self.orbit) - 1):
                point = self.orbit[i]
                next_point = self.orbit[i + 1]

                # Check if the points have the correct format
                if len(point) == 3 and len(next_point) == 3:
                    x_point, y_point, timestamp = point
                    next_x, next_y, _ = next_point

                    age = current_time - timestamp
                    alpha = max(255 * (1 - age / trail_fade_time), 0)
                    if alpha <= 0:
                        continue

                    pygame.draw.line(trail_surface, (*self.color, int(alpha)),
                                     (x_point * self.SCALE + width // 2, y_point * self.SCALE + height // 2),
                                     (next_x * self.SCALE + width // 2, next_y * self.SCALE + height // 2), 2)
                else:
                    # Skip this point if it does not have the correct format
                    continue

            win.blit(trail_surface, (0, 0))

    def draw(self, win, width, height, font, color):
        # First draw the trail
        self.draw_trail(win, width, height)

        # Then draw the planet
        x = self.x * self.SCALE + width // 2
        y = self.y * self.SCALE + height // 2
        pygame.draw.circle(win, self.color, (x, y), self.radius)

        # Display distance in kilometers without decimals (if not the sun)
        if not self.sun:
            distance_km = int(self.distance_to_sun / 1000)
            distance_text = font.render(f"{distance_km} km", 1, color)
            text_x = x - distance_text.get_width() // 2
            text_y = y + self.radius  # Position the text below the planet
            win.blit(distance_text, (text_x, text_y))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue  # Skip self in gravity calculation

            fx, fy = self.attraction(planet)  # Calculate gravitational force
            total_fx += fx
            total_fy += fy

        # Update velocity based on the total force exerted
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update position based on the new velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        # Append new position with current time to the orbit list
        current_time = time.time()
        self.orbit.append((self.x, self.y, current_time))

def draw_back_button(win, font):
    button_rect = pygame.Rect(10, 50, 50, 30)
    pygame.draw.rect(win, (255,255,255), button_rect)
    back_text = font.render("Back", 1, (0, 0, 0))
    win.blit(back_text, (15, 55))
    return button_rect

def run_pygame_simulation():
    pygame.init()
    WIDTH, HEIGHT = 800, 800
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Planet Simulation")

    # Define colors and font
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLUE = (100, 149, 237)
    RED = (188, 39, 50)
    DARK_GREY = (80, 78, 81)
    FONT = pygame.font.SysFont("comicsans", 16)

    # Create planets
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30, "Sun")
    sun.sun = True
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10 ** 24, "Earth")
    earth.y_vel = 29.783 * 1000
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23, "Mars")
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10 ** 23, "Mercury")
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10 ** 24, "Venus")
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    run = True
    clock = pygame.time.Clock()

    speeds = [0.5,2.5,0.01]  # Different speeds
    current_speed_index = 0
    update_counter = 0  # Counter to manage update frequency

    def draw_speed_button():
        button_rect = pygame.Rect(10, 10, 100, 30)
        pygame.draw.rect(WIN, WHITE, button_rect)
        speed_text = FONT.render(f"Speed: {speeds[current_speed_index]}", 1, (0, 0, 0))
        WIN.blit(speed_text, (15, 15))
        return button_rect

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        speed_button_rect = draw_speed_button()
        back_button_rect = draw_back_button(WIN, FONT)  # Draw the back button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if speed_button_rect.collidepoint(event.pos):
                    current_speed_index = (current_speed_index + 1) % len(speeds)
                elif back_button_rect.collidepoint(event.pos):
                    # Perform action when back button is clicked
                    print("Back button clicked")
                    run = False  # For example, exiting the simulation

        update_counter += 1

        if update_counter >= (1 / speeds[current_speed_index]):
            for planet in planets:
                planet.update_position(planets)
            update_counter = 0

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for planet in planets:
            planet.draw(WIN, WIDTH, HEIGHT, FONT, WHITE)
            if planet.is_mouse_over(mouse_x, mouse_y, WIDTH, HEIGHT):
                formatted_mass = "{:.2e}".format(planet.mass)
                info_text = FONT.render(f"{planet.name}: Mass = {formatted_mass} kg", 1, WHITE)
                WIN.blit(info_text, (mouse_x, mouse_y - 20))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run_pygame_simulation()
