"""Quick audio smoke test for AudioManager.

Run this from the project root with your virtualenv activated. It will:
- create an AudioManager using a lightweight owner object
- ensure audio is ready
- load sounds (placeholders created if missing)
- play the 'flap' SFX, wait 1s, then start 'forest' music for 4s and stop
"""
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from audio import AudioManager


class DummyOwner:
    def __init__(self):
        # minimal attributes used by AudioManager
        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        self.sounds = {}
        self._music_files = {}


def main():
    owner = DummyOwner()
    am = AudioManager(owner)
    ok = am.ensure_audio_ready()
    print(f"ensure_audio_ready -> {ok}")
    am.load_sounds()
    print("Loaded sounds:", sorted(list(am.sounds.keys())))

    print("Playing 'flap' sfx...")
    am.play_sfx('flap')
    time.sleep(1.0)

    print("Starting 'forest' music for 4s...")
    am.play_music('forest')
    time.sleep(4.0)
    print("Stopping music")
    am.stop_music()


if __name__ == '__main__':
    main()
