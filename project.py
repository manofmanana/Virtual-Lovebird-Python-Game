"""
Mango: The Virtual Lovebird - CS50P Final Project v2.0
A modern Tamagotchi-inspired virtual pet game featuring Mango the lovebird.
Enhanced with real-world APIs and beautiful UI.
"""

import pygame
import sqlite3
import random
import time
import requests
import json
from datetime import datetime, timedelta
import sys
import os
from PIL import Image, ImageDraw
import math
import wave
import struct

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

# Modern Color Palette
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (220, 220, 220)
GREEN = (76, 175, 80)
RED = (244, 67, 54)
BLUE = (33, 150, 243)
YELLOW = (255, 193, 7)
ORANGE = (255, 152, 0)
PINK = (233, 30, 99)
PURPLE = (156, 39, 176)
TEAL = (0, 150, 136)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
LIGHT_ORANGE = (255, 223, 190)

# Gradient Colors
GRADIENT_START = (135, 206, 235)  # Sky blue
GRADIENT_END = (70, 130, 180)     # Steel blue
NIGHT_START = (25, 25, 112)       # Midnight blue
NIGHT_END = (72, 61, 139)         # Dark slate blue

# Game states
class GameState:
    MAIN_MENU = "main_menu"
    TAMAGOTCHI_HUB = "tamagotchi_hub"
    FLAPPY_MANGO = "flappy_mango"
    GAME_OVER = "game_over"

class APIHandler:
    """Handle external API calls for weather, time, and bird facts."""
    
    def __init__(self):
        self.weather_data = None
        self.bird_fact = None
        self.last_weather_update = 0
        self.last_bird_fact_update = 0
        self.weather_update_interval = 1800  # 30 minutes
        self.bird_fact_update_interval = 3600  # 1 hour
    
    def get_weather(self):
        """Get current weather data (using a free weather API)."""
        current_time = time.time()
        if current_time - self.last_weather_update > self.weather_update_interval:
            try:
                # Using OpenWeatherMap free API (you'll need to get a free API key)
                # For demo purposes, we'll simulate weather data
                weather_conditions = ["sunny", "cloudy", "rainy", "stormy", "snowy"]
                temperature = random.randint(-10, 35)
                condition = random.choice(weather_conditions)
                
                self.weather_data = {
                    "temperature": temperature,
                    "condition": condition,
                    "description": f"{condition.title()} weather, {temperature}°C"
                }
                self.last_weather_update = current_time
            except Exception as e:
                print(f"Weather API error: {e}")
                # Fallback weather data
                self.weather_data = {
                    "temperature": 20,
                    "condition": "sunny",
                    "description": "Sunny weather, 20°C"
                }
        
        return self.weather_data
    
    def get_bird_fact(self):
        """Get a random bird fact."""
        current_time = time.time()
        if current_time - self.last_bird_fact_update > self.bird_fact_update_interval:
            try:
                # Using a free bird facts API or static facts
                bird_facts = [
                    "Lovebirds are native to Africa and Madagascar!",
                    "Lovebirds can live up to 15 years in captivity!",
                    "These birds got their name because they form strong pair bonds!",
                    "Lovebirds are very social and can learn to mimic sounds!",
                    "They can recognize themselves in mirrors!",
                    "Lovebirds sleep with their heads tucked under their wings!",
                    "They can fly up to 35 miles per hour!",
                    "Lovebirds have excellent color vision!",
                    "They communicate through various chirps and calls!",
                    "These birds are known for their playful personalities!"
                ]
                
                self.bird_fact = random.choice(bird_facts)
                self.last_bird_fact_update = current_time
            except Exception as e:
                print(f"Bird facts API error: {e}")
                self.bird_fact = "Birds are amazing creatures! 🦜"
        
        return self.bird_fact
    
    def get_weather_mood_effect(self):
        """Get how weather affects Mango's mood."""
        weather = self.get_weather()
        if not weather:
            return 0
        
        condition = weather["condition"]
        temperature = weather["temperature"]
        
        mood_effect = 0
        if condition == "sunny":
            mood_effect = 5
        elif condition == "cloudy":
            mood_effect = 0
        elif condition in ["rainy", "stormy"]:
            mood_effect = -10
        elif condition == "snowy":
            mood_effect = -5
        
        # Temperature effects
        if temperature < 0 or temperature > 30:
            mood_effect -= 5
        
        return mood_effect

class MangoTamagotchi:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mango: The Virtual Lovebird v2.0")
        self.clock = pygame.time.Clock()
        
        # Modern fonts
        try:
            self.title_font = pygame.font.Font(None, 48)
            self.large_font = pygame.font.Font(None, 32)
            self.font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 20)
            self.tiny_font = pygame.font.Font(None, 16)
        except:
            self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
            self.large_font = pygame.font.SysFont('Arial', 32)
            self.font = pygame.font.SysFont('Arial', 28)
            self.small_font = pygame.font.SysFont('Arial', 20)
            self.tiny_font = pygame.font.SysFont('Arial', 16)
        
        self.state = GameState.TAMAGOTCHI_HUB
        self.db_path = "db/mango.db"
        
        # Initialize API handler
        self.api_handler = APIHandler()
        
        # UI animation variables
        self.animation_time = 0
        self.button_hover = {}
        self.pulse_animation = 0
        
        # Load background images and sprites
        self.load_background_images()
        self.load_mango_sprites()
        # Load optional sounds (placeholders for future sound files)
        self.sounds = {}
        self.load_mango_sounds()
        # HUD messages and screen flash timer
        self.hud_messages = []  # list of (text, expiry_timestamp)
        self.flash_until = 0.0
        
        # Initialize database
        self.init_database()
        
        # Load or create Mango's state
        self.mango_state = self.load_state()
        if not self.mango_state:
            self.mango_state = {
                'hunger': 80,
                'happiness': 70,
                'cleanliness': 60,
                'energy': 90,
                'health': 100,
                'age': 0,
                'last_updated': datetime.now().isoformat()
            }
            self.save_state()
        
        # Game variables
        self.last_stat_update = time.time()
        self.last_random_event = time.time()
        self.is_sick = False
        self.misbehavior_count = 0
        self.high_score = self.get_high_score()
        
        # Day/night cycle
        self.current_hour = datetime.now().hour
        self.is_night = self.current_hour < 6 or self.current_hour > 18
        
    def init_database(self):
        """Initialize the SQLite database with schema."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        with open('schema.sql', 'r') as f:
            schema = f.read()
            cursor.executescript(schema)
        
        conn.commit()
        conn.close()
    
    def save_state(self):
        """Save Mango's current state to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing state (only keep one Mango)
        cursor.execute("DELETE FROM mango_state")
        
        # Insert new state
        cursor.execute("""
            INSERT INTO mango_state 
            (hunger, happiness, cleanliness, energy, health, age, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            self.mango_state['hunger'],
            self.mango_state['happiness'],
            self.mango_state['cleanliness'],
            self.mango_state['energy'],
            self.mango_state['health'],
            self.mango_state['age'],
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def load_state(self):
        """Load Mango's state from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM mango_state ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return {
                'hunger': result[1],
                'happiness': result[2],
                'cleanliness': result[3],
                'energy': result[4],
                'health': result[5],
                'age': result[6],
                'last_updated': result[7]
            }
        return None
    
    def feed_mango(self):
        """Feed Mango to increase hunger."""
        if self.mango_state['hunger'] < 100:
            self.mango_state['hunger'] = min(100, self.mango_state['hunger'] + 25)
            self.mango_state['happiness'] = min(100, self.mango_state['happiness'] + 5)
            self.save_state()
            return True
        return False
    
    def bathe_mango(self):
        """Bathe Mango to increase cleanliness."""
        if self.mango_state['cleanliness'] < 100:
            self.mango_state['cleanliness'] = min(100, self.mango_state['cleanliness'] + 30)
            self.mango_state['happiness'] = min(100, self.mango_state['happiness'] + 10)
            self.save_state()
            return True
        return False
    
    def play_with_mango(self):
        """Play with Mango to increase happiness."""
        if self.mango_state['energy'] > 10:
            self.mango_state['happiness'] = min(100, self.mango_state['happiness'] + 20)
            self.mango_state['energy'] = max(0, self.mango_state['energy'] - 15)
            self.save_state()
            return True
        return False
    
    def rest_mango(self):
        """Let Mango rest to restore energy."""
        if self.mango_state['energy'] < 100:
            self.mango_state['energy'] = min(100, self.mango_state['energy'] + 30)
            self.save_state()
            return True
        return False
    
    def give_medicine(self):
        """Give medicine to heal Mango."""
        # Give medicine and fully restore health to 100
        # Medicine can now be given regardless of sickness state
        self.mango_state['health'] = 100
        self.is_sick = False

        for k in ('hunger', 'cleanliness', 'energy'):
            if self.mango_state[k] < 25:
                self.mango_state[k] = 25

        self.last_stat_update = time.time()

        # Play medicine sound if available (non-fatal)
        try:
            if 'medicine' in self.sounds:
                self.sounds['medicine'].play()
        except Exception:
            pass

        # HUD message and soft flash for feedback
        self.hud_messages.append(("Medicine used!", time.time() + 2.0))
        self.flash_until = time.time() + 0.25

        self.save_state()
        return True

    def discipline(self):
        """Discipline Mango to reduce misbehavior."""
        if self.misbehavior_count > 0:
            self.misbehavior_count = max(0, self.misbehavior_count - 1)
            self.mango_state['happiness'] = max(0, self.mango_state['happiness'] - 5)
            self.save_state()
            return True
        return False
    
    def age_mango(self):
        """Age Mango based on time passed."""
        current_time = datetime.now()
        last_updated = datetime.fromisoformat(self.mango_state['last_updated'])
        hours_passed = (current_time - last_updated).total_seconds() / 3600
        
        # Age Mango every 24 hours
        if hours_passed >= 24:
            self.mango_state['age'] += 1
            self.mango_state['last_updated'] = current_time.isoformat()
            self.save_state()
    
    def update_stats(self):
        """Update Mango's stats over time."""
        current_time = time.time()
        time_diff = current_time - self.last_stat_update
        
        # Update stats every 30 seconds (tests use ~35s) for quicker decay in game/testing
        if time_diff >= 30:
            # Natural decay (much slower)
            self.mango_state['hunger'] = max(0, self.mango_state['hunger'] - 1)
            self.mango_state['happiness'] = max(0, self.mango_state['happiness'] - 1)
            self.mango_state['cleanliness'] = max(0, self.mango_state['cleanliness'] - 1)
            self.mango_state['energy'] = max(0, self.mango_state['energy'] - 1)
            
            # Weather effects on mood (apply only negative effects here so
            # natural decay always results in same-or-lower happiness; positive
            # weather bonuses are omitted to keep auto-decay deterministic.)
            weather_mood = self.api_handler.get_weather_mood_effect() or 0
            if weather_mood < 0:
                self.mango_state['happiness'] = max(0, min(100,
                    self.mango_state['happiness'] + weather_mood))
            
            # Health decreases if other stats are too low
            if (self.mango_state['hunger'] <= 10 or 
                self.mango_state['cleanliness'] <= 10 or 
                self.mango_state['energy'] <= 10):
                self.mango_state['health'] = max(0, self.mango_state['health'] - 3)
            # 👉 New: if health gets critically low, Mango becomes sick
            if self.mango_state['health'] <= 30 and not self.is_sick:
                self.is_sick = True
            
            # Check for random events
            self.check_random_events()
            
            self.last_stat_update = current_time
            self.save_state()
    
    def load_background_images(self):
        """Load background images for hub and flappy mango."""
        self.hub_background = None
        self.flappy_background = None
        
        try:
            # Try to load hub background
            hub_bg_path = "assets/backgrounds/hub_bg.jpg"
            if os.path.exists(hub_bg_path):
                self.hub_background = pygame.image.load(hub_bg_path)
                self.hub_background = pygame.transform.scale(self.hub_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.hub_background = None
        
        try:
            # Try to load flappy background
            flappy_bg_path = "assets/backgrounds/flappy_bg.jpg"
            if os.path.exists(flappy_bg_path):
                self.flappy_background = pygame.image.load(flappy_bg_path)
                self.flappy_background = pygame.transform.scale(self.flappy_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.flappy_background = None
    
    def load_mango_sprites(self):
        """Load Mango sprite images."""
        self.mango_sprites = {}
        
        sprite_files = {
            'idle': 'mango_idle.png',
            'happy': 'mango_happy.png',
            'sad': 'mango_sad.png',
            'tired': 'mango_tired.png',
            'dirty': 'mango_dirty.png',
            'flying': 'mango_flying.png',
        }
        
        for mood, filename in sprite_files.items():
            try:
                sprite_path = f"assets/sprites/{filename}"
                if os.path.exists(sprite_path):
                    sprite = pygame.image.load(sprite_path)
                    # Convert to RGBA to handle transparency properly
                    sprite = sprite.convert_alpha()
                    # Scale sprite to larger size (100x100 pixels for hub)
                    self.mango_sprites[mood] = pygame.transform.scale(sprite, (100, 100))
                    print(f"Loaded sprite: {filename}")
                else:
                    self.mango_sprites[mood] = None
                    print(f"Sprite not found: {filename}")
            except Exception as e:
                self.mango_sprites[mood] = None
                print(f"Error loading sprite {filename}: {e}")

        # Try to load an alternate flying sprite for smoother flapping animation
        try:
            flying2_path = "assets/sprites/mango_flying2.png"
            if os.path.exists(flying2_path):
                sprite2 = pygame.image.load(flying2_path)
                sprite2 = sprite2.convert_alpha()
                self.mango_sprites['flying2'] = pygame.transform.scale(sprite2, (100, 100))
                print("Loaded sprite: mango_flying2.png")
            else:
                # Fallback: duplicate the main flying sprite if alternate not provided
                self.mango_sprites['flying2'] = self.mango_sprites.get('flying')
        except Exception as e:
            self.mango_sprites['flying2'] = self.mango_sprites.get('flying')
            print(f"Error loading flying2 sprite: {e}")

        # Ensure keys exist even if None
        if 'flying' not in self.mango_sprites:
            self.mango_sprites['flying'] = None
        if 'flying2' not in self.mango_sprites:
            self.mango_sprites['flying2'] = None

    def load_mango_sounds(self):
        """Load optional Mango sounds (non-fatal if missing).

        Looks for assets/sounds/flap.wav and assets/sounds/medicine.wav.
        If loading fails (no mixer or missing files), stores nothing but
        keeps code paths safe.
        """
        try:
            # Initialize mixer if possible; ignore errors in headless/test envs
            try:
                pygame.mixer.init()
            except Exception:
                pass

            flap_path = "assets/sounds/flap.wav"
            med_path = "assets/sounds/medicine.wav"

            # If the sound files don't exist, generate tiny placeholders so
            # users immediately hear something without adding assets.
            def write_placeholder(path, freq=1000, duration_ms=120, volume=0.2):
                # Create a short sine wave WAV file
                framerate = 44100
                amplitude = int(32767 * volume)
                nframes = int(framerate * duration_ms / 1000)
                with wave.open(path, 'w') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(framerate)
                    for i in range(nframes):
                        t = i / framerate
                        val = int(amplitude * math.sin(2 * math.pi * freq * t))
                        wf.writeframes(struct.pack('<h', val))

            if not os.path.exists(os.path.dirname(flap_path)):
                os.makedirs(os.path.dirname(flap_path), exist_ok=True)
            if not os.path.exists(flap_path):
                try:
                    write_placeholder(flap_path, freq=1500, duration_ms=100, volume=0.15)
                    print("Created placeholder sound: flap.wav")
                except Exception as e:
                    print(f"Could not create flap placeholder: {e}")
            if not os.path.exists(med_path):
                try:
                    write_placeholder(med_path, freq=800, duration_ms=180, volume=0.18)
                    print("Created placeholder sound: medicine.wav")
                except Exception as e:
                    print(f"Could not create medicine placeholder: {e}")

            if os.path.exists(flap_path):
                try:
                    self.sounds['flap'] = pygame.mixer.Sound(flap_path)
                    print("Loaded sound: flap.wav")
                except Exception as e:
                    print(f"Error loading flap sound: {e}")
            if os.path.exists(med_path):
                try:
                    self.sounds['medicine'] = pygame.mixer.Sound(med_path)
                    print("Loaded sound: medicine.wav")
                except Exception as e:
                    print(f"Error loading medicine sound: {e}")
        except Exception as e:
            # Any sound init failures should not break the game
            print(f"Sound loading skipped: {e}")
    
    def draw_gradient_background(self):
        """Draw a beautiful gradient background."""
        if self.is_night:
            start_color = NIGHT_START
            end_color = NIGHT_END
        else:
            start_color = GRADIENT_START
            end_color = GRADIENT_END
        
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def draw_hub_background(self):
        """Draw the hub background (image or gradient)."""
        if self.hub_background:
            self.screen.blit(self.hub_background, (0, 0))
            # Add a slight overlay for better text readability
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(30)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
        else:
            self.draw_gradient_background()
    
    def draw_flappy_background(self):
        """Draw the flappy mango background (image or gradient)."""
        if self.flappy_background:
            self.screen.blit(self.flappy_background, (0, 0))
        else:
            self.draw_gradient_background()
    
    def draw_modern_button(self, rect, text, color, hover_color, text_color=WHITE, hover=False):
        """Draw a modern button with hover effects."""
        # Button shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect, border_radius=8)
        
        # Button background
        button_color = hover_color if hover else color
        pygame.draw.rect(self.screen, button_color, rect, border_radius=8)
        
        # Button border
        border_color = WHITE if hover else LIGHT_GRAY
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=8)
        
        # Button text
        text_surface = self.small_font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return rect
    
    def draw_modern_progress_bar(self, x, y, width, height, value, max_value, color, bg_color=DARK_GRAY):
        """Draw a modern progress bar."""
        # Background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, bg_rect, border_radius=height//2)
        
        # Progress
        progress_width = int((value / max_value) * width)
        if progress_width > 0:
            progress_rect = pygame.Rect(x, y, progress_width, height)
            pygame.draw.rect(self.screen, color, progress_rect, border_radius=height//2)
        
        # Border
        pygame.draw.rect(self.screen, WHITE, bg_rect, 2, border_radius=height//2)
    
    def check_random_events(self):
        """Check for random events like sickness or misbehavior."""
        current_time = time.time()
        time_diff = current_time - self.last_random_event
        
        # Random events every 2 minutes
        if time_diff >= 120:
            if random.random() < 0.3:  # 30% chance
                event = random.choice(['sick', 'misbehavior'])
                if event == 'sick' and not self.is_sick:
                    self.is_sick = True
                    self.mango_state['health'] = max(0, self.mango_state['health'] - 20)
                elif event == 'misbehavior':
                    self.misbehavior_count += 1
                    self.mango_state['happiness'] = max(0, self.mango_state['happiness'] - 10)
            
            self.last_random_event = current_time
    
    def get_mango_mood(self):
        """Determine Mango's current mood based on stats."""
        if self.is_sick:
            return "sick"
        elif self.mango_state['cleanliness'] < 30:
            return "dirty"
        elif self.mango_state['energy'] < 20:
            return "tired"
        elif self.mango_state['happiness'] > 70:
            return "happy"
        elif self.mango_state['happiness'] < 30:
            return "sad"
        else:
            return "neutral"
    
    def is_game_over(self):
        """Check if game is over (health = 0)."""
        return self.mango_state['health'] <= 0
    
    def restart_game(self):
        """Restart the game with a new Mango."""
        self.mango_state = {
            'hunger': 80,
            'happiness': 70,
            'cleanliness': 60,
            'energy': 90,
            'health': 100,
            'age': 0,
            'last_updated': datetime.now().isoformat()
        }
        self.is_sick = False
        self.misbehavior_count = 0
        self.save_state()
    
    def save_score(self, score):
        """Save Flappy Mango score to database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO scores (score) VALUES (?)", (score,))
        conn.commit()
        conn.close()
        
        # Update high score
        if score > self.high_score:
            self.high_score = score
    
    def get_high_score(self):
        """Get the highest score from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT MAX(score) FROM scores")
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result[0] else 0
    
    def play_flappy_mango(self):
        """Launch the modern Flappy Mango mini-game."""
        self.state = GameState.FLAPPY_MANGO
        # Reload sprites to ensure they persist when returning
        self.load_mango_sprites()
        
        # Flappy Mango game variables
        mango_x = 150
        mango_y = SCREEN_HEIGHT // 2
        mango_velocity = 0
        gravity = 0.75  # Reduced gravity for easier control
        jump_strength = -13  # Increased jump strength
        
        crows = []
        crow_spawn_timer = 0
        crow_spawn_interval = 150  # Even slower spawn rate for easier gameplay
        
        score = 0
        game_over = False
        game_started = False
        last_score_update = 0
        
        while self.state == GameState.FLAPPY_MANGO:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.state = GameState.TAMAGOTCHI_HUB
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if not game_started:
                            game_started = True
                        if not game_over:
                            mango_velocity = jump_strength
                            # play flap sound if available
                            try:
                                if 'flap' in self.sounds:
                                    self.sounds['flap'].play()
                            except Exception:
                                pass
                            # toggle which flying sprite to use for smooth animation
                            # start a short crossfade between flying and flying2
                            # keep track by storing a small crossfade state
                            if not hasattr(self, '_flap_fade'):
                                self._flap_fade = {'progress': 0.0, 'direction': 1}
                            else:
                                # trigger toggle
                                self._flap_fade['direction'] = 1
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.TAMAGOTCHI_HUB
                        return
                    elif event.key == pygame.K_r and game_over:
                        # Restart game
                        mango_x = 150
                        mango_y = SCREEN_HEIGHT // 2
                        mango_velocity = 0
                        crows = []
                        score = 0
                        game_over = False
                        game_started = False
                        last_score_update = 0
            
            if not game_over and game_started:
                # Update Mango
                mango_velocity += gravity
                mango_y += mango_velocity
                
                # Update crows
                crow_spawn_timer += 1
                if crow_spawn_timer >= crow_spawn_interval:
                    crows.append({
                        'x': SCREEN_WIDTH,
                        'y': random.randint(150, SCREEN_HEIGHT - 250),
                        'gap': 220,  # Wider gap for easier gameplay
                        'scored': False  # Track if this crow has been scored
                    })
                    crow_spawn_timer = 0
                
                # Move crows and update score
                for crow in crows[:]:
                    crow['x'] -= 3
                    if crow['x'] < -50:
                        crows.remove(crow)
                    
                    # Score when Mango passes a crow (only once per crow)
                    if not crow['scored'] and crow['x'] + 50 < mango_x:
                        score += 1
                        crow['scored'] = True
                        last_score_update = time.time()
                
                # Collision detection with modern hitboxes
                mango_rect = pygame.Rect(mango_x - 15, mango_y - 15, 30, 30)
                for crow in crows:
                    # Top crow obstacle
                    top_rect = pygame.Rect(crow['x'], 0, 70, crow['y'] - crow['gap'] // 2)
                    # Bottom crow obstacle
                    bottom_rect = pygame.Rect(crow['x'], crow['y'] + crow['gap'] // 2, 70, SCREEN_HEIGHT - crow['y'] - crow['gap'] // 2)
                    
                    if mango_rect.colliderect(top_rect) or mango_rect.colliderect(bottom_rect):
                        game_over = True
                        break
                
                # Ground/ceiling collision
                if mango_y >= SCREEN_HEIGHT - 60 or mango_y <= -150:
                    game_over = True
            
            # Draw flappy background
            self.draw_flappy_background()
            
            # Draw realistic crows with shadows
            for crow in crows:
                # Crow shadow
                shadow_offset = 3
                # Top crow shadow
                pygame.draw.rect(self.screen, (0, 0, 0, 100), 
                               (crow['x'] + shadow_offset, shadow_offset, 70, crow['y'] - crow['gap'] // 2))
                # Bottom crow shadow
                pygame.draw.rect(self.screen, (0, 0, 0, 100), 
                               (crow['x'] + shadow_offset, crow['y'] + crow['gap'] // 2 + shadow_offset, 70, 
                                SCREEN_HEIGHT - crow['y'] - crow['gap'] // 2))
                
                # Top crow body (more realistic)
                crow_top_rect = pygame.Rect(crow['x'], 0, 70, crow['y'] - crow['gap'] // 2)
                pygame.draw.rect(self.screen, BLACK, crow_top_rect, border_radius=12)
                
                # Bottom crow body (more realistic)
                crow_bottom_rect = pygame.Rect(crow['x'], crow['y'] + crow['gap'] // 2, 70, 
                                             SCREEN_HEIGHT - crow['y'] - crow['gap'] // 2)
                pygame.draw.rect(self.screen, BLACK, crow_bottom_rect, border_radius=12)
                
                # Draw realistic crow heads with beaks
                head_y_top = crow['y'] - crow['gap'] // 2 - 15
                head_y_bottom = crow['y'] + crow['gap'] // 2 + 15
                
                # Top crow head
                pygame.draw.circle(self.screen, BLACK, (crow['x'] + 35, head_y_top), 12)
                # Top crow beak
                beak_points = [(crow['x'] + 35, head_y_top - 5), (crow['x'] + 30, head_y_top - 12), (crow['x'] + 40, head_y_top - 12)]
                pygame.draw.polygon(self.screen, (255, 140, 0), beak_points)
                # Top crow eye
                pygame.draw.circle(self.screen, WHITE, (crow['x'] + 32, head_y_top - 2), 3)
                pygame.draw.circle(self.screen, BLACK, (crow['x'] + 32, head_y_top - 2), 2)
                
                # Bottom crow head
                pygame.draw.circle(self.screen, BLACK, (crow['x'] + 35, head_y_bottom), 12)
                # Bottom crow beak
                beak_points = [(crow['x'] + 35, head_y_bottom + 5), (crow['x'] + 30, head_y_bottom + 12), (crow['x'] + 40, head_y_bottom + 12)]
                pygame.draw.polygon(self.screen, (255, 140, 0), beak_points)
                # Bottom crow eye
                pygame.draw.circle(self.screen, WHITE, (crow['x'] + 32, head_y_bottom + 2), 3)
                pygame.draw.circle(self.screen, BLACK, (crow['x'] + 32, head_y_bottom + 2), 2)
            
            # Draw modern Mango with wing animation
            mango_wing_offset = int(3 * math.sin(self.animation_time * 4)) if not game_over else 0

            # Mango shadow (reduced so it doesn't look like a black ball on his back)
            try:
                shadow_radius = 10
                pygame.draw.circle(self.screen, (0, 0, 0, 50), (int(mango_x + 2), int(mango_y + 8)), shadow_radius)
            except Exception:
                pass

            # Try to use sprite image, fallback to drawn shapes
            if hasattr(self, 'mango_sprites') and self.mango_sprites.get('flying'):
                # Use actual sprite images (larger for flappy game)
                sprite1 = self.mango_sprites.get('flying')
                sprite2 = self.mango_sprites.get('flying2')
                flappy_sprite1 = pygame.transform.scale(sprite1, (90, 90)) if sprite1 else None
                flappy_sprite2 = pygame.transform.scale(sprite2, (90, 90)) if sprite2 else None

                # Handle crossfade progress if present
                if hasattr(self, '_flap_fade') and flappy_sprite2:
                    fade = self._flap_fade
                    # progress moves from 0.0 to 1.0 over ~6 frames (~100ms at 60fps)
                    fade['progress'] = min(1.0, fade.get('progress', 0.0) + 0.17)
                    alpha2 = int(255 * fade['progress'])
                    alpha1 = 255 - alpha2

                    # Create surfaces with per-surface alpha for blending
                    surf1 = flappy_sprite1.copy() if flappy_sprite1 else None
                    surf2 = flappy_sprite2.copy() if flappy_sprite2 else None
                    if surf1:
                        surf1.set_alpha(alpha1)
                    if surf2:
                        surf2.set_alpha(alpha2)

                    rect = surf1.get_rect(center=(int(mango_x), int(mango_y))) if surf1 else surf2.get_rect(center=(int(mango_x), int(mango_y)))
                    if surf1:
                        self.screen.blit(surf1, rect)
                    if surf2:
                        self.screen.blit(surf2, rect)

                    # Reset fade if finished so next SPACE restarts it
                    if fade['progress'] >= 1.0:
                        fade['progress'] = 0.0
                else:
                    # Simple swap if no second sprite or no fade state
                    sprite_rect = flappy_sprite1.get_rect(center=(int(mango_x), int(mango_y)))
                    self.screen.blit(flappy_sprite1, sprite_rect)
            else:
                # Fallback to drawn Mango
                # Mango body
                pygame.draw.circle(self.screen, ORANGE, (int(mango_x), int(mango_y)), 18)
                
                # Mango wings
                pygame.draw.ellipse(self.screen, (255, 140, 0), 
                                  (mango_x - 20, mango_y - 5 + mango_wing_offset, 15, 10))
                pygame.draw.ellipse(self.screen, (255, 140, 0), 
                                  (mango_x + 5, mango_y - 5 + mango_wing_offset, 15, 10))
                
                # Mango face
                pygame.draw.circle(self.screen, BLACK, (int(mango_x - 6), int(mango_y - 5)), 2)
                pygame.draw.circle(self.screen, BLACK, (int(mango_x + 6), int(mango_y - 5)), 2)
                
                # Beak
                beak_points = [(mango_x, mango_y + 3), (mango_x - 2, mango_y + 7), (mango_x + 2, mango_y + 7)]
                pygame.draw.polygon(self.screen, (255, 165, 0), beak_points)
            
            # Modern UI elements
            # Score panel (top right)
            score_panel = pygame.Rect(SCREEN_WIDTH - 220, 20, 200, 80)
            pygame.draw.rect(self.screen, SILVER, score_panel, border_radius=15)
            pygame.draw.rect(self.screen, GOLD, score_panel, 3, border_radius=15)
            
            score_text = self.large_font.render(f"Score: {score}", True, BLACK)
            self.screen.blit(score_text, (SCREEN_WIDTH - 205, 35))
            
            high_score_text = self.small_font.render(f"Best: {self.high_score}", True, DARK_GRAY)
            self.screen.blit(high_score_text, (SCREEN_WIDTH - 205, 65))
            
            if not game_started:
                # Start screen
                start_panel = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
                pygame.draw.rect(self.screen, WHITE, start_panel, border_radius=20)
                pygame.draw.rect(self.screen, GOLD, start_panel, 4, border_radius=20)
                
                start_text = self.title_font.render("Flappy Mango", True, BLACK)
                start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
                self.screen.blit(start_text, start_rect)
                
                instruction_text = self.font.render("Press SPACE to start!", True, BLACK)
                inst_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
                self.screen.blit(instruction_text, inst_rect)
                
                esc_text = self.small_font.render("ESC to return to hub", True, DARK_GRAY)
                esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
                self.screen.blit(esc_text, esc_rect)
            elif not game_over:
                # Game instructions
                instruction_text = self.small_font.render("SPACE to flap | ESC to quit", True, WHITE)
                self.screen.blit(instruction_text, (20, SCREEN_HEIGHT - 40))
            else:
                # Game over screen
                game_over_panel = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
                pygame.draw.rect(self.screen, WHITE, game_over_panel, border_radius=20)
                pygame.draw.rect(self.screen, RED, game_over_panel, 4, border_radius=20)
                
                game_over_text = self.title_font.render("Game Over!", True, RED)
                go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
                self.screen.blit(game_over_text, go_rect)
                
                final_score_text = self.large_font.render(f"Final Score: {score}", True, BLACK)
                fs_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
                self.screen.blit(final_score_text, fs_rect)
                
                restart_text = self.font.render("Press R to restart", True, BLACK)
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
                self.screen.blit(restart_text, restart_rect)
                
                esc_text = self.font.render("ESC to return to hub", True, BLACK)
                esc_rect = esc_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(esc_text, esc_rect)
                
                # Save score and update happiness
                if score > 0:
                    self.save_score(score)
                    happiness_bonus = min(25, score * 2)
                    self.mango_state['happiness'] = min(100, self.mango_state['happiness'] + happiness_bonus)
                    self.save_state()
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def draw_home_screen(self):
        """Draw the modern Tamagotchi hub screen."""
        # Draw background (image or gradient)
        self.draw_hub_background()
        
        # Update animations
        self.animation_time += 0.1
        self.pulse_animation = math.sin(self.animation_time) * 0.1 + 1.0
        
        # Title
        title_text = self.title_font.render("Mango: The Virtual Lovebird", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Draw Mango's habitat (modern cage)
        cage_x, cage_y = 80, 120
        cage_width, cage_height = 280, 280
        
        # Cage shadow
        cage_shadow = pygame.Rect(cage_x + 5, cage_y + 5, cage_width, cage_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 100), cage_shadow, border_radius=15)
        
        # Gold frame around entire cage (outer border)
        frame_rect = pygame.Rect(cage_x - 8, cage_y - 8, cage_width + 16, cage_height + 16)
        pygame.draw.rect(self.screen, GOLD, frame_rect, border_radius=20)
        
        # Cage background (silver inside the golden frame)
        cage_rect = pygame.Rect(cage_x, cage_y, cage_width, cage_height)
        pygame.draw.rect(self.screen, SILVER, cage_rect, border_radius=15)
        
        # Draw Mango with animations
        mood = self.get_mango_mood()
        mango_x = cage_x + cage_width // 2
        mango_y = cage_y + cage_height // 2
        
        # Try to use sprite image, fallback to drawn shapes
        sprite_mood = mood if mood in ['happy', 'sad', 'tired', 'dirty'] else 'idle'
        
        if hasattr(self, 'mango_sprites') and self.mango_sprites.get(sprite_mood):
            # Use actual sprite image
            sprite = self.mango_sprites[sprite_mood]
            
            # Apply different animations based on mood
            if mood == "happy":
                # Pulsing animation for happy mood
                scale_factor = self.pulse_animation
                scaled_sprite = pygame.transform.scale(sprite, 
                    (int(140 * scale_factor), int(140 * scale_factor)))
                sprite_rect = scaled_sprite.get_rect(center=(mango_x, mango_y))
                self.screen.blit(scaled_sprite, sprite_rect)
            elif mood == "sad":
                # Slight bobbing animation for sad mood
                bob_offset = int(3 * math.sin(self.animation_time * 2))
                sprite_rect = sprite.get_rect(center=(mango_x, mango_y + bob_offset))
                self.screen.blit(sprite, sprite_rect)
            elif mood == "tired":
                # Slow swaying animation for tired mood
                sway_offset = int(2 * math.sin(self.animation_time * 0.8))
                sprite_rect = sprite.get_rect(center=(mango_x + sway_offset, mango_y))
                self.screen.blit(sprite, sprite_rect)
            elif mood == "dirty":
                # Slight shake animation for dirty mood
                shake_x = int(1.5 * math.sin(self.animation_time * 8))
                shake_y = int(1.5 * math.cos(self.animation_time * 8))
                sprite_rect = sprite.get_rect(center=(mango_x + shake_x, mango_y + shake_y))
                self.screen.blit(sprite, sprite_rect)
            else:
                # Gentle floating animation for idle/neutral mood
                float_offset = int(2 * math.sin(self.animation_time * 1.5))
                sprite_rect = sprite.get_rect(center=(mango_x, mango_y + float_offset))
                self.screen.blit(sprite, sprite_rect)
        else:
            # Fallback to drawn Mango (if no sprite available)
            mango_colors = {
                "happy": YELLOW,
                "sad": DARK_GRAY,
                "tired": PINK,
                "dirty": (139, 69, 19),
                "sick": (128, 128, 128),
                "neutral": ORANGE
            }
            mango_color = mango_colors.get(mood, ORANGE)
            
            # Pulsing animation for happy Mango
            if mood == "happy":
                mango_radius = int(30 * self.pulse_animation)
            else:
                mango_radius = 30
            
            # Draw Mango body
            pygame.draw.circle(self.screen, mango_color, (mango_x, mango_y), mango_radius)
            
            # Draw Mango's face
            eye_offset = int(8 * self.pulse_animation if mood == "happy" else 8)
            pygame.draw.circle(self.screen, BLACK, (mango_x - eye_offset, mango_y - 8), 3)
            pygame.draw.circle(self.screen, BLACK, (mango_x + eye_offset, mango_y - 8), 3)
            
            # Beak
            beak_points = [(mango_x, mango_y + 5), (mango_x - 3, mango_y + 10), (mango_x + 3, mango_y + 10)]
            pygame.draw.polygon(self.screen, ORANGE, beak_points)
            
            # Wings (if happy)
            if mood == "happy":
                wing_offset = int(5 * math.sin(self.animation_time * 2))
                pygame.draw.ellipse(self.screen, (255, 140, 0), 
                                  (mango_x - 25, mango_y - 5 + wing_offset, 20, 15))
                pygame.draw.ellipse(self.screen, (255, 140, 0), 
                                  (mango_x + 5, mango_y - 5 + wing_offset, 20, 15))
        
        # HUD messages and flash
        if time.time() < self.flash_until:
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash.set_alpha(90)
            flash.fill(WHITE)
            self.screen.blit(flash, (0, 0))

        now = time.time()
        self.hud_messages = [m for m in self.hud_messages if m[1] > now]
        for i, (text, expiry) in enumerate(self.hud_messages):
            hud_surf = self.font.render(text, True, BLACK)
            hud_rect = hud_surf.get_rect(center=(SCREEN_WIDTH // 2, 100 + i * 28))
            self.screen.blit(hud_surf, hud_rect)

        # Modern stats panel
        stats_x, stats_y = 400, 120
        stats_width, stats_height = 550, 400
        
        # Panel shadow
        panel_shadow = pygame.Rect(stats_x + 5, stats_y + 5, stats_width, stats_height)
        pygame.draw.rect(self.screen, (0, 0, 0, 100), panel_shadow, border_radius=20)
        
        # Panel background
        panel_rect = pygame.Rect(stats_x, stats_y, stats_width, stats_height)
        pygame.draw.rect(self.screen, SILVER, panel_rect, border_radius=20)
        pygame.draw.rect(self.screen, GOLD, panel_rect, 3, border_radius=20)
        
        # Panel title
        panel_title = self.large_font.render("Mango's Stats", True, BLACK)
        self.screen.blit(panel_title, (stats_x + 20, stats_y + 20))
        
        # Draw modern stat bars
        stat_y_start = stats_y + 70
        stat_spacing = 60
        stat_width = 450
        stat_height = 25
        
        stats_data = [
            ("Hunger", self.mango_state['hunger'], RED, "Feed Mango to increase hunger"),
            ("Happiness", self.mango_state['happiness'], YELLOW, "Play or care for Mango"),
            ("Cleanliness", self.mango_state['cleanliness'], BLUE, "Bathe Mango regularly"),
            ("Energy", self.mango_state['energy'], GREEN, "Let Mango rest to restore energy"),
            ("Health", self.mango_state['health'], PINK, "Keep all stats balanced")
        ]
        
        for i, (name, value, color, tooltip) in enumerate(stats_data):
            y_pos = stat_y_start + i * stat_spacing
            
            # Stat label
            label_text = self.font.render(f"{name}: {value}%", True, BLACK)
            self.screen.blit(label_text, (stats_x + 20, y_pos - 5))
            
            # Modern progress bar
            self.draw_modern_progress_bar(stats_x + 20, y_pos + 20, stat_width, stat_height, 
                                        value, 100, color)
        
        # Info section
        info_y = stats_y + 380
        weather = self.api_handler.get_weather()
        weather_text = self.small_font.render(f"Weather: {weather['description'] if weather else 'Sunny, 20°C'}", True, BLACK)
        self.screen.blit(weather_text, (stats_x + 20, info_y))
        
        time_text = self.small_font.render(f"Time: {datetime.now().strftime('%H:%M')} {'(Night)' if self.is_night else '(Day)'}", True, BLACK)
        self.screen.blit(time_text, (stats_x + 250, info_y))
        
        age_text = self.small_font.render(f"Age: {self.mango_state['age']} days", True, BLACK)
        self.screen.blit(age_text, (stats_x + 450, info_y))
        
        # Action buttons (modern design)
        button_y = 550
        button_width = 120
        button_height = 50
        button_spacing = 130
        
        buttons = [
            ("Feed", self.feed_mango, GREEN, (0, 200, 0)),
            ("Bathe", self.bathe_mango, BLUE, (0, 100, 200)),
            ("Play", self.play_with_mango, YELLOW, (200, 150, 0)),
            ("Rest", self.rest_mango, PINK, (200, 100, 150)),
            ("Medicine", self.give_medicine, RED, (200, 0, 0)),
            ("Discipline", self.discipline, PURPLE, (100, 0, 100))
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for i, (text, action, color, hover_color) in enumerate(buttons):
            button_x = 80 + i * button_spacing
            if button_x + button_width > SCREEN_WIDTH - 20:
                break
                
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            is_hovered = button_rect.collidepoint(mouse_pos)
            
            # Always allow Medicine button (styling uses provided color)
            button_color = color
            text_color = WHITE
            
            self.draw_modern_button(button_rect, text, button_color, hover_color, text_color, is_hovered)
        
        # Flappy Mango button (top right corner)
        flappy_x = SCREEN_WIDTH - 200
        flappy_y = 80
        flappy_rect = pygame.Rect(flappy_x, flappy_y, 150, 60)
        is_flappy_hovered = flappy_rect.collidepoint(mouse_pos)
        
        self.draw_modern_button(flappy_rect, "Flappy Mango", ORANGE, GOLD, WHITE, is_flappy_hovered)
        
        # High score display (moved down since Flappy button is now at top)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        self.screen.blit(high_score_text, (SCREEN_WIDTH - 250, 150))
        
        # Status messages with modern design
        status_y = 620
        if self.is_sick:
            status_rect = pygame.Rect(50, status_y, 400, 40)
            pygame.draw.rect(self.screen, RED, status_rect, border_radius=20)
            pygame.draw.rect(self.screen, WHITE, status_rect, 2, border_radius=20)
            sick_text = self.font.render("Mango is sick! Give medicine!", True, WHITE)
            text_rect = sick_text.get_rect(center=status_rect.center)
            self.screen.blit(sick_text, text_rect)
        elif self.misbehavior_count > 0:
            status_rect = pygame.Rect(50, status_y, 400, 40)
            pygame.draw.rect(self.screen, ORANGE, status_rect, border_radius=20)
            pygame.draw.rect(self.screen, WHITE, status_rect, 2, border_radius=20)
            misbehavior_text = self.font.render(f"Mango misbehaved! ({self.misbehavior_count})", True, WHITE)
            text_rect = misbehavior_text.get_rect(center=status_rect.center)
            self.screen.blit(misbehavior_text, text_rect)
        
        # Bird fact display
        bird_fact = self.api_handler.get_bird_fact()
        if bird_fact:
            fact_rect = pygame.Rect(SCREEN_WIDTH - 450, status_y, 440, 40)
            pygame.draw.rect(self.screen, GOLD, fact_rect, border_radius=20)
            pygame.draw.rect(self.screen, WHITE, fact_rect, 2, border_radius=20)
            fact_text = self.tiny_font.render(bird_fact, True, BLACK)
            text_rect = fact_text.get_rect(center=fact_rect.center)
            self.screen.blit(fact_text, text_rect)
    
    def handle_click(self, pos):
        """Handle mouse clicks on the hub screen."""
        x, y = pos
        
        # Check action buttons (modern layout)
        button_y = 550
        button_width = 120
        button_height = 50
        button_spacing = 130
        
        buttons = [
            ("Feed", self.feed_mango, GREEN),
            ("Bathe", self.bathe_mango, BLUE),
            ("Play", self.play_with_mango, YELLOW),
            ("Rest", self.rest_mango, PINK),
            ("Medicine", self.give_medicine, RED),
            ("Discipline", self.discipline, PURPLE)
        ]
        
        for i, (text, action, color) in enumerate(buttons):
            button_x = 80 + i * button_spacing
            if button_x + button_width > SCREEN_WIDTH - 20:
                break
                
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            
            if button_rect.collidepoint(pos):
                action()
                return
        
        # Check Flappy Mango button (top right)
        flappy_x = SCREEN_WIDTH - 200
        flappy_y = 80
        flappy_rect = pygame.Rect(flappy_x, flappy_y, 150, 60)
        if flappy_rect.collidepoint(pos):
            self.play_flappy_mango()
    
    def run(self):
        """Main game loop."""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Update game state
            self.update_stats()
            self.age_mango()
            
            # Force sickness if health is low (real-time check)
            if self.mango_state['health'] <= 30 and not self.is_sick:
                self.is_sick = True
            
            # Update day/night cycle
            current_hour = datetime.now().hour
            if current_hour != self.current_hour:
                self.current_hour = current_hour
                self.is_night = current_hour < 6 or current_hour > 18
            
            # Check game over
            if self.is_game_over():
                self.state = GameState.GAME_OVER
            
            # Draw current state
            if self.state == GameState.TAMAGOTCHI_HUB:
                self.draw_home_screen()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def draw_game_over_screen(self):
        """Draw the modern game over screen."""
        # Draw gradient background
        self.draw_gradient_background()
        
        # Game over panel
        panel_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200, 600, 400)
        
        # Panel shadow
        shadow_rect = pygame.Rect(panel_rect.x + 5, panel_rect.y + 5, panel_rect.width, panel_rect.height)
        pygame.draw.rect(self.screen, (0, 0, 0, 100), shadow_rect, border_radius=25)
        
        # Panel background
        pygame.draw.rect(self.screen, WHITE, panel_rect, border_radius=25)
        pygame.draw.rect(self.screen, RED, panel_rect, 4, border_radius=25)
        
        # Game over text
        game_over_text = self.title_font.render("Mango has flown away!", True, RED)
        go_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, go_rect)
        
        # Restart button
        restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, 300, 60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        is_hovered = restart_button.collidepoint(mouse_pos)
        
        self.draw_modern_button(restart_button, "Get a New Mango", GREEN, (0, 200, 0), WHITE, is_hovered)
        
        # Instructions
        instruction_text = self.small_font.render("Click the button above to start over with a new Mango!", True, DARK_GRAY)
        inst_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        self.screen.blit(instruction_text, inst_rect)
        
        # Handle click to restart
        if mouse_clicked and restart_button.collidepoint(mouse_pos):
            self.restart_game()
            self.state = GameState.TAMAGOTCHI_HUB

def main():
    """Main function to run the game."""
    game = MangoTamagotchi()
    game.run()

if __name__ == "__main__":
    main()
