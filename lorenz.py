import pygame

class Lorenz():
    def __init__(self, init_x, init_y, init_z, color):
        self.x_min, self.x_max = -25, 25
        self.y_min, self.y_max = -40, 40
        self.z_min, self.z_max = 0, 50

        # Lorenz attractor "evolution parameters"
        self.A = 10
        self.B = 28
        self.C = 7 / 3

        self.x = init_x
        self.y = init_y
        self.z = init_z

        self.x_prev = self.x
        self.y_prev = self.y
        self.z_prev = self.z

        self.dt = 0.003

        self.pixel_color = color

    def step(self):
        self.x_prev = self.x
        self.y_prev = self.y
        self.z_prev = self.z
        
        self.x += self.A * (self.y_prev - self.x_prev) * self.dt
        self.y += (self.x_prev * (self.B - self.z_prev) - self.y_prev) * self.dt
        self.z += (self.x_prev * self.y_prev - self.C * self.z_prev) * self.dt

    def draw(self, display_surface):
        width, height = display_surface.get_size()
        
        prev_pos = self.to_screen_coords(
            self.x_prev, self.y_prev,
            self.x_min, self.x_max,
            self.y_min, self.y_max,
            width, height
        )
        new_pos = self.to_screen_coords(
            self.x, self.y,
            self.x_min, self.x_max,
            self.y_min, self.y_max,
            width, height
        )

        new_rect = pygame.draw.line(
            display_surface, self.pixel_color, prev_pos, new_pos, 1
        )

        return new_rect

    def to_screen_coords(self, x, y, x_min, x_max, y_min, y_max, width, height):
        screen_x = width * ((x - x_min) / (x_max - x_min))
        screen_y = height * ((y - y_min) / (y_max - y_min))

        return round(screen_x), round(screen_y)


class Application():
    def __init__(self, inital_conditions):
        self.is_running = True
        self.display_surface = None
        self.fps_clock = None
        self.attractors = []
        self.inital_condititions = inital_conditions
        # TODO: make this compatible with any monitor size
        self.size = self.width, self.height = 1440, 850
        self.count = 0
        self.output_count = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorentz Attractor")
        self.display_surface = pygame.display.set_mode(self.size)
        self.is_running = True
        self.fps_clock = pygame.time.Clock()

        for cond in self.inital_condititions:
            new_attractor = Lorenz(*cond)
            self.attractors.append(new_attractor)

    def on_event(self, event):
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            self.is_running = False

    def on_loop(self):
        for a in self.attractors:
            a.step()

    def on_render(self):
        new_rects = []
        for a in self.attractors:
            rect = a.draw(self.display_surface)
            new_rects.append(rect)

        pygame.display.update(new_rects)

    def on_execute(self):
        if self.on_init() == False:
            self.is_running = False

        while self.is_running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            self.fps_clock.tick()
            self.count += 1

        pygame.quit()

# TODO: CLI that lets users specify # of attractors and initial conditions
if __name__ == "__main__":
    orange = (255, 165, 0)
    blue = (5, 5, 255)

    a1 = (0.10, 0.0, 0.0, orange)
    a2 = (0.11, 0.0, 0.0, blue)

    app = Application((a1, a2))
    app.on_execute()