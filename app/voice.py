"""
Voice input and output handling for RTO AI Enrollment System
"""
import os
import tempfile
import platform
import subprocess
import threading
from openai import OpenAI as OpenAIClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client for voice features
#openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"))


class VoiceOutputHandler:
    """Handle voice output using OpenAI TTS API with female voice"""

    def __init__(self):
        self.voice = "nova"  # OpenAI female voice: "nova" or "shimmer"
        self.use_openai_tts = True
        self._is_playing = False
        self._play_lock = threading.Lock()
        self._check_openai_available()

    def _check_openai_available(self):
        """Check if OpenAI TTS is available"""
        if not openai_client.api_key:
            self.use_openai_tts = False
            # Fallback to pyttsx3 if OpenAI not available
            try:
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                voices = self.tts_engine.getProperty('voices')
                if len(voices) > 1:
                    self.tts_engine.setProperty('voice', voices[1].id)  # Usually female
                self.use_openai_tts = False
            except:
                self.tts_engine = None

    def speak(self, text, async_mode=False):
        """Convert text to speech and play it using OpenAI TTS
        async_mode=False ensures sequential playback (prevents overlapping)
        """
        # Wait if another audio is playing
        if self._play_lock:
            self._play_lock.acquire()

        try:
            if self.use_openai_tts:
                result = self._speak_openai(text, async_mode)
            else:
                result = self._speak_pyttsx3(text, async_mode)
            return result
        finally:
            if self._play_lock:
                self._play_lock.release()

    def _speak_openai(self, text, async_mode):
        """Use OpenAI TTS API for high-quality female voice"""
        try:
            import tempfile

            # Generate speech using OpenAI TTS
            response = openai_client.audio.speech.create(
                model="tts-1",
                voice=self.voice,  # "nova" is a high-quality female voice
                input=text,
                speed=1.0
            )

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_path = tmp_file.name
                # Write audio content to file (using iter_bytes for proper streaming)
                with open(tmp_path, 'wb') as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)

            # Play the audio file (always synchronous to prevent overlapping)
            self._is_playing = True
            try:
                self._play_audio_file(tmp_path)
            finally:
                self._is_playing = False
                # Clean up after playback
                import time
                time.sleep(0.1)  # Small delay to ensure file is released
                if os.path.exists(tmp_path):
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass  # File might be in use, will be cleaned up later
            return True

        except Exception as e:
            print(f"⚠️  OpenAI TTS error: {str(e)}")
            import traceback
            traceback.print_exc()
            # Fallback to pyttsx3 if available
            if hasattr(self, 'tts_engine') and self.tts_engine:
                return self._speak_pyttsx3(text, async_mode)
            return False

    def _play_audio_file(self, file_path):
        """Play audio file using reliable Python library"""
        if not os.path.exists(file_path):
            print(f"⚠️  Audio file not found: {file_path}")
            return False

        try:
            # Try using pydub with simpleaudio (most reliable)
            try:
                from pydub import AudioSegment
                from pydub.playback import play
                audio = AudioSegment.from_mp3(file_path)
                play(audio)
                return True
            except ImportError:
                pass
            except Exception as e:
                pass

            # Try using pygame (good cross-platform support)
            try:
                import pygame
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    import pygame.time
                    pygame.time.Clock().tick(10)
                pygame.mixer.quit()
                return True
            except ImportError:
                pass
            except Exception as e:
                pass

            # Try using playsound
            try:
                from playsound import playsound
                playsound(file_path, block=True)
                return True
            except ImportError:
                pass
            except Exception as e:
                pass

            # Fallback to system commands
            import subprocess
            import platform
            system = platform.system()
            if system == "Linux":
                # Try multiple Linux audio players
                for player in ["mpg123", "mpg321", "ffplay", "aplay", "paplay"]:
                    try:
                        result = subprocess.run([player, file_path], check=False,
                                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                        if result.returncode == 0:
                            return True
                    except:
                        continue
            elif system == "Darwin":  # macOS
                result = subprocess.run(["afplay", file_path], check=False,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                return result.returncode == 0
            elif system == "Windows":
                result = subprocess.run(["start", file_path], shell=True, check=False,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
                return result.returncode == 0

            print("⚠️  No audio playback method available. Please install pydub, pygame, or system audio player.")
            return False
        except Exception as e:
            print(f"⚠️  Audio playback error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def _speak_pyttsx3(self, text, async_mode):
        """Fallback to pyttsx3 if OpenAI not available"""
        if not hasattr(self, 'tts_engine') or self.tts_engine is None:
            return False

        try:
            # Always synchronous to prevent overlapping
            self._is_playing = True
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self._is_playing = False
            return True
        except Exception as e:
            self._is_playing = False
            return False

    def save_to_file(self, text, filename):
        """Save speech to audio file"""
        if self.use_openai_tts:
            try:
                response = openai_client.audio.speech.create(
                    model="tts-1",
                    voice=self.voice,
                    input=text,
                    speed=1.0
                )
                # Use with_streaming_response for proper streaming
                with open(filename, 'wb') as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
                return True
            except Exception as e:
                return False
        elif hasattr(self, 'tts_engine') and self.tts_engine:
            try:
                self.tts_engine.save_to_file(text, filename)
                self.tts_engine.runAndWait()
                return True
            except Exception as e:
                return False
        return False
