# Mango: The Virtual Lovebird v2.0

A modern Tamagotchi-inspired virtual pet game featuring Mango the lovebird, built as a CS50P Final Project. Enhanced with fun UI, real-world APIs, and sprite support. Inspired by my old bird friend Mango. May he rest in peace.

## Game Overview

Take care of Mango, your virtual lovebird companion! Feed, bathe, play, and nurture Mango through different life stages while enjoying mini-games and watching your pet grow and evolve.

## Features

### Core Tamagotchi Features
- **Hunger Management** - Feed Mango to keep hunger levels up
````markdown
# Mango: The Virtual Lovebird v2.0

Mango is a Tamagotchi-inspired virtual pet game featuring Mango the lovebird, built as a final project for CS50's Introduction to Programming with Python at Harvard.

This repository and the game are dedicated in loving memory of my pet love bird Mango (2019–2024). Mango was too beautiful for this world. He was more than a pet — he was my friend and a member of my family. I miss him deeply. May he be flying among the stars.

## Game Overview

Take care of Mango, your virtual lovebird companion. Feed, bathe, play, and nurture Mango through different life stages while enjoying mini-games and watching your pet grow.

## Features

### Core Tamagotchi Features
- Hunger management: Feed Mango to keep hunger levels up
- Happiness system: Play with Mango and win mini-games to increase happiness
- Cleanliness care: Bathe Mango to maintain hygiene
- Energy management: Let Mango rest to restore energy
- Health monitoring: Keep all stats balanced to maintain health
- Aging system: Watch Mango grow from chick to adult over time

### Mini-Game: Flappy Mango
- Fly through the sky avoiding crow towers
- Score points based on survival time
- High scores are saved and displayed
- Playing increases Mango's happiness

### Advanced Features
- Real-world integration: Weather API affects Mango's mood
- Educational content: Bird facts API provides learning opportunities
- Day/night cycle: Background changes based on system time
- Random events: Mango can get sick or misbehave
- Medicine system: Heal Mango when sick
- Discipline system: Manage misbehavior
- Multiple moods: Different sprites based on Mango's condition
- Custom sprites: Load your own Mango images
- Game over/restart: Start fresh when health reaches zero

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. Clone or download the project
   ```bash
   git clone <repository-url>
   cd mango_project
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the game
   ```bash
   python project.py
   ```

### Running Tests
```bash
pytest test_project.py -v
```

## How to Play

### Main Hub
- Feed button: Increases hunger (+25) and happiness (+5)
- Bathe button: Increases cleanliness (+30) and happiness (+10)
- Play button: Increases happiness (+20) but decreases energy (-15)
- Rest button: Increases energy (+30)
- Medicine button: Heals Mango when sick
- Discipline button: Reduces misbehavior but decreases happiness (-5)
- Flappy Mango button: Launch the mini-game

### Flappy Mango Mini-Game
- Press SPACE to make Mango flap and avoid crows
- Press ESC to return to the main hub
- Press R to restart the game after game over
- Score increases happiness based on performance

### Stat Management
- Hunger: Decreases naturally every 2 minutes (realistic Tamagotchi pace)
- Happiness: Decreases if ignored, increases with care and weather
- Cleanliness: Decreases over time
- Energy: Decreases with play, increases with rest
- Health: Decreases if other stats are too low for too long

## Database Schema

The game uses SQLite for data persistence with two main tables:

### mango_state
- Stores Mango's current stats (hunger, happiness, cleanliness, energy, health, age)
- Only one Mango instance at a time
- Auto-updates timestamp on saves

### scores
- Stores Flappy Mango high scores
- Tracks play date and time
- Used for leaderboard display

## Project Structure

```
mango_project/
│── project.py            # Main game file
│── test_project.py       # Unit tests
│── schema.sql            # Database schema
│── requirements.txt      # Python dependencies (pygame, pytest, requests, pillow)
│── README.md             # This file
│
├── assets/
│   ├── sprites/          # Mango sprite images (PNG format)
│   ├── backgrounds/      # Background images
│   └── sounds/           # Audio assets (WAV format)
└── db/
    └── mango.db          # SQLite database (created automatically)
```

## Testing

The project includes unit tests covering stat management, database operations, game mechanics, random events, age progression, and score saving.

Run tests with:
```bash
pytest test_project.py -v
```

## Customization

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

## Future Enhancements

- Weather API integration - real weather affects Mango's mood
- Custom sprites - different sprites for different moods
- Bird facts API - educational content integration
- Modern UI - clean, professional interface
- Leaderboard - top Flappy Mango scores
- Multiple pets - save/load multiple Mango profiles
- Evolution system - more complex aging with visual changes
- Additional mini-games

## Troubleshooting

Common issues:

Game won't start:
- Ensure pygame is installed: `pip install pygame`
- Check Python version (3.7+ required)

Database errors:
- Delete `db/mango.db` to reset the database
- Ensure write permissions in the project directory

Missing sprites/sounds:
- The game works without assets (uses colored shapes)
- Add sprite/sound files as described in asset README files

Performance issues:
- Reduce FPS in the `FPS` constant
- Close other applications to free up resources

## Technical Details

### Architecture
- Main class: `MangoTamagotchi` handles game logic
- Game states: Uses state machine pattern for different screens
- Database: SQLite
- Graphics: Pygame for rendering and input handling

### Key Algorithms
- Stat decay: Time-based stat reduction with configurable rates
- Random events: Probabilistic event system with cooldowns
- Collision detection: Rectangle-based collision for Flappy Mango
- Score system: Persistent high score tracking

## License

This project was created as part of CS50P coursework. Feel free to use and modify for educational purposes.

## Author

Created as a CS50P final project showcasing Python programming concepts including object-oriented programming, database management, game development, testing methodologies, and user interface design.

---

If you want the dedication phrasing changed, tell me and I'll update it.

````
---
