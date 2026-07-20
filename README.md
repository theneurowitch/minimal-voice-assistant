# Minimal Voice Assistant for Beginners

## What is this and who is it for?

This project is a very simple voice assistant, designed as a learning exercise. I made a couple of social media posts about my personal voice assistant project, and got a fair number of comments from people who want to build one, but aren't programmers and/or only want to use the assistant to do one or two things. My full assistant is massive overkill for both those scenarios.

As well, a lot of comments asked for a tutorial. The more I thought about it, the more I think this could be a really cool project for someone to learn basic programming, with endless opportunities to upgrade! So this is a very minimal voice assistant example, with the goal of teaching concepts and making space for beginners to get used to stuff like installing packages and writing simple python functions without having to own a really powerful computer or needing to buy any satellite hardware.

## What this project is NOT:
This is not a full Alexa replacement, not by a long shot. It's a minimal scaffolding for people who want to try out the process of building something without needing to know everything, buy new hardware, etc.

## Current Skills:
This project ships with 2 demo skills. One for setting a timer, and one for checking the time. They are both in the main.py file. The intention is that you add your own skills to learn some basic python, and grow some confidence in building stuff that works really well for you. As you add skills, update this list!

- Timer: Sets a timer for the designated length
- Time: Reads the current time

## Prerequisites

- A computer. If you're reading this on a machine you own, you're good
- A microphone that can plug into the computer. A webcam mic is fine, a built-in laptop mic is fine
- A text editor. I like SublimeText or VSCode because they make reading code nice, but you can use literally any text editor if you want
- A terminal. Looks scary in the movies but it's just a chat window that you can use to talk to your computer and tell it what to do, instead of clicking around with your mouse!
- If you have a computer, you have a terminal; it's built in. You can open it like any other application.
    - Side note though, if you get excited about this project and start googling stuff, don't just paste random commands you find into your terminal. Do your due diligence to understand what you're telling the computer to do, or you might tell it to do something insane. This doesn't usually happen unless you're putting in really strange commands, but it's worth mentioning
- Python. If you have a mac or most linux machines, you will already have python. If you have windows, you'll have to install it from [python.org](https://python.org)
    - You need **python 3.11 or newer**. Not sure? Open a terminal and type `python3 --version`
    - If that prints 3.11 or higher, you're good — and use `python3` and `pip3` everywhere this README says `python` and `pip`
    - If it says something like `command not found`, try `python --version` instead. If *that* prints 3.11 or higher, you're good and you can use `python` and `pip` as written
    - If the number is lower than 3.11 (or starts with a 2), install a current python from [python.org](https://python.org). The old one will keep working for anything else on your computer; you're just adding a newer one alongside it
    - Skipping this bites you at the `pip install` step, as a wall of red text about not finding a version that satisfies the requirement. That's just this, in disguise
- On Linux only: the audio library needs one system package. Run `sudo apt install libportaudio2` (or your distro's equivalent). Without it you'll get an error about PortAudio when you start the assistant. Mac and Windows users can skip this
- A lil teeny bit of python knowledge, or willingness to learn. (I highly recommend just browsing python.org; they have really good stuff for beginners, including installation guides!)

## Quickstart
Clone this project (press the green button that says "code" and pick your method. I recommend learning a bit of git and cloning it, but you can also just download the files as a .zip file and open in your text editor)

`cd` into your project directory from your terminal (for explanations of this and other commands, check out [w3schools](https://www.w3schools.com/bash/bash_cd.php) reference page. They'll have explanations and examples of common commands)

Run the following in your terminal (type it in, or copy/paste it, and hit enter to run):

`python -m venv env`

*** Note: this is not strictly necessary, but is a really good idea because it keeps your project's libraries contained and separate from other stuff. The one downside is you have to remember to deactivate it when switching projects in the same terminal window, and you have to remember to activate it again if you close the terminal window and open a new one ***

*** Note2: It doesn't matter what you put after the venv part. I've just called it 'env' but you can name it something more descriptive so they're easier to keep straight from different projects if you like ***

Activate the virtual environment by running the command for your operating system:

**macOS / Linux:**

`source env/bin/activate`

**Windows:**

`env\Scripts\activate`

You'll know it worked because your terminal prompt now starts with `(env)`. That's how you tell at a glance whether it's on. (If you named your folder something other than `env`, use that name instead.)


Install the needed packages by running: 
`pip install -r requirements.txt`

*** Note: The -r flag tells the package manager to open and read the file. Otherwise, it'll try to look on the internet for a library called requirements.txt and it won't find one ***


### Running it

Start the assistant:

`python main.py`

The first run downloads the speech-recognition model (~75MB), so give it a minute. When you see the "Listening" line, say **"hey livekit, what time is it?"** — all in one breath. Ctrl+C stops it.

*** Note: the first time you run it, your computer will probably ask if the terminal is allowed to use the microphone. Say yes! If you accidentally said no, that permission lives in your system settings under Privacy > Microphone ***

### How it understands commands

There's no AI language model in here deciding what you meant. It's something much older and simpler: the text gets checked against a list of triggers. About two thirds of the way down `main.py`, under the "Skills" heading, there's a little table:

```python
INTENTS = [
    (re.compile(r"what time is it|what's the time", re.IGNORECASE), say_time),
    (re.compile(r"set a timer for (\d+|[a-z-]+) (second|minute)s?", re.IGNORECASE), set_timer),
]
```

Whatever you say gets turned into text, and the text is checked against each trigger, top to bottom. First match wins and its function runs. Out of the box it knows two tricks:

- "what time is it" → tells you the time
- "set a timer for 5 minutes" → dings when your timer is up

Those two use *regular expressions* (`re.compile(...)`), which are patterns that can pull pieces out of a sentence — that's how the timer knows you said "5" and "minutes". They're powerful and they're also the most annoying part of this to learn, so **you don't have to start there.** A trigger can also just be plain words:

```python
("flip a coin", flip_coin),
```

That matches if you said those words anywhere in your sentence. Start with plain words, and reach for a regular expression only when your skill needs to grab a number or a name out of what you said.

### Your first skill, start to finish

Let's teach it to flip a coin. The whole thing is two steps.

**Step 1.** Open `main.py` and find the Skills section (search for `def say_time`). Add this function just above the `INTENTS` list:

```python
def flip_coin(match):
    result = random.choice(["Heads", "Tails"])
    reply(result)
```

Three things worth noticing:

- **`reply()`** is how a skill answers you. It prints, and it speaks too if you've set up the voice. Always answer with `reply()` rather than `print()`, so your skill works in both setups.
- **`match`** is the piece of information every skill receives about *how* it matched. This skill doesn't need it, so it just ignores it, but the function still has to accept it. `set_timer` right below shows what it's for.
- **`random`** is a built-in python toolbox we haven't used yet, so add `import random` up at the top of the file with the other imports. If you forget, you'll get a `NameError: name 'random' is not defined`, which is python telling you exactly this.

**Step 2.** Add your trigger to the `INTENTS` list, so it knows when to run:

```python
INTENTS = [
    (re.compile(r"what time is it|what's the time", re.IGNORECASE), say_time),
    (re.compile(r"set a timer for (\d+|[a-z-]+) (second|minute)s?", re.IGNORECASE), set_timer),
    ("flip a coin", flip_coin),
]
```

The trailing comma matters! Every row needs one. Forgetting it is probably the single most common python mistake there is, and you'll see a `SyntaxError` pointing near that line.

**Step 3.** Try it, no microphone needed: (See below for text mode explanation)

```
python main.py --text
> flip a coin
Heads
```

That's a skill. Now go break it on purpose. Do something like misspell `random`, or delete a bracket, and watch what it tells you. If a skill hits an error the assistant prints the problem and keeps running, so you can poke at it freely without it crashing every time.

Once it works in text mode, run `python main.py` and say "hey livekit, flip a coin." Same code, now with your voice.

**Some ideas for your next one:** roll a dice, pick randomly from your lunch options, tell you how many days until a date you care about, add an item to a shopping list saved in a text file. That last one is the doorway to most genuinely useful home skills. Once a skill can read and write a file, it can remember things between runs.

*** Note: When making changes, you'll need to end the program with ctrl + c and run it again to see the changes. I deliberately avoided adding complexity with hot-reloading, but may add it in a future version if that's really annoying for people. ***

### Writing a skill without talking to your computer

When you're working on a new skill, testing it by speaking is slow and confusing. If nothing happens, you can't tell whether your pattern is wrong, or the microphone didn't hear you, or it heard you and wrote down something slightly different.

So there's a text mode:

`python main.py --text`

It skips the microphone entirely and just lets you type commands:

```
> what time is it
It's 4:32 PM
> set a timer for 5 seconds
Timer set for 5 seconds
```

This only tests your skill's code. Once it works here, you know any remaining problem is an audio one, and you can go look at the troubleshooting section instead of rewriting your pattern over and over. Highly recommend building every new skill this way first. (And as a bonus you can do stuff in a coffee shop or late at night or on a computer that doesn't have a speaker hooked up)

### Optional level-up: real wakeword detection (highly recommended)

Out of the box, the assistant listens for "hey livekit" by transcribing what you say and checking the whole text for the phrase. That works, but it means the speech recognizer runs on every sound in the room, which is harder on your computer, and it can miss the phrase if it gets transcribed weirdly. You'll also likely have to mess with the audio settings in main.py to get it working for your particular environment and background noise.

The upgrade: a tiny model specially trained to recognize the sound of one exact phrase. (So it's much better at recognizing that phrase than the general model that is listening for/recognizing all speech.) It listens all day using barely any computer power, and speech recognition only runs after it hears the magic words. 

To set it up:

1. Open `requirements.txt`, remove the `#` from the `livekit-wakeword` and `onnxruntime` lines, and run `pip install -r requirements.txt` again. (Only the two lines that look like package names! Leave the explanation lines commented out, because pip can't read English)
2. Make a folder called `models` inside the project folder, and download [hey_livekit.onnx](https://github.com/livekit-examples/hello-wakeword/raw/main/client/models/hey_livekit.onnx) into it

   Downloading in a browser sometimes saves the file under the wrong name, which is annoying to debug. If you'd rather be certain, run this in your terminal from the project folder:

   ```
   mkdir -p models
   curl -L -o models/hey_livekit.onnx https://github.com/livekit-examples/hello-wakeword/raw/main/client/models/hey_livekit.onnx
   ```

3. Run `python main.py`. It'll say "Wakeword model loaded" and you're done. Everything else works exactly the same

*** Note: the wakeword is "hey livekit" because that's the phrase this free model was trained on. A wakeword model only knows its one exact phrase. (You can train your own phrase with [livekit-wakeword](https://github.com/livekit/livekit-wakeword)'s training pipeline, but that's a whole project of its own) ***

*** Note2: don't "upgrade" the onnxruntime line in requirements.txt! It's pinned below 1.23 on purpose. Newer versions have a bug where wakeword models load fine but score everything near zero, which looks exactly like the assistant ignoring you ***

### Optional level-up: give it a voice (may not need, depending on your use case)

Right now the assistant answers by printing text. This level-up makes it talk back, using [Piper](https://github.com/OHF-Voice/piper1-gpl), a neural text-to-speech engine that's fast enough for a modest CPU and totally offline, just like everything else here. 

Same recipe as the wakeword:

1. Open `requirements.txt`, remove the `#` from the `piper-tts` line, and run `pip install -r requirements.txt` again
2. Download a voice into a `models` folder inside the project (the same folder the wakeword model goes in — make it if you haven't already). You need BOTH files:
   - [en_US-lessac-medium.onnx](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx) (the voice, ~60MB)
   - [en_US-lessac-medium.onnx.json](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json) (its settings. Piper needs it sitting next to the voice with exactly this name)

   Or, from the terminal:

   ```
   mkdir -p models
   curl -L -o models/en_US-lessac-medium.onnx https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
   curl -L -o models/en_US-lessac-medium.onnx.json https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
   ```
3. Run `python main.py`. it'll say "Voice loaded" and now every reply is spoken as well as printed

You may or may not want this one. If you're across the room asking about the weather, hearing the answer is the whole point. If you're sitting at your desk watching the replies print, or your assistant mostly just controls some lights and you can see them turn on, it's not adding much.

*** Note: there are lots of voices in lots of languages. You can see them all, and play with audio previews, at [the piper samples page](https://rhasspy.github.io/piper-samples/). If you pick a different one, download its two files into `models` and change the filename in `main.py` where it says `PiperVoice.load(...)` ***

*** Note: There are also other voice engines, which could be a good first upgrade/feature swap to work on. Check out [Kokoro](https://kokorottsai.com/) and [Kitten TTS](https://github.com/KittenML/KittenTTS) ***

## Troubleshooting

Everything here is normal and fixable. Nothing you can do in this project will break your computer.

**`ModuleNotFoundError: No module named 'sounddevice'` (or faster_whisper, or numpy)**

The packages aren't installed in the environment you're currently in. Nine times out of ten the virtual environment just isn't activated — check whether your prompt starts with `(env)`. If it doesn't, activate it (see the Quickstart) and run `pip install -r requirements.txt` again.

**An error mentioning PortAudio, on Linux**

Install the system audio library: `sudo apt install libportaudio2`.

**It says "Listening" but nothing happens when I talk**

Work through these in order:

1. Check the microphone permission. On a mac, System Settings > Privacy & Security > Microphone, and make sure your terminal app is allowed. The prompt only appears once, so if you clicked "don't allow" a while ago, that's the problem.
2. Check that your skill works at all: `python main.py --text` and type the command. If it doesn't work there, it's the skill, not the mic.
3. If it works in text mode, it's an audio-level problem. Open `main.py` and lower `SILENCE_THRESHOLD` (try `0.002`). Your microphone may just be quieter than the default assumes.
4. Without the wakeword model, you have to say the wakeword and the command **together in one breath** "hey livekit, what time is it?" A pause in the middle splits it into two separate pieces of audio and neither one matches.

**It answers things I didn't say to it / it's triggering constantly**

Your room is noisier than the default assumes. Raise `SILENCE_THRESHOLD` in `main.py` (try `0.01`). A fan or other ambient noise will cause this.

**It hears me but says "I don't have a skill for that"**

It heard you, but your words don't match any pattern. It prints what it heard, so compare that to your regex. Common culprits: whisper wrote a number as a word ("two" not "2"), or added punctuation, or capitalized something. Test your pattern in `--text` mode using the exact text it printed.

**I set up the wakeword model but it still says "No wakeword model"**

The startup message tells you why. Usually it's one of:

- The file isn't at `models/hey_livekit.onnx` inside the project folder, or the browser saved it under a different name
- You installed `livekit-wakeword` but not `onnxruntime` (you need to uncomment both lines in `requirements.txt`)
- You have onnxruntime 1.23 or newer. Check with `pip show onnxruntime`, and if so run `pip install -r requirements.txt` again to get back to the pinned version

**Ctrl+C doesn't stop it**

Press it again. If it still won't quit, close the terminal window. It won't break anything if you terminate the process.

## This project uses
- [FasterWhisper](https://github.com/SYSTRAN/faster-whisper) - turns your speech into text, fully offline
- [sounddevice](https://python-sounddevice.readthedocs.io/) - reads audio from your microphone
- [LiveKit Wakeword](https://github.com/livekit/livekit-wakeword) * OPTIONAL * - dedicated "hey livekit" detection (see the level-up section above)
- [Piper](https://piper.ttstool.com/) * OPTIONAL * - text-to-speech, for when you want it to talk back
