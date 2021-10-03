import pygame
import pygame.font

class Lorenz():
    def __init__(self, init_x, init_y, init_z, color, dt):
        self.x_min, self.x_max = -30, 30
        self.y_min, self.y_max = -30, 30
        self.z_min, self.z_max = -50, 50

        # Lorenz attractor "evolution parameters"
        self.A = 10
        self.B = 28
        self.C = 8 / 3

        self.x = init_x
        self.y = init_y
        self.z = init_z

        self.x_prev = self.x
        self.y_prev = self.y
        self.z_prev = self.z

        self.dt = dt

        self.pixel_color = color

    def step(self):
        self.x_prev = self.x
        self.y_prev = self.y
        self.z_prev = self.z
        
        self.x += self.A * (self.y_prev - self.x_prev) * self.dt
        self.y += (self.x_prev * (self.B - self.z_prev) - self.y_prev) * self.dt
        self.z += (self.x_prev * self.y_prev - self.C * self.z_prev) * self.dt

    def draw(self, display_surface, display_padding):
        width, height = display_surface.get_size()
        width *= 1 - display_padding
        height *= 1 - display_padding
        
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
        self.display_padding = 0.1
        self.fps_clock = None
        self.attractors = []
        self.inital_condititions = inital_conditions
        self.count = 0
        self.output_count = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorentz Attractor")
        # surface will have the same size as the current screen resolution
        self.display_surface = pygame.display.set_mode((0, 0))
        self.is_running = True
        self.fps_clock = pygame.time.Clock()

        # TODO: Configure help message
        # if pygame.font:
        #     font = pygame.font.Font(None, 12)
        #     text = font.render("Press any key to quit.", False, (200, 200, 200))
        #     self.display_surface.blit(text,(100,100))

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
            rect = a.draw(self.display_surface, self.display_padding)
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

def collect_inital_conds():
    ORANGE = (255, 165, 0)
    BLUE = (5, 5, 255)
    GREEN = (5, 255, 5)
    RED = (255, 5, 5)
    GREY = (120, 120, 120)
    colors = [ORANGE, BLUE, GREEN, RED, GREY]

    SLOW = 0.0025
    MEDIUM = 0.005
    FAST = 0.01
    speeds = [SLOW, MEDIUM, FAST]

    num_attractors = None
    print('')
    while True:
        inp = input(
            "How many attractors would you like to animate [1 - 5]? "
        )
        if inp == 'q' or inp == 'Q':
            return None

        try:
            num_attractors = int(inp)
        except:
            print("Please enter a number between 1 and 5", "\n")
            continue

        if num_attractors not in range(1, 5):
            print("Please enter a number between 1 and 5", "\n")
            continue

        break

    speed_choice = None
    while True:
        speed_in = input(
            "How fast would you like the animation to evolve [slow|medium|fast]? "
        )
        if speed_in == 'q' or speed_in == 'Q':
            return None

        if speed_in not in ['slow', 'medium', 'fast']:
            print("Please enter a valid choice.")
            continue

        speed_choice = speeds[['slow', 'medium', 'fast'].index(speed_in)]

        break

    initial_conds = []
    for i in range(num_attractors):
        print("")
        print(f"Attractor #{i+1}")
        print("=================")

        x_init = ['Initial x coordinate [-1.0 - +1.0]? ', None]
        y_init = ['Initial y coordinate [-1.0 - +1.0]? ', None]
        z_init = ['Initial z coordinate [-1.0 - +1.0]? ', None]
        for coord in [x_init, y_init, z_init]:
            while True:
                inp = input(f"{coord[0]}")
                if inp == 'q' or inp == 'Q':
                    return None

                try:
                    coord[1] = float(inp)
                except:
                    print("Please enter a value between -1.0 and +1.0")
                    continue

                if coord[1] < -1.0 or 1.0 < coord[1]:
                    print("Please enter a value between -1.0 and +1.0")
                    continue

                break

        initial_conds.append(
            (x_init[1], y_init[1], z_init[1], colors[i], speed_choice)
        )


    return initial_conds

def print_welcome_message():
    header = "\n===== LORENZ ATTRACTOR ANIMATOR =====\n\n"

    welcome =  "Welcome! Follow the instructions below to get started,\n"
    welcome += "         or type q+Enter to quit any time.\n"

    print(header)
    print(welcome)

if __name__ == "__main__":

    print_welcome_message()

    while True:
        initial_conds = collect_inital_conds()

        if initial_conds is not None:
            print("\nInitializing...")
            app = Application(initial_conds)
            app.on_execute()
        else:
            break

        repeat = input("\nCreate another animation [y/n]? ")
        if repeat in ['y', 'Y', "yes", "Yes"]:
            continue
        else:
            print("See you!")
            break
