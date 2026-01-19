from cvat_sdk import Client
from cvat_sdk.core.proxies.model_proxy import Location
from datetime import date
import os

# CVAT credentials
cvat_url = "https://app.cvat.ai"
username = "swadmin@trianz.com"
password = "7Wa.cEa8c6kEsVf"

# CVAT project name
project_name = "pw_fleet_dataset"
task_name = "passenger seatbelt"

# Specified Windows download directory
local_download_dir = r"D:\experiment_res"  # Using raw string to handle Windows path

def download_dataset(cvat_url, username, password, project_name):
    # Create download directory if it doesn't exist
    os.makedirs(local_download_dir, exist_ok=True)
    
    client = Client(url=cvat_url)
    client.login([username, password])
    
    projects = client.projects.list()
    project = next((p for p in projects if p.name == project_name), None)
    if not project:
        print(f"Project '{project_name}' not found.")
        return
    
    tasks = project.get_tasks()
    date_filter = date(2024, 1, 23)
    count = 1
    
    filtered_tasks = [task for task in tasks if task.name == task_name and task.created_date.date() == date_filter]
    
    for task in filtered_tasks:
        filename = f"{task.name.replace(' ', '_')}_{count}.zip"
        local_path = os.path.join(local_download_dir, filename)
        
        print(f"Downloading task '{task.name}' to '{local_path}'...")
        
        task.export_dataset(
            format_name="Ultralytics YOLO Oriented Bounding Boxes 1.0",
            include_images=True,
            filename=local_path,
            location=Location.LOCAL
        )
        
        count += 1
        print(f"Task downloaded: '{task.name}' to local path '{local_path}' (created: {task.created_date})")

# Download the dataset
download_dataset(cvat_url, username, password, project_name)