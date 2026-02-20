from celery import shared_task
import tempfile
import subprocess
import os
import shutil
import json

@shared_task
def analyze(project_path):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    temp_path = temp_file.name
    temp_file.close()  

    try:
        subprocess.run(
            [
                "trivy",
                "fs",
                project_path,
                "--format",
                "json",
                "-o",
                temp_path
            ],
            check=True
        )

        with open(temp_path, "r") as f:
            trivy_json = json.load(f)

        return trivy_json
        #_save_result(trivy_json)
    
    except subprocess.CalledProcessError as e:
        raise Exception("It wasn't possible to analyze the project.")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(project_path):
            shutil.rmtree(project_path) # Delete the entire directory

def _save_result(trivy_json):
    print("TO AQUI!!")
    
    """
    TA TUDO ERRADO >:{

    result = json.loads(trivy_json)

    for k, v in result.items():
        if "Title" in k:
            print(v["Title"])
    """