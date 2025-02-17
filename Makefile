_init:
    $global:mjk_working_directory = "C:\Users\Mathew Jacob Kavalam\OneDrive - Robert Gordon University\Feb 16th onwards\AI+Dataanalysis+python"
    cd $mjk_working_directory 
init_venv:
    .\make.ps1 _init
    $venv_dir = ".\.venv" 
    python -m venv $venv_dir 
activate_venv:
    .\make.ps1 _init
    cd .venv
    .\Scripts\Activate.ps1
    cd $mjk_working_directory
deactivate_venv:
    .\make.ps1 _init
    cd .venv\Scripts\
    deactivate
    cd $mjk_working_directory
run:
    .\make.ps1 _init
    pip freeze > requirements.txt
    .\make.ps1 runAI
    python anthony.py
    .\make.ps1 stopAI
runAI:
    lms load hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf
    lms server start --port 1234
dev2:
    .\make.ps1 _init
    lms load hugging-quants/Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf
    lms server start --port 1234
    pip freeze > requirements.txt
    python localLLM.py
    .\make.ps1 stopAI
stopAI:
    lms unload llama-3.2-1b-instruct
    lms server stop