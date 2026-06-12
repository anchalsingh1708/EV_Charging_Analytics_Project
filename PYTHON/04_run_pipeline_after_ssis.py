import subprocess
import sys
from pathlib import Path
root = Path(r"D:\ANCHAL\MINI Project SEM 2\EV_Charging_Analytics_Project")
for script in ["02_clean_transform_load.py", "03_demand_prediction.py"]:
    subprocess.check_call([sys.executable, str(root / "python" / script)])
