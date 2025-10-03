# Mango: The Virtual Lovebird v2.0

A modern Tamagotchi-inspired virtual pet game featuring Mango the lovebird, built as a CS50P Final Project. Enhanced with beautiful UI, real-world APIs, and sprite support.

## 🎮 Game Overview

Take care of Mango, your virtual lovebird companion! Feed, bathe, play, and nurture Mango through different life stages while enjoying mini-games and watching your pet grow and evolve.

## ✨ Features

### Core Tamagotchi Features
- **Hunger Management** - Feed Mango to keep hunger levels up
- **Happiness System** - Play with Mango and win mini-games to increase happiness
- **Cleanliness Care** - Bathe Mango to maintain hygiene
- **Energy Management** - Let Mango rest to restore energy
- **Health Monitoring** - Keep all stats balanced to maintain health
- **Aging System** - Watch Mango grow from chick to adult over time

### Mini-Game: Flappy Mango
- Fly through the sky avoiding crows
- Score points based on survival time
- High scores are saved and displayed
- Playing increases Mango's happiness

### Advanced Features
- **Real-World Integration** - Weather API affects Mango's mood
- **Educational Content** - Bird facts API provides learning opportunities
- **Day/Night Cycle** - Background changes based on system time
- **Random Events** - Mango can get sick or misbehave
- **Medicine System** - Heal Mango when sick
- **Discipline System** - Manage misbehavior
- **Multiple Moods** - Different sprites based on Mango's condition
- **Custom Sprites** - Load your own Mango images
- **Game Over/Restart** - Start fresh when health reaches zero
- **Modern UI** - Clean, professional interface without emojis

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd mango_project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game**
   ```bash
   python project.py
   ```

### Running Tests
```bash
pytest test_project.py -v
```

## 🎯 How to Play

### Main Hub
- **Feed Button** - Increases hunger (+25) and happiness (+5)
- **Bathe Button** - Increases cleanliness (+30) and happiness (+10)
- **Play Button** - Increases happiness (+20) but decreases energy (-15)
- **Rest Button** - Increases energy (+30)
- **Medicine Button** - Heals Mango when sick (+40 health)
- **Discipline Button** - Reduces misbehavior but decreases happiness (-5)
- **Flappy Mango Button** - Launch the mini-game

### Flappy Mango Mini-Game
- Press **SPACE** to make Mango flap and avoid crows
- Press **ESC** to return to the main hub
- Press **R** to restart the game after game over
- Score increases happiness based on performance

### Stat Management
- **Hunger** - Decreases naturally every 2 minutes (realistic Tamagotchi pace)
- **Happiness** - Decreases if ignored, increases with care and weather
- **Cleanliness** - Decreases over time
- **Energy** - Decreases with play, increases with rest
- **Health** - Decreases if other stats are too low for too long

## 🗄️ Database Schema

The game uses SQLite for data persistence with two main tables:

### mango_state
- Stores Mango's current stats (hunger, happiness, cleanliness, energy, health, age)
- Only one Mango instance at a time
- Auto-updates timestamp on saves

### scores
- Stores Flappy Mango high scores
- Tracks play date and time
- Used for leaderboard display

## 📁 Project Structure

```
mango_project/
│── project.py            # Main game file (1000+ lines)
│── test_project.py       # Comprehensive unit tests (31 tests)
│── schema.sql            # Database schema
│── requirements.txt      # Python dependencies (pygame, pytest, requests, pillow)
│── README.md             # This file
│
├── assets/
│   ├── sprites/          # Mango sprite images (PNG format)
│   │   ├── mango_idle.png
│   │   ├── mango_happy.png
│   │   ├── mango_sad.png
│   │   ├── mango_tired.png
│   │   └── mango_dirty.png
│   ├── backgrounds/      # Background images
│   │   ├── hub_bg.jpg    # Main hub background
│   │   └── flappy_bg.jpg # Flappy Mango background
│   └── sounds/           # Audio assets (WAV format)
└── db/
    └── mango.db          # SQLite database (created automatically)
```

## 🧪 Testing

The project includes comprehensive unit tests covering:
- Stat management and constraints
- Database operations
- Game mechanics
- Random events
- Age progression
- Score saving

Run tests with:
```bash
pytest test_project.py -v
```

## 🎨 Customization

### Adding New Sprites
1. Add sprite files to `assets/sprites/`
2. Update the `draw_home_screen()` method to load and display new sprites
3. Modify `get_mango_mood()` to include new mood states

### Adding New Sounds
1. Add sound files to `assets/sounds/`
2. Use `pygame.mixer.Sound()` to load sounds
3. Play sounds at appropriate game events

### Modifying Game Balance
- Adjust stat decay rates in `update_stats()`
- Modify stat gains from actions (feed, bathe, etc.)
- Change random event probabilities in `check_random_events()`

## 🔮 Future Enhancements

### Stretch Goals (Completed/In Progress)
- **Weather API Integration** ✅ - Real weather affects Mango's mood
- **Custom Sprites** ✅ - Different sprites for different moods
- **Bird Facts API** ✅ - Educational content integration
- **Modern UI** ✅ - Clean, professional interface
- **Leaderboard** - Top 5 Flappy Mango scores
- **Multiple Pets** - Save/load multiple Mango profiles
- **Evolution System** - More complex aging with visual changes
- **Mini-Games** - Additional games beyond Flappy Mango

## 🐛 Troubleshooting

### Common Issues

**Game won't start:**
- Ensure pygame is installed: `pip install pygame`
- Check Python version (3.7+ required)

**Database errors:**
- Delete `db/mango.db` to reset the database
- Ensure write permissions in the project directory

**Missing sprites/sounds:**
- The game works without assets (uses colored shapes)
- Add sprite/sound files as described in asset README files

**Performance issues:**
- Reduce FPS in the `FPS` constant
- Close other applications to free up resources

## 📝 Technical Details

### Architecture
- **Main Class**: `MangoTamagotchi` handles all game logic
- **Game States**: Uses state machine pattern for different screens
- **Database**: SQLite with connection pooling
- **Graphics**: Pygame for rendering and input handling

### Key Algorithms
- **Stat Decay**: Time-based stat reduction with configurable rates
- **Random Events**: Probabilistic event system with cooldowns
- **Collision Detection**: Rectangle-based collision for Flappy Mango
- **Score System**: Persistent high score tracking

## 📄 License

This project is created as part of CS50P coursework. Feel free to use and modify for educational purposes.

## 👨‍💻 Author

Created as a CS50P Final Project showcasing Python programming concepts including:
- Object-oriented programming
- Database management
- Game development
- Testing methodologies
- User interface design

---

*Enjoy taking care of Mango!*
