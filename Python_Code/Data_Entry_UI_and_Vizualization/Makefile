_init:
    $global:mjk_working_directory = "C:\RGU Hack 2025\Code\github_repo\satyameva_jayate\Python_Code\Data_Entry_UI_and_Vizualization\"
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
run_data_entry:
    .\make.ps1 _init
    pip freeze > requirements.txt
    streamlit run .\AnimalSightingUpload.py
run_search:
    .\make.ps1 _init
    pip freeze > requirements.txt
    streamlit run .\SearchBar.py