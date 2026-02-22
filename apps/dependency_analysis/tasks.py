from celery import shared_task
import tempfile
import subprocess
import os
import shutil
import json
from apps.projects.models.version_model import Version

@shared_task
def analyze(project_path, upload_id):
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

        from apps.projects.models.upload_model import Upload
        upload = Upload.objects.get(id=upload_id)

        Version.objects.create(
            is_analysis_complete=True,
            analysis=trivy_json,
            project_id=upload.project_id,
            upload_id=upload
        )
    
    except subprocess.CalledProcessError as e:
        raise Exception("It wasn't possible to analyze the project.")
    
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(project_path):
            shutil.rmtree(project_path) # Delete the entire directory
