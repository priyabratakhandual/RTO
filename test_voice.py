#!/usr/bin/env python3
"""
Test script to diagnose voice output issues
"""
import os
import sys
from dotenv import load_dotenv

print("="*60)
print("VOICE SYSTEM DIAGNOSTIC TEST")
print("="*60)

# Test 1: Check environment variables
print("\n1. Checking environment variables...")
load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")

if groq_key:
    print("   ✓ GROQ_API_KEY found")
else:
    print("   ✗ GROQ_API_KEY not found")

if openai_key:
    print("   ✓ OPENAI_API_KEY found")
else:
    print("   ✗ OPENAI_API_KEY not found (required for TTS)")

# Test 2: Check required packages
print("\n2. Checking required packages...")
packages = {
    'groq': 'groq',
    'openai': 'openai',
    'dotenv': 'python-dotenv',
    'sounddevice': 'sounddevice',
    'soundfile': 'soundfile',
    'pygame': 'pygame',
    'pydub': 'pydub',
    'playsound': 'playsound',
    'pyttsx3': 'pyttsx3'
}

for module, package in packages.items():
    try:
        __import__(module)
        print(f"   ✓ {package} installed")
    except ImportError:
        print(f"   ✗ {package} NOT installed")

# Test 3: Test OpenAI TTS
print("\n3. Testing OpenAI TTS...")
if openai_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_key)
        
        print("   Testing TTS generation...")
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input="Hello, this is a test message.",
            speed=1.0
        )
        
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tmp_path = f.name
            response.stream_to_file(tmp_path)
        
        print(f"   ✓ TTS file created: {tmp_path}")
        print(f"   File size: {os.path.getsize(tmp_path)} bytes")
        
        # Test audio playback
        print("\n4. Testing audio playback...")
        
        # Try pydub
        try:
            from pydub import AudioSegment
            from pydub.playback import play
            print("   Trying pydub...")
            audio = AudioSegment.from_mp3(tmp_path)
            print(f"   ✓ Audio loaded: {len(audio)}ms duration")
            print("   Playing audio (you should hear it)...")
            play(audio)
            print("   ✓ pydub playback successful")
        except ImportError:
            print("   ✗ pydub not available")
        except Exception as e:
            print(f"   ✗ pydub error: {str(e)}")
            
            # Try pygame
            try:
                import pygame
                print("   Trying pygame...")
                pygame.mixer.init()
                pygame.mixer.music.load(tmp_path)
                pygame.mixer.music.play()
                import time
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                pygame.mixer.quit()
                print("   ✓ pygame playback successful")
            except Exception as e:
                print(f"   ✗ pygame error: {str(e)}")
                
                # Try playsound
                try:
                    from playsound import playsound
                    print("   Trying playsound...")
                    playsound(tmp_path, block=True)
                    print("   ✓ playsound playback successful")
                except Exception as e:
                    print(f"   ✗ playsound error: {str(e)}")
        
        # Cleanup
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
            
    except Exception as e:
        print(f"   ✗ OpenAI TTS error: {str(e)}")
        import traceback
        traceback.print_exc()
else:
    print("   ✗ Cannot test - OPENAI_API_KEY not set")

# Test 5: Test pyttsx3 fallback
print("\n5. Testing pyttsx3 fallback...")
try:
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    print(f"   ✓ pyttsx3 initialized")
    print(f"   Available voices: {len(voices)}")
    for i, voice in enumerate(voices[:3]):
        print(f"      Voice {i}: {voice.name}")
    engine.setProperty('rate', 150)
    print("   Testing speech...")
    engine.say("This is a test message from pyttsx3")
    engine.runAndWait()
    print("   ✓ pyttsx3 test completed")
except Exception as e:
    print(f"   ✗ pyttsx3 error: {str(e)}")

print("\n" + "="*60)
print("DIAGNOSTIC COMPLETE")
print("="*60)

