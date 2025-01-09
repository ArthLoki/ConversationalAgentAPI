<h1 align="center"> Conversational Agente API </h1>

<h2 tabindex="-1" class="heading-element" dir="auto">Introduction</h2>

SOMETHING

<h2 tabindex="-1" class="heading-element" dir="auto">Set-up</h2>

<h3 tabindex="-1" class="heading-element" dir="auto">1. Install Python3</h3>

<h3 tabindex="-1" class="heading-element" dir="auto">2. Create a Virtual Environment</h3>

<p>Before installing all dependencies, I suggest you to create a python virtual environment in WSL (I'm using Ubuntu) for each process.</p>

<p>
<strong>Step 1: </strong>Run the command for the python version you're using:
<code>sudo apt install python3.12-venv</code>
</p>

<p>
<strong>Step 2: </strong>Create the virtual environment by running the following command in terminal:
<code>python3 -m venv venv</code>
</p>

<p><strong>Step 3: </strong>Activate the virtual environment by running the following command in terminal.
<code>source venv/bin/activate</code></p>

<h3 tabindex="-1" class="heading-element" dir="auto">3. Install Dependencies</h3>

Install pytorch using the following command:
<code>pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121</code>

Install ollama using the following command (in linux -> base directory):
<code>curl -fsSL https://ollama.com/install.sh | sh</code>

Install dependencies using the file <em>requirements.txt</em>:
<code>pip install -r requirements.txt</code>

Or install dependencies separately. For example: <code>pip install trl peft accelerate bitsandbytes triton transformers xformers</code>

<h3 tabindex="-1" class="heading-element" dir="auto">4. Building Finetuning Dataset</h3>

<p>The dataset must be saved as <em>filename.json</em> in <em>finetuning/static</em> and its content/dialog MUST have the following format:</p>
<code>[
    {
        "instruction": "Description of the character",
        "input": "User/player input",
        "output": "How the AI must answer the question"
    },
    .....
]
</code>

<h3 tabindex="-1" class="heading-element" dir="auto">5. Run <em>Finetuning</em></h3>

<p>Use the <code>cd</code> command to reach the directory <em>finetuning</em> which contains the files to perform the finetuning, then run the command below:</p>
<code>python f5_main.py</code>

<h3 tabindex="-1" class="heading-element" dir="auto">6. Create Ollama API</h3>

<p>Use the <code>cd</code> command to reach the directory <em>api</em> which contains the files to perform the creation of the Ollama API, then run the command below following the instructions given in execution:</p>
<code>python a3_main.py</code>
<p></p>
<p>Once the code runs smoothly, run in terminal:</p>
<code>ollama run chosen_modelname</code>

<h3 tabindex="-1" class="heading-element" dir="auto">7. Run Ollama API</h3>
<p>Use the <code>cd</code> command to reach the directory <em>finetuning</em> which contains the files to perform the finetuning, then run the commands below in order:</p>
<code>curl -fsSL https://elastic.co/start-local | sh</code>

<p>Remember to update the environment variables in .env, using the ones given by the command above.<p>

<code>python ra4_main.py</code>
