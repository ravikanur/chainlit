echo [$(date)] : "START"
echo [$(date)] : "creating conda environment with python 3.9"
conda create -n chainlit python==3.9 -y
echo [$(date)] : "created conda environment with python 3.9"
source activate chainlit
echo [$(date)] : "activated chainlit conda environment"
echo [$(date)] : "Installing requirements"
pip install -r requirements.txt
echo [$(date)] : "Installed the requirements"
echo [$(date)] : "END"