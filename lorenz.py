# Lorenz Attractor Animator and CLI
# by Andrew Kerr <kerrand@protonmail.com>

import pygame


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
        self.y += (self.x_prev *
                   (self.B - self.z_prev) - self.y_prev) * self.dt
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

    def to_screen_coords(
            self, x, y, x_min, x_max, y_min, y_max, width, height):
        screen_x = width * ((x - x_min) / (x_max - x_min))
        screen_y = height * ((y - y_min) / (y_max - y_min))

        return round(screen_x), round(screen_y)


class Simulator():
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
        if self.on_init() is False:
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
    colors = (ORANGE, BLUE, GREEN, RED, GREY)

    SLOW = 0.0025
    MEDIUM = 0.005
    FAST = 0.01
    speeds = (SLOW, MEDIUM, FAST)

    num_attractors = None
    while True:
        prompt = "How many attractors would you like to animate [1 - 5]? "
        inp = input(prompt).lower().strip()
        if inp in ("q", "quit"):
            return None

        try:
            num_attractors = int(inp)
        except ValueError:
            print("Please enter a number between 1 and 5", "\n")
            continue

        if num_attractors not in range(1, 6):
            print("Please enter a number between 1 and 5", "\n")
            continue

        break

    speed_choice = None
    valid_speeds = ("slow", "medium", "fast")
    while True:
        prompt = "How fast would you like the animation to evolve "
        prompt += "[slow | medium | fast]? "
        speed_in = input(prompt).lower().strip()
        if speed_in in ("q", "quit"):
            return None

        if speed_in not in valid_speeds:
            print("Please enter a valid choice.", "\n")
            continue

        speed_choice = speeds[valid_speeds.index(speed_in)]

        break

    initial_conds = []
    for i in range(num_attractors):
        print("")
        print(f"Attractor #{i+1}")
        print("=================")

        x_in = {"prompt": "Initial x [-1.0 - +1.0]? ", "val": None}
        y_in = {"prompt": "Initial y [-1.0 - +1.0]? ", "val": None}
        z_in = {"prompt": "Initial z [-1.0 - +1.0]? ", "val": None}

        # one while loop is used to collect valid inital conditions,
        # the second invites the user to re-enter them if x_in == y_in == 0
        while True:
            for coord in (x_in, y_in, z_in):
                while True:
                    inp = input(f"{coord['prompt']}").lower().strip()
                    if inp in ("q", "quit"):
                        return None

                    try:
                        coord["val"] = float(inp)
                    except ValueError:
                        print("Please enter a value between -1.0 and +1.0\n")
                        continue

                    if abs(coord["val"]) > 1.0:
                        print("Please enter a value between -1.0 and +1.0\n")
                        continue

                    break

            if x_in["val"] == 0.0 and y_in["val"] == 0.0:
                warning = "WARNING: The animtator currently supports "
                warning += "attractor animations in the xy-plane only.\n"
                warning += "         Initial x- and y-values of 0.0 will create "
                warning += "a stationary attractor.\n\nProceed [y/n]? "

                response = input(warning).lower().strip()
                if response not in ("y", "yes"):
                    continue

            break

        initial_conds.append(
            (x_in["val"], y_in["val"], z_in["val"], colors[i], speed_choice)
        )

    return initial_conds


def print_welcome_message():
    header = "\n============= LORENZ ATTRACTOR ANIMATOR =============\n\n"

    welcome = "Welcome! Follow the instructions below to get started,\n"
    welcome += "         or type q+Enter to quit any time.\n\n"

    print(header)
    print(welcome)


def print_exit_message():
    print("\nSee you!")


if __name__ == "__main__":

    print_welcome_message()

    while True:
        initial_conds = collect_inital_conds()

        if initial_conds is not None:
            print("\nInitializing...")
            print("\nRunning...press any key to stop.")
            app = Simulator(initial_conds)
            app.on_execute()
        else:
            break

        repeat = input("\nCreate another animation [y/n]? ").lower().strip()
        if repeat in ("y", "yes"):
            continue
        else:
            break

    print_exit_message()
