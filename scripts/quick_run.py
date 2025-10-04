#!/usr/bin/env python3
"""Quick smoke-run for Mango: draw the hub screen and exit fast.

This avoids the full game loop and heavy interactions so you can verify
startup and rendering quickly while iterating.
"""
import sys
import time
import os
import pygame

# Ensure the repository root is on sys.path so imports like `project` resolve
root = os.path.dirname(os.path.dirname(__file__))
if root not in sys.path:
    sys.path.insert(0, root)

try:
    from project import MangoTamagotchi
except Exception as e:
    print('Failed to import project:', e)
    raise


def main():
    # Create the game instance (this will initialize subsystems).
    g = MangoTamagotchi()

    # Draw one frame of the hub and save a screenshot for quick verification.
    try:
        g.draw_home_screen()
        # Allow a couple ticks for fonts/surfaces to settle
        for _ in range(3):
            pygame.event.pump()
            g.clock.tick(60)
            time.sleep(0.02)
        out = 'smoke_screenshot.png'
        try:
            pygame.image.save(g.screen, out)
            print('Saved smoke screenshot to', out)
        except Exception as e:
            print('Could not save screenshot:', e)
    except Exception as e:
        print('Error while drawing hub screen:', e)
    finally:
        try:
            pygame.quit()
        except Exception:
            pass


if __name__ == '__main__':
    main()
