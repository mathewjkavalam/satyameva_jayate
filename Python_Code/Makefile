_init:
    $global:mjk_working_directory = "C:\RGU Hack 2025\Code\satyameva_jayate\Python_Code\"
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
    streamlit run .\home.py
run_search:
    .\make.ps1 _init
    pip freeze > requirements.txt
    streamlit run .\SearchBar.py