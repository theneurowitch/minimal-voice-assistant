# Minimal Voice Assistant for Beginners

## What is this and who is it for?

This project is a very simple voice assistant to accompany my tutorial on neurowitch.io. I started posting about my full agentic voice assistant project on social media, and got a decent amount of interest. I also noticed a lot of the interest was from folks who may not be especially technical, and only want a couple of skills anyway.


### Prerequisites

- A computer. If you're reading this, congrats, you pass
- Python. If you have a mac or most linux machines, you will already have python. If you have windows, you'll have to install it from [python.org](python.org)
- A lil teeny bit of python knowledge. (I highly recommend just browsing python.org; they have really good stuff for beginners, including installation guides!)
- A little bit of courage. Working with the terminal can seem really scary at first (thanks, movies!) but it's just a text window where you can talk directly to your computer instead of using the mouse to click around for stuff.

### Quickstart
Clone this project and cd into the project from your terminal

Run the following:

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


### This project uses
- [FastApi](https://fastapi.tiangolo.com/)
- [FasterWhisper](https://github.com/SYSTRAN/faster-whisper)
- [Piper](https://piper.ttstool.com/) * OPTIONAL *
