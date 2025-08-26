# 🎮 Dodging Simulator

A fast-paced arcade game where you dodge projectiles and survive as long as possible! Features two challenging game modes with different mechanics and difficulty levels.

![Game Icon](game_icon.png)

## 🚀 Quick Start

### For Players
1. **Download** `Dodging_Simulator.exe` from the releases
2. **Double-click** to run - no installation required!
3. **Enjoy** the game!

### For Developers
1. **Clone** this repository
2. **Install** Python 3.9+ and required dependencies
3. **Run** `python start_screen.py` to play
4. **Build** executable with `python build_game.py`

## 🎯 Game Modes

### 🟢 Normal Mode
- **5 Hearts** to start
- **Balanced difficulty** - perfect for beginners
- **Projectile damage**: Small (1 heart), Large (2 hearts)
- **Goal**: Survive as long as possible!

### 🔴 Nightmare Mode
- **5 Hearts** to start (same as Normal)
- **25% smaller player hitbox** - harder to avoid hits
- **150% faster projectiles** - lightning-fast action
- **150% larger projectiles** - bigger hitboxes to avoid
- **Dynamic difficulty**: Spawn rate increases every 5 seconds
- **Heart restoration system**:
  - 🏆 First restoration: 75 projectiles dodged
  - 🏆 Subsequent restorations: 150 projectiles each
  - 💪 No heart limit - stack up for epic runs!

## 🎮 Controls

| Key | Action |
|-----|--------|
| `W` `A` `S` `D` | Move player |
| `Arrow Keys` | Alternative movement |
| `ESC` | Return to menu |
| `R` | Restart game (when game over) |

## 🏆 Features

- **Modern UI** with heart-based health display
- **Real-time timer** showing survival time
- **Separate leaderboards** for each game mode
- **Progressive difficulty** in Nightmare mode
- **Custom game icon** and professional presentation
- **Standalone executable** - share with anyone!

## 📁 Project Structure

```
Dodging Simulator/
├── game_main.py             # Main game file (design patterns)
├── Dodging_Simulator/       # Game modules
│   ├── config.py           # Game constants and settings
│   ├── entities/           # Game objects (Player, Projectiles)
│   ├── managers/           # Score management
│   ├── ui/                 # User interface components
│   ├── utils/              # Utility functions
│   └── patterns/           # Design pattern implementations
├── assets/                 # Game assets
|   |__images/              # Game-related images and avatars   
|   |____background/    
|   |____character/ 
|   |____projectiles/ 
|   |____warning_sign/          
├── build_game.py          # Build script for executable
├── game_icon.ico          # Game icon
├── DESIGN_PATTERNS.md     # Design patterns documentation
└── README.md              # This file
```

## 🛠️ Development

### Prerequisites
```bash
pip install pygame pillow pyinstaller
```

### Running from Source
```bash
python game_main.py
```

### Building Executable
```bash
python build_game.py
```
Creates `dist/Dodging_Simulator.exe` - ready to distribute!

### Modifying the Game
- **Game settings**: Edit `Dodging_Simulator/config.py`
- **Player mechanics**: Edit `Dodging_Simulator/entities/player.py`
- **Projectile behavior**: Edit `Dodging_Simulator/entities/projectile.py`
- **UI elements**: Edit files in `Dodging_Simulator/ui/`

## 🎨 Technical Details

- **Engine**: Pygame
- **Language**: Python 3.9+
- **Architecture**: Modular object-oriented design
- **Executable**: PyInstaller with custom icon
- **Assets**: PNG images, configurable colors

## 📈 High Scores

Scores are automatically saved locally:
- **Normal Mode**: `scores_normal.txt`
- **Nightmare Mode**: `scores_nightmare.txt`

## 🐛 Troubleshooting

### Game won't start
- Ensure all files are in the same directory
- Try running `python game_main.py` instead
- Check that images folder contains `background/test_bg.png`

### Performance issues
- Close other applications for better performance
- Check graphics drivers are up to date

### Antivirus false positive
- Some antivirus software flags PyInstaller executables
- Add exception to your antivirus if needed
- The executable is safe - this is a common occurrence

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is open source. Feel free to modify and distribute!
This project is created solely for the purpose of the study for OOP concepts (originally in C++, coded using Python for familiarity)

## 🎉 Credits

Created with ❤️ using Python and Pygame.

---

**Enjoy the game and see how long you can survive!** 🚀
"# Dodging-Simulator" 
