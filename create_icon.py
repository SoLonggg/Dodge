"""
Simple script to create a game icon for Dodging Simulator.
This creates a .ico file that can be used with PyInstaller.
"""
import pygame
import os

# Initialize pygame (just for creating the icon)
pygame.init()

# Icon size (Windows standard is 32x32, but we'll create 64x64 for quality)
icon_size = 64
surface = pygame.Surface((icon_size, icon_size), pygame.SRCALPHA)

# Colors from your game
background_color = (12, 12, 16)
player_color = (80, 200, 255)
projectile_color = (240, 96, 96)
accent_color = (255, 255, 255)

# Fill background
surface.fill(background_color)

# Draw a stylized player (centered circle)
player_radius = 8
player_center = (icon_size // 2, icon_size // 2)
pygame.draw.circle(surface, player_color, player_center, player_radius)
pygame.draw.circle(surface, accent_color, player_center, player_radius, 2)

# Draw some projectiles around the player to show "dodging"
projectile_positions = [
    (16, 16), (48, 16),  # Top corners
    (16, 48), (48, 48),  # Bottom corners
    (32, 12), (32, 52),  # Top and bottom center
    (12, 32), (52, 32)   # Left and right center
]

for pos in projectile_positions:
    pygame.draw.rect(surface, projectile_color, (pos[0]-3, pos[1]-3, 6, 6))
    pygame.draw.rect(surface, accent_color, (pos[0]-3, pos[1]-3, 6, 6), 1)

# Add a subtle border
pygame.draw.rect(surface, accent_color, (0, 0, icon_size, icon_size), 2)

# Save as PNG first
pygame.image.save(surface, "game_icon.png")

print("Icon created as 'game_icon.png'")
print("To convert to .ico format for Windows:")
print("You can use online converters or install Pillow and use the conversion script below.")

# Also create a Pillow-based converter if available
try:
    from PIL import Image
    
    # Load the PNG and convert to ICO
    img = Image.open("game_icon.png")
    # Create multiple sizes for better Windows compatibility
    img.save("game_icon.ico", format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])
    print("Successfully created 'game_icon.ico' with multiple sizes!")
    
except ImportError:
    print("\nTo create .ico file, install Pillow:")
    print("pip install Pillow")
    print("Then run this script again.")

pygame.quit()
