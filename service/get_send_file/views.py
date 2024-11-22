import os
from pathlib import Path
from django.conf import settings
from django.forms import ValidationError
from django.http import FileResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from file_processing.handl_file import accept_file
from file_processing.add_columns import add_new_columns, update_existing_template
from file_processing.delete_file import delete_file_in_static

from .serializers import FileUploadSerializer
from drf_yasg.utils import swagger_auto_schema



class FileUploadView(APIView):

    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Отправление файла с исходными данными",
        request_body=FileUploadSerializer,
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = FileUploadSerializer(data=request.data)
            serializer.is_valid(raise_exception=True) 
            uploaded_file = serializer.validated_data['file']
            if not uploaded_file.name.endswith('.xlsx'):
                raise ValueError("Неподдерживаемый формат файла. Разрешены только файлы с расширением .xlsx")

            save_path = os.path.join(settings.BASE_DIR, 'static', '', uploaded_file.name)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            update_existing_template(add_new_columns(accept_file(save_path)))

            result_file_path = Path("static/new.xlsx")
            if not result_file_path.exists():
                raise FileNotFoundError("Результирующий файл не найден")

            response = FileResponse(open(result_file_path, 'rb'), as_attachment=True)
            response['Content-Disposition'] = 'attachment; filename="result.xlsx"'
            return response

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except FileNotFoundError as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            delete_file_in_static('static')