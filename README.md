# Minimal Voice Assistant for Beginners

## What is this and who is it for?

This project is a very simple voice assistant to accompany my tutorial on neurowitch.io. I made a couple of social media posts about my personal voice assistant project, and got a fair number of comments from people who want to build one, but aren't programmers and/or only want to use the assistant to do one or two things. My full assistant is massive overkill for both those scenarios.

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
- Python. If you have a mac or most linux machines, you will already have python. If you have windows, you'll have to install it from [python.org](python.org)
    - Not sure? Open a terminal and type `python --version`
    - If the version starts with a 3, you're good. If it starts with a 2 (like 2.7.3 or something), then you'll need to type `python3 --version`
    - If that shows a number that starts with 3, then you'll need to run commands with `python3` instead of `python` and `pip3` instead of `pip`
- A lil teeny bit of python knowledge, or willingness to learn. (I highly recommend just browsing python.org; they have really good stuff for beginners, including installation guides!)

## Quickstart
Clone this project (press the green button that says "code" and pick your method. I recommend learning a bit of git and cloning it, but you can also just download the files as a .zip file and open in your text editor)

`cd` into your project directory from your terminal (for explanations of this and other commands, check out [w3schools](https://www.w3schools.com/bash/bash_cd.php) reference page. They'll have explanations and examples of common commands)

Run the following in your terminal (type it in, or copy/paste it, and hit enter to run):

`python -m venv env`

*** Note: this is not strictly necessary, but is a really good idea because it keeps your project's libraries contained and separate from other stuff. The one downside is you have to remember to deactivate it when switching projects in the same terminal window, and you have to remember to activate it again if you close the terminal window and open a new one ***

*** Note2: It doesn't matter what you put after the venv part. I've just called it 'env' but you can name it something more descriptive so they're easier to keep straight from different projects if you like ***

Activate the virtual enviroment by running the correct command for your operating system:

<table class="">
<thead>
<tr class="row-odd"><th class="head"><p>Platform</p></th>
<th class="head"><p>Shell</p></th>
<th class="head"><p>Command to activate virtual environment</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td rowspan="4"><p>POSIX</p></td>
<td><p>bash/zsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>fish</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate.fish</span></code></p></td>
</tr>
<tr class="row-even"><td><p>csh/tcsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate.csh</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>pwsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/Activate.ps1</span></code></p></td>
</tr>
<tr class="row-even"><td rowspan="2"><p>Windows</p></td>
<td><p>cmd.exe</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">C:\&gt;</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">\Scripts\activate.bat</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>PowerShell</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">PS</span> <span class="pre">C:\&gt;</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">\Scripts\Activate.ps1</span></code></p></td>
</tr>
</tbody>
</table>


Install the needed packages by running: 
`pip install -r requirements.txt`

*** Note: The -r flag tells the package manager to open and read the file. Otherwise, it'll try to look on the internet for a library called requirements.txt and it won't find one ***


### Running it

Start the assistant:

`python main.py`

The first run downloads the speech-recognition model (~75MB), so give it a minute. When you see the "Listening" line, say **"hey livekit, what time is it?"** — all in one breath. Ctrl+C stops it.

*** Note: the first time you run it, your computer will probably ask if the terminal is allowed to use the microphone. Say yes! If you accidentally said no, that permission lives in your system settings under Privacy > Microphone ***

### How it understands commands

There's no AI language model in here deciding what you meant. It's something much older and simpler: regular expressions (patterns that match text). Near the top of `main.py` there's a little table:

```python
INTENTS = [
    (re.compile(r"what time is it|what's the time", re.IGNORECASE), say_time),
    (re.compile(r"set a timer for (\d+|[a-z-]+) (second|minute)s?", re.IGNORECASE), set_timer),
]
```

Whatever you say gets turned into text, and the text is checked against each pattern, top to bottom. First match wins and its function runs. Out of the box it knows two tricks:

- "what time is it" → tells you the time
- "set a timer for 5 minutes" → dings when your timer is up

Want to teach it something new? Write a little function, add a row to the table. That's the whole skill system, and honestly, for a couple of commands it's all you need. Really great for getting a little experience programming!

### Optional level-up: real wakeword detection (highly recommended)

Out of the box, the assistant listens for "hey livekit" by transcribing what you say and checking the whole text for the phrase. That works, but it means the speech recognizer runs on every sound in the room, which is harder on your computer, and it can miss the phrase if it gets transcribed weirdly. You'll also likely have to mess with the audio settings in main.py to get it working for your particular environment and background noise.

The upgrade: a tiny model specially trained to recognize the sound of one exact phrase. (So it's much better at recognizing that phrase than the general model that is listening for/recognizing all speech.) It listens all day using barely any computer power, and speech recognition only runs after it hears the magic words. 

To set it up:

1. Open `requirements.txt`, remove the `#` from the `livekit-wakeword` and `onnxruntime` lines, and run `pip install -r requirements.txt` again
2. Make a folder called `models` in the project, and download [hey_livekit.onnx](https://github.com/livekit-examples/hello-wakeword/raw/main/client/models/hey_livekit.onnx) into it
3. Run `python main.py` — it'll say "Wakeword model loaded" and you're done. Everything else works exactly the same

*** Note: the wakeword is "hey livekit" because that's the phrase this free model was trained on. A wakeword model only knows its one exact phrase. (You can train your own phrase with [livekit-wakeword](https://github.com/livekit/livekit-wakeword)'s training pipeline, but that's a whole project of its own) ***

*** Note2: don't "upgrade" the onnxruntime line in requirements.txt! Versions 1.27 and newer have a bug where wakeword models load fine but score everything near zero, which looks exactly like the assistant ignoring you ***

### Optional level-up: give it a voice (may not need, depending on your use case)

Right now the assistant answers by printing text. This level-up makes it talk back, using [Piper](https://github.com/OHF-Voice/piper1-gpl), a neural text-to-speech engine that's fast enough for a modest CPU and totally offline, just like everything else here. 

Same recipe as the wakeword:

1. Open `requirements.txt`, remove the `#` from the `piper-tts` line, and run `pip install -r requirements.txt` again
2. Download a voice. You need BOTH files, and they go in the same `models` folder as before:
   - [en_US-lessac-medium.onnx](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx) (the voice, ~60MB)
   - [en_US-lessac-medium.onnx.json](https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json) (its settings. Piper needs it sitting next to the voice with exactly this name)
3. Run `python main.py`. it'll say "Voice loaded" and now every reply is spoken as well as printed

You may or may not need this one. If you're controlling some lights, you 

*** Note: there are lots of voices in lots of languages. You can see them all, and play with audio previews, at [the piper samples page](https://rhasspy.github.io/piper-samples/). If you pick a different one, download its two files into `models` and change the filename in `main.py` where it says `PiperVoice.load(...)` ***

## This project uses
- [FasterWhisper](https://github.com/SYSTRAN/faster-whisper) - turns your speech into text, fully offline
- [sounddevice](https://python-sounddevice.readthedocs.io/) - reads audio from your microphone
- [LiveKit Wakeword](https://github.com/livekit/livekit-wakeword) * OPTIONAL * - dedicated "hey livekit" detection (see the level-up section above)
- [Piper](https://piper.ttstool.com/) * OPTIONAL * - text-to-speech, for when you want it to talk back
