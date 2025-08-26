"""
Refactored main game file using design patterns.
This demonstrates proper OOP design with State, Observer, Factory, Singleton, and Strategy patterns.
"""

import os
import pygame
from typing import List, Optional

# Import design patterns
from Dodging_Simulator.patterns.state import GameContext
from Dodging_Simulator.patterns.observer import GameEventManager, ScoreObserver, StatsObserver
from Dodging_Simulator.patterns.factory import ConcreteGameObjectFactory
from Dodging_Simulator.patterns.singleton import GameConfig, GameState
from Dodging_Simulator.patterns.strategy import (
    GameModeContext, NormalModeStrategy, NightmareModeStrategy
)

# Import existing components
from Dodging_Simulator.entities.player import Player
from Dodging_Simulator.entities.enhanced_projectile import (
    create_random_projectile, EnhancedProjectile, WarningIndicator,
    ProjectileType, create_warning_for_longsword
)
from Dodging_Simulator.managers.score_manager import ScoreManager
from Dodging_Simulator.managers.sound_manager import SoundManager
from Dodging_Simulator.ui.menu import MenuScreen
from Dodging_Simulator.ui.hall_of_fame import HallOfFameScreen
from Dodging_Simulator.ui.hud import HUD
from Dodging_Simulator.config import GAME_WIDTH, GAME_HEIGHT, BACKGROUND_COLOR, BACKGROUND_IMAGE


class DodgingSimulatorGame(GameContext):
    """Main game class implementing design patterns."""
    
    def __init__(self) -> None:
        super().__init__()
        
        # Initialize pygame
        pygame.init()
        pygame.font.init()
        
        # Setup display
        self.window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
        pygame.display.set_caption("Dodging Simulator")
        
        # Load assets
        self._load_assets()
        
        # Initialize singletons
        self.game_config = GameConfig()
        self.game_state = GameState()
        
        # Initialize event system
        self.event_manager = GameEventManager()
        self.stats_observer = StatsObserver()
        
        # Initialize factories and strategies
        self.factory = ConcreteGameObjectFactory()
        self.game_mode_context = GameModeContext(NormalModeStrategy(self.event_manager))
        
        # Initialize managers
        score_base_dir = os.path.dirname(__file__)
        self.score_manager = ScoreManager(score_base_dir)
        self.score_observer = ScoreObserver(self.score_manager)
        
        # Setup observers
        self.event_manager.attach(self.score_observer)
        self.event_manager.attach(self.stats_observer)
        
        # Initialize UI components
        self._initialize_ui()
        
        # Game objects
        self.player: Optional[Player] = None
        self.projectiles: List[EnhancedProjectile] = []
        self.warning_indicators: List[WarningIndicator] = []
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Timing
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Start in menu state
        self.transition_to_menu()
    
    def _load_assets(self) -> None:
        """Load game assets."""
        try:
            self.background_image = pygame.image.load(BACKGROUND_IMAGE).convert()
            self.background_image = pygame.transform.scale(self.background_image, (GAME_WIDTH, GAME_HEIGHT))
        except (pygame.error, FileNotFoundError):
            print(f"Warning: Could not load background image from {BACKGROUND_IMAGE}")
            # Create a fallback background
            self.background_image = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            self.background_image.fill(BACKGROUND_COLOR)
    
    def _initialize_ui(self) -> None:
        """Initialize UI components."""
        self.default_font = pygame.font.SysFont("consolas", 22)
        self.large_font = pygame.font.SysFont("consolas", 48, bold=True)
        self.title_font = pygame.font.SysFont("consolas", 64, bold=True)
        
        self.menu_screen = MenuScreen()
        self.menu_screen.setup_buttons(self.default_font, self.title_font)
        
        self.hall_of_fame_screen = HallOfFameScreen(self.score_manager)
        self.hall_of_fame_screen.setup_button(self.default_font)
    
    def set_game_mode(self, mode: str) -> None:
        """Set the game mode using strategy pattern."""
        if mode == "normal":
            strategy = NormalModeStrategy(self.event_manager)
        elif mode == "nightmare":
            strategy = NightmareModeStrategy(self.event_manager)
        else:
            raise ValueError(f"Unknown game mode: {mode}")
        
        self.game_mode_context.set_strategy(strategy)
        self.game_state.set_mode(mode)
    
    def initialize_game(self) -> None:
        """Initialize game objects for new game."""
        # Reset observers
        self.stats_observer.reset()
        
        # Create player using factory
        self.player = self.game_mode_context.create_player()
        
        # Clear projectiles and warnings
        self.projectiles.clear()
        self.warning_indicators.clear()
        
        # Setup spawn timer
        spawn_interval = self.game_mode_context.get_spawn_interval(0.0)
        self.current_spawn_interval = spawn_interval
        pygame.time.set_timer(self.SPAWN_EVENT, spawn_interval)
    
    def spawn_projectile(self) -> None:
        """Spawn a new projectile using factory pattern."""
        projectile = self.game_mode_context.create_projectile()
        self.projectiles.append(projectile)
    
    def render_game(self, surface: pygame.Surface, game_over: bool, elapsed_seconds: float, final_score: Optional[float]) -> None:
        """Render the game state."""
        surface.fill(BACKGROUND_COLOR)
        surface.blit(self.background_image, (0, 0))
        
        if not game_over and self.player:
            # Draw game objects
            self.player.draw(surface)
            for projectile in self.projectiles:
                projectile.draw(surface)
            
            # Draw warning indicators
            for warning in self.warning_indicators:
                warning.draw(surface)
            
            # Draw HUD
            mode_name = self.game_mode_context.get_mode_name()
            HUD.draw_hearts(surface, self.player.health, self.player.max_health, mode_name)
            HUD.draw_time(surface, elapsed_seconds)
            
            # Draw nightmare mode specific stats
            if mode_name == "nightmare":
                hearts_needed = 75 if self.stats_observer.hearts_restored == 0 else 150
                next_heart_at = hearts_needed * (self.stats_observer.hearts_restored + 1)
                HUD.draw_nightmare_stats(surface, self.stats_observer.projectiles_dodged, next_heart_at)
        else:
            # Draw game over screen
            self._render_game_over(surface, final_score)
    
    def _render_game_over(self, surface: pygame.Surface, final_score: Optional[float]) -> None:
        """Render game over screen."""
        from Dodging_Simulator.config import GAME_OVER_OVERLAY, HUD_TEXT_COLOR
        from Dodging_Simulator.utils.formatting import format_seconds
        
        # Draw overlay
        overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
        overlay.fill(GAME_OVER_OVERLAY)
        surface.blit(overlay, (0, 0))
        
        # Draw game over text
        title_surface = self.large_font.render("Game Over", True, HUD_TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 120))
        surface.blit(title_surface, title_rect)
        
        # Draw score
        if final_score is None:
            final_text = "Score: 0.0s"
        else:
            final_text = f"Score: {format_seconds(final_score)}"
        score_surface = self.default_font.render(final_text, True, HUD_TEXT_COLOR)
        score_rect = score_surface.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 60))
        surface.blit(score_surface, score_rect)
        
        # Draw instructions
        instruction_surface = self.default_font.render("Press R to restart  |  Esc to menu", True, HUD_TEXT_COLOR)
        instruction_rect = instruction_surface.get_rect(center=(GAME_WIDTH // 2, GAME_HEIGHT // 2))
        surface.blit(instruction_surface, instruction_rect)
        
        # Draw top scores
        mode_name = self.game_mode_context.get_mode_name()
        top = self.score_manager.top_scores(5, mode_name)
        mode_text = "Normal Mode" if mode_name == "normal" else "Nightmare Mode"
        highs_title = self.default_font.render(f"Top Scores ({mode_text})", True, HUD_TEXT_COLOR)
        surface.blit(highs_title, (GAME_WIDTH // 2 - highs_title.get_width() // 2, GAME_HEIGHT // 2 + 36))
        
        for idx, value in enumerate(top, start=1):
            line = self.default_font.render(f"{idx}. {format_seconds(value)}", True, HUD_TEXT_COLOR)
            surface.blit(line, (GAME_WIDTH // 2 - 80, GAME_HEIGHT // 2 + 36 + idx * 26))
    
    def run(self) -> None:
        """Main game loop."""
        while self.running and self.game_state.game_running:
            dt_seconds = self.clock.tick(60) / 1000.0
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)
            
            # Update
            self.update(dt_seconds)
            
            # Render
            self.render(self.window)
            pygame.display.update()
        
        pygame.quit()


def main() -> None:
    """Main entry point."""
    game = DodgingSimulatorGame()
    game.run()


if __name__ == "__main__":
    main()
