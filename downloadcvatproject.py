from cvat_sdk import Client
from cvat_sdk.core.proxies.model_proxy import Location
from datetime import date
 
# CVAT credentials
cvat_url = "https://app.cvat.ai"
username = "swadmin@trianz.com"
password = "7Wa.cEa8c6kEsVf"
 
# CVAT project name
project_name = "pw_fleet_dataset"
task_name = "passenger seatbelt"
# "Food/Drink Observed"
# "Cell Phone Handheld Observed"
#"Cell Phone Hands Free Observed"
#"smoking"
# #"passenger seatbelt"
 
def download_dataset(cvat_url, username, password, project_name):
   
    client = Client(url=cvat_url)
    client.login([username, password])
   
    projects = client.projects.list()
    project = next((p for p in projects if p.name == project_name), None)
    if not project:
        print(f"Project '{project_name}' not found.")
        return
   
    s3_prefix = "tasks_exports/"
    tasks = project.get_tasks()
 
    date_filter = date(2024,1,23) #If want to filter data by creation date
    count = 1
 
 
    # filtered_tasks = [task for task in tasks if task.name == task_name]
 
    filtered_tasks = [task for task in tasks if task.name == task_name and task.created_date.date() == date_filter] #use this if want to filter data by creation date
 
    for task in tasks:
       
        if(task.name == task_name and task.created_date.date() == date_filter):
            filename = f"{s3_prefix}{task.name.replace(' ', '_')}{'_'}{count}.zip"
 
 
            task.export_dataset(
                    format_name="Ultralytics YOLO Oriented Bounding Boxes 1.0",
                    include_images=True,
                    filename=filename,  # Cloud storage key for file
                    location=Location.CLOUD_STORAGE,
                    cloud_storage_id=2533  # Replace with your cloud storage ID
                )
            count +=1
            print(f"Task uploaded: '{task.name}' to S3 path '{filename}' ----'{task.created_date}'")
       
# Download the dataset
download_dataset(cvat_url, username, password, project_name)