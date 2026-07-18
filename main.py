"""A tiny, fully-local voice assistant.

This one file is the entire assistant. Reading it top to bottom shows you the
whole trick:

  1. grab audio from your microphone in little blocks,
  2. figure out when you started and stopped talking,
  3. notice the wakeword ("hey livekit"),
  4. turn your speech into text with faster-whisper,
  5. match that text against a couple of regular expressions to run commands.

Run it:               python main.py
Stop it:              ctrl+c

"""

import queue
import re
import threading
from datetime import datetime

import numpy as np
import sounddevice as sd  # talks to your microphone (and speakers)
from faster_whisper import WhisperModel  # speech -> text

# ---------------------------------------------------------------------------
# Settings. Play around with these to see what works best for your setup!
# ---------------------------------------------------------------------------

SAMPLE_RATE = 16000  # samples per second. Whisper wants exactly this rate
BLOCK_SECONDS = 0.25  # size of each little piece of audio we look at. Smaller takes more CPU but reacts faster


# "Loudness" below this counts as silence. This is the number to tune first:
#   - assistant seems deaf / cuts you off  -> make it smaller (try 0.002)
#   - assistant hears things when the room is quiet -> make it bigger (try 0.01)
SILENCE_THRESHOLD = 0.003

SILENCE_BLOCKS = 4  # this many quiet blocks in a row (~1s) = you finished talking
MAX_SPEECH_SECONDS = 15  # stop collecting eventually, even in a noisy room

# These two only matter if you set up the optional wakeword model (see README):
WAKEWORD_THRESHOLD = 0.5  # model score above this counts as "hey livekit"
WAIT_FOR_COMMAND_SECONDS = 5  # give up if you wake it but don't say anything

WINDOW_SECONDS = 2  # the wakeword model always scores the last 2s of audio

# ---------------------------------------------------------------------------
# The speech-to-text model. "base.en" is small enough to run on a modest CPU.
# The first run downloads it (~75MB); after that it loads from disk.
# ---------------------------------------------------------------------------

whisper = WhisperModel("base.en", compute_type="int8")

# ---------------------------------------------------------------------------
# The OPTIONAL wakeword model. If you followed the README's wakeword section
# you'll have the library installed and a model file in models/ — in that case
# we use it. If not, no problem: the assistant falls back to transcribing what
# you say and looking for the words "hey livekit" in the text.
#
# Why bother with the model at all? Two reasons:
#   - whisper only runs AFTER the wakeword, instead of transcribing every
#     sound in your room all day (nicer to your battery), and
#   - it's trained specifically on that one phrase, so it's better at
#     catching it than a transcribe-then-check approach.
# ---------------------------------------------------------------------------

try:
    from livekit.wakeword import WakeWordModel

    wakeword = WakeWordModel(models=["models/hey_livekit.onnx"])
except Exception:
    wakeword = None

# ---------------------------------------------------------------------------
# The OPTIONAL voice. Same deal as the wakeword model: if you followed the
# README's "give it a voice" section, piper is installed and there's a voice
# model in models/ — then the assistant speaks its replies out loud (as well
# as printing them). If not, replies just show up as text. That's the whole
# difference.
# ---------------------------------------------------------------------------

try:
    from piper.voice import PiperVoice

    voice = PiperVoice.load("models/en_US-lessac-medium.onnx")
except Exception:
    voice = None


def reply(text):
    """Answer the user: always print, and speak too if the voice is set up."""
    print(text)
    if voice is None:
        return
    # Piper hands us the speech in a few pieces. Glue them together, play the
    # whole thing through the speakers, and wait until it's done talking.
    # (The microphone stays on while it talks, but that's okay: the assistant's
    # own replies never contain the wakeword, so it can't wake itself up.)
    chunks = list(voice.synthesize(text))
    if not chunks:
        return
    audio = np.concatenate([chunk.audio_float_array for chunk in chunks])
    sd.play(audio, samplerate=chunks[0].sample_rate)
    sd.wait()


# The fallback looks for the phrase in whisper's text instead.
# Whisper might write it as "hey livekit", "Hey, LiveKit" or "hey live kit",
# so the pattern is forgiving about spaces, commas and capital letters.
# This might look kinda scary, but it's just a regular expression. 
# Basically a pattern that tells Python "look for the words 'hey' or 'okay', 
# then some punctuation or whitespace, then the word 'livekit' 
# (with or without a space in the middle), then some punctuation or whitespace again"
WAKE_PHRASE = re.compile(r"\b(?:hey|okay)[,.!]?\s+live\s?kit\b[,.!]?", re.IGNORECASE)

# ---------------------------------------------------------------------------
# Skills
# 
# This is the part you'll want to extend!
#
# Each entry is a pair: (a regular expression, and the function to run when the
# text matches it). We check them top to bottom and run the first match.
# The function receives the "match object", which is how it can grab numbers
# out of the sentence. Look at set_timer to see that in action.
#
# To add your own command: write a function, add a row here. That's it.
# Can even copy/paste another one, name it something else, and tweak the regex to match your new phrase.
# ---------------------------------------------------------------------------


def say_time(match):
    now = datetime.now().strftime("%I:%M %p").lstrip("0")
    reply(f"It's {now}")


# Whisper usually writes small numbers as words ("set a timer for two minutes"),
# so the timer pattern accepts both digits and these words:
NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "fifteen": 15,
    "twenty": 20, "thirty": 30, "forty-five": 45, "sixty": 60,
}


def set_timer(match):
    # match.group(1) is whatever the first (...) in the pattern captured —
    # either digits like "5" or a word like "five". group(2) is the unit.
    raw = match.group(1).lower()
    amount = int(raw) if raw.isdigit() else NUMBER_WORDS.get(raw)
    if amount is None:
        reply(f"I didn't catch how long — '{raw}' isn't a number I know")
        return
    unit = match.group(2).lower()
    seconds = amount * 60 if unit.startswith("minute") else amount

    def ring():
        # The \a is the terminal "bell" — some terminals ding, some flash.
        # (The voice just ignores it and reads the words.)
        reply(f"\aDing! Your {amount} {unit} timer is done!")

    threading.Timer(seconds, ring).start()
    reply(f"Timer set for {amount} {unit}{'s' if amount != 1 else ''}")

# ADD NEW COMMANDS HERE! Just add a new row to the INTENTS list below, and write a function for it above.
INTENTS = [
    (re.compile(r"what time is it|what's the time", re.IGNORECASE), say_time),
    (re.compile(r"set a timer for (\d+|[a-z-]+) (second|minute)s?", re.IGNORECASE), set_timer),
]


def handle_command(text):
    """Figure out which command the text is asking for, and run it."""
    for pattern, action in INTENTS:
        match = pattern.search(text)
        if match:
            action(match)
            return
    reply(f"I heard: {text}, but I don't have a skill for that")


# ---------------------------------------------------------------------------
# Small helpers used by both listening modes.
# ---------------------------------------------------------------------------


def transcribe(audio):
    """Hand audio to whisper, get text back."""
    segments, _ = whisper.transcribe(audio, language="en")
    return " ".join(segment.text for segment in segments).strip()


def loudness(block):
    """How loud is this block of audio? (Root-mean-square, if you're curious:
    square every sample, average them, square-root it. Bigger = louder.)"""
    return np.sqrt(np.mean(block**2))


def open_microphone(on_audio):
    """Open the default microphone. Every BLOCK_SECONDS, the sound library
    calls on_audio() with the newest block of samples."""
    return sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32",
        blocksize=int(SAMPLE_RATE * BLOCK_SECONDS),
        callback=on_audio,
    )


# ---------------------------------------------------------------------------
# Listening mode 1: with the wakeword model.
#
# We keep a "rolling window" of the last 2 seconds of audio imagine a strip
# of paper 2 seconds wide, that always shows the most recent sound. Every
# quarter second we ask the model "does this strip end with someone finishing
# the phrase 'hey livekit'?" (it was trained to expect the phrase right at the
# end, because in real life the moment to react is right as you finish saying
# it). When it says yes, we start collecting audio, stop when you go quiet
# for a second, and hand ONLY that part to whisper. Whisper never hears the
# rest of your day.
# ---------------------------------------------------------------------------


def listen_with_wakeword_model():
    audio_queue = queue.Queue()

    # This little function runs on the sound library's own thread. It just
    # drops each block into a queue so our loop below never misses audio,
    # even while whisper is busy thinking.
    def on_audio(indata, frames, time, status):
        audio_queue.put(indata.copy())

    wait_blocks = int(WAIT_FOR_COMMAND_SECONDS / BLOCK_SECONDS)
    max_blocks = int(MAX_SPEECH_SECONDS / BLOCK_SECONDS)
    window = np.zeros(SAMPLE_RATE * WINDOW_SECONDS, dtype=np.float32)

    with open_microphone(on_audio):
        print("Listening for 'hey livekit' (ctrl+c to stop)")
        command = None  # None = waiting for wakeword. A list = recording you
        heard_speech = False
        silent_blocks = 0

        while True:
            block = audio_queue.get().flatten()

            if command is None:
                # Slide the window along: drop the oldest quarter second,
                # append the newest one, and score what we've got.
                window = np.concatenate([window[len(block):], block])
                score = max(wakeword.predict(window).values(), default=0.0)
                if score > WAKEWORD_THRESHOLD:
                    print(f"Wakeword! (score {score:.2f})")
                    command = []  # start recording the actual command
                    heard_speech = False
                    silent_blocks = 0
                    window[:] = 0  # blank the window so it can't re-trigger
                continue

            # Collect audio until you stop talking.
            command.append(block)
            if loudness(block) > SILENCE_THRESHOLD:
                heard_speech = True
                silent_blocks = 0
            else:
                silent_blocks += 1

            if not heard_speech and len(command) >= wait_blocks:
                print("No command heard")
                command = None
            elif heard_speech and (silent_blocks >= SILENCE_BLOCKS or len(command) >= max_blocks):
                text = transcribe(np.concatenate(command))
                if text:
                    print(f"You said: {text}")
                    handle_command(text)
                command = None


# ---------------------------------------------------------------------------
# Listening mode 2: no wakeword model (the fallback).
#
# Here we can't detect the phrase in the audio itself, so we do the next best
# thing: wait for you to say *something*, transcribe all of it, and look for
# "hey livekit" in the text. Say the wakeword and the command in one breath:
# "hey livekit, what time is it?"
#
# The tradeoff is that whisper transcribes every sound in the room. That works fine, 
# it's just doing more work than mode 1, which is why the model is worth setting
# up eventually.
# ---------------------------------------------------------------------------


def listen_with_transcript_check():
    audio_queue = queue.Queue()

    def on_audio(indata, frames, time, status):
        audio_queue.put(indata.copy())

    max_blocks = int(MAX_SPEECH_SECONDS / BLOCK_SECONDS)

    with open_microphone(on_audio):
        print("Listening... say 'hey livekit' and a command in one breath (ctrl+c to stop)")
        speech = []  # blocks we've collected since you started talking
        silent_blocks = 0

        while True:
            block = audio_queue.get().flatten()

            # Collect audio while there's sound and count quiet blocks while
            # there isn't. One second of quiet after some sound = a finished
            # sentence that is ready to transcribe. (We wait for the pause instead
            # of using fixed chunks so we never cut a sentence in half.)
            if loudness(block) > SILENCE_THRESHOLD:
                speech.append(block)
                silent_blocks = 0
            elif speech:
                speech.append(block)
                silent_blocks += 1

            if speech and (silent_blocks >= SILENCE_BLOCKS or len(speech) >= max_blocks):
                text = transcribe(np.concatenate(speech))
                speech = []
                silent_blocks = 0

                match = WAKE_PHRASE.search(text)
                if not match:
                    continue  # not talking to us, so ignore
                command = text[match.end():].strip()
                print(f"You said: {command}")
                handle_command(command)

# ---------------------------------------------------------------------------
# Below this is the actual program entry point. Don't change anything here unless you know what you're doing!
# Or for learning purposes. Highly recommend messing around with every part of this file to see what happens
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if wakeword is not None:
        print("Wakeword model loaded (models/hey_livekit.onnx)")
    else:
        print("No wakeword model — using the transcribe-and-check fallback (see README to upgrade)")

    if voice is not None:
        print("Voice loaded (models/en_US-lessac-medium.onnx) — replies will be spoken")
    else:
        print("No voice model — replies will be text only (see README to give it a voice)")

    try:
        if wakeword is not None:
            listen_with_wakeword_model()
        else:
            listen_with_transcript_check()
    except KeyboardInterrupt:
        print("\nBye")
