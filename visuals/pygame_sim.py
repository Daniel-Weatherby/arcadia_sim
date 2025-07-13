import pygame
import random
from environment import Environment, Service
from models.agent import Agent

# --- Constants ---
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

NEED_COLORS = {
    "food": (255, 100, 100),
    "health": (100, 255, 100),
    "education": (100, 100, 255),
}

# --- AgentSprite Class ---
class AgentSprite(pygame.sprite.Sprite):
    def __init__(self, agent, x, y):
        super().__init__()
        self.agent = agent
        self.x = x
        self.y = y
        self.state = "idle"  # idle, moving, at_service, returning
        self.target = None
        self.agent_need = None

        self.image = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4))
        self.image.fill((random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)))
        self.rect = self.image.get_rect()
        self.update_rect()

    def update_rect(self):
        self.rect.topleft = (self.x * CELL_SIZE + 2, self.y * CELL_SIZE + 2)

    def tick(self):
        """Call every simulation tick to reduce usage time per agent and free spots."""
        to_remove = []
        for agent_name in self.users_time:
            self.users_time[agent_name] -= 1
            if self.users_time[agent_name] <= 0:
                to_remove.append(agent_name)
        for agent_name in to_remove:
            self.current_users.remove(agent_name)
            del self.users_time[agent_name]

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        if dx != 0:
            self.x += int(dx / abs(dx))
        elif dy != 0:
            self.y += int(dy / abs(dy))

        # Movement costs energy
        self.agent.energy = max(0, self.agent.energy - 1)

        self.update_rect()

    def update(self, environment):
        if self.state == "idle":
            # Decide what need to fulfill
            self.agent.evaluate_needs()
            self.agent_need = self.agent.decide_need()

            services = environment.get_services_by_type(self.agent_need)
            if self.agent_need == "food" and not services:
                # Eat at home fallback
                print(f"{self.agent.name} eating at home 🍽️")
                self.agent.energy = min(100, self.agent.energy + 5)
                self.agent.happiness = min(1.0, self.agent.happiness + 0.1)
                self.agent.fulfill_need("food")
                self.state = "idle"
                return

            if services:
                # Pick a random service with availability
                available_services = [s for s in services if s.is_available()]
                if available_services:
                    self.target = random.choice(available_services)
                    self.state = "moving"
                else:
                    # No available service
                    print(f"{self.agent.name} could not find available {self.agent_need} service")
                    self.agent.energy = max(0, self.agent.energy - 5)
                    self.agent.happiness = max(0.0, self.agent.happiness - 0.05)
                    self.state = "idle"
                    return
            else:
                print(f"{self.agent.name} no services for need: {self.agent_need}")
                self.state = "idle"
                return

        if self.state == "moving":
            # Move toward service
            if (self.x, self.y) == (self.target.x, self.target.y):
                # Try to use the service
                if self.target.use(self.agent.name):
                    print(f"{self.agent.name} entered {self.target.name} for {self.agent_need}")
                    self.state = "at_service"
                    # Apply rewards
                    self.agent.happiness = min(1.0, self.agent.happiness + self.target.happiness_reward)
                    self.agent.energy = min(100, self.agent.energy + self.target.energy_reward)
                    self.agent.fulfill_need(self.agent_need)
                else:
                    print(f"{self.agent.name} could not access {self.target.name}")
                    self.agent.energy = max(0, self.agent.energy - 5)
                    self.agent.happiness = max(0.0, self.agent.happiness - 0.05)
                    self.state = "idle"
            else:
                self.move_towards(self.target.x, self.target.y)

        elif self.state == "at_service":
            if not hasattr(self, 'service_timer'):
                self.service_timer = 0  # initialize timer once when agent arrives

            self.service_timer += 1

            if self.service_timer >= self.target.usage_duration:
                self.target.release(self.agent.name)  # agent leaves the service
                self.service_timer = 0
                self.state = "returning"
                # Assign home location (or save and reuse a fixed home pos)
                self.home_x = random.randint(0, GRID_SIZE - 1)
                self.home_y = random.randint(0, GRID_SIZE - 1)
            else:
                # Keep occupying
                pass

        elif self.state == "returning":
            if (self.x, self.y) == (self.home_x, self.home_y):
                print(f"{self.agent.name} returned home")
                self.state = "idle"
            else:
                self.move_towards(self.home_x, self.home_y)

# --- Main simulation function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ArcadiaSim: Pygame Visualization")
    clock = pygame.time.Clock()

    # Create environment and services
    env = Environment()
    env.add_service(Service("Clinic A", 2, "health", x=2, y=2, energy_reward=2, happiness_reward=0.2))
    env.add_service(Service("School A", 2, "education", x=6, y=2, energy_reward=1, happiness_reward=0.15))
    env.add_service(Service("Takeaway", 3, "food", x=4, y=6, energy_reward=10, happiness_reward=0.2))

    # Create agents
    agents = [Agent(f"Agent {i}", random.randint(18, 60)) for i in range(5)]
    agent_sprites = pygame.sprite.Group()

    for agent in agents:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        sprite = AgentSprite(agent, x, y)
        agent_sprites.add(sprite)

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw grid
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)

        # Draw services
        for service in env.services.values():
            rect = pygame.Rect(service.x * CELL_SIZE, service.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, NEED_COLORS.get(service.service_type, BLACK), rect)

        # Tick environment to update services usage timers
        env.tick()
        
        # Update and draw agents
        for sprite in agent_sprites:
            sprite.update(env)
            screen.blit(sprite.image, sprite.rect)

        # Draw need bars above agents
        bar_width = CELL_SIZE - 4
        bar_height = 5
        bar_x = sprite.rect.left
        bar_y = sprite.rect.top - bar_height - 2

        for idx, (need, level) in enumerate(sprite.agent.needs.items()):
            fill_width = int(bar_width * level)
            pygame.draw.rect(screen, NEED_COLORS.get(need, GRAY),
                                (bar_x, bar_y + idx * (bar_height + 2), fill_width, bar_height))

        print("\n--- Agent Status Summary ---")
        for sprite in agent_sprites:
            agent = sprite.agent
            needs_status = ", ".join(f"{k}: {v:.2f}" for k, v in agent.needs.items())
            print(f"{agent.name} | Energy: {agent.energy:.1f} | Happiness: {agent.happiness:.2f} | Needs: [{needs_status}]")
        
        pygame.display.flip()
        clock.tick(5)

    pygame.quit()

if __name__ == "__main__":
    main()
