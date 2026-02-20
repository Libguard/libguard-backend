from rest_framework.views import APIView
from apps.dependency_analysis.serializers import ProjectUplaodSerializer
from apps.dependency_analysis.tasks import analyze
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
import uuid
import zipfile
from pathlib import Path

class ProjectUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = ProjectUplaodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_compressed = serializer.validated_data["project_path"] # type: ignore

        project_id = str(uuid.uuid4()) # Pesquisar depois oq é cada UUID
        project_path = Path("/tmp/projects/") / project_id # /tmp/projects/12345678 por exemplo
        project_path.mkdir(parents=True, exist_ok=True) # o 'parents' permite criar pastas dentro de pastas e o 'exists_ok' é pra não lançar uma exception se o diretório já existir

        # Extract paths and files at zip file
        with zipfile.ZipFile(project_compressed, "r") as zp:
            for file in zp.namelist():
                file_path = Path(file)
                if file_path.is_absolute() or ".." in file_path.parts:
                    continue
                zp.extract(file, project_path)

        try:
            #task = analyze.delay(str(project_path))
            analyze.delay(str(project_path))
        except Exception as e:
            return Response({"error": f"{e}"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        return Response({"detail": "DEU BOM AQUI"}, status=status.HTTP_202_ACCEPTED)
