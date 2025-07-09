from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
from .services.llm_service import LLMService
from .services.metrics import TextMetrics
from .models import BenchmarkResult
import logging
from rest_framework.parsers import MultiPartParser, JSONParser

logger = logging.getLogger(__name__)

@api_view(['POST'])
@parser_classes([MultiPartParser, JSONParser])
def benchmark_api(request):
    """
    Endpoint para procesar benchmarking de LLMs
    """
    if not any([request.data.get('text'), request.FILES.get('file')]):
        return Response(
            {'error': 'Se requiere texto o archivo para procesar'},
            status=status.HTTP_400_BAD_REQUEST
        )

    llm_service = LLMService()
    metrics_calculator = TextMetrics()

    try:
        text = request.data.get('text', '')
        file = request.FILES.get('file')

        if file:
            if not file.name.lower().endswith(('.txt', '.hrf')):
                return Response(
                    {'error': 'Solo se aceptan archivos .txt o .hrf'},
                    status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
                )
            try:
                text = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return Response(
                    {'error': 'El archivo no tiene codificación UTF-8 válida'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if not text.strip():
            return Response(
                {'error': 'El texto proporcionado está vacío'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Procesa los LLMs
        chatgpt_res, deepseek_res = llm_service.process_with_llms(text)

        # Calcula TODAS las métricas
        metrics = metrics_calculator.calculate_all_metrics(chatgpt_res, deepseek_res)

        # Usa directamente la complejidad ya calculada
        complexity_chatgpt = metrics['complexity_chatgpt']
        complexity_deepseek = metrics['complexity_deepseek']

        # Similaridad global
        similarity = metrics['similarity'] * 100

        # Guarda en la base
        result = BenchmarkResult.objects.create(
            input_text=text,
            chatgpt_response=chatgpt_res,
            deepseek_response=deepseek_res,
            metrics={
                'similarity': similarity,
                'complexity_chatgpt': complexity_chatgpt,
                'complexity_deepseek': complexity_deepseek,
                'similarity_details': metrics['similarity_details'],
                'details_chatgpt': metrics['details_chatgpt'],
                'details_deepseek': metrics['details_deepseek'],
            }
        )

        return Response({
            'id': result.id,
            'input_text': text[:100] + '...' if len(text) > 100 else text,
            'chatgpt': chatgpt_res,
            'deepseek': deepseek_res,
            'metrics': result.metrics,
            'created_at': result.created_at
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error en benchmark_api: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Error interno al procesar la solicitud'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def metrics_api(request, result_id):
    """
    Endpoint para obtener métricas específicas
    """
    try:
        result = BenchmarkResult.objects.get(id=result_id)

        response_data = {
            'id': result.id,
            'input_preview': result.input_text[:100] + '...' if len(result.input_text) > 100 else result.input_text,
            'created_at': result.created_at,
            'similarity': result.metrics.get('similarity'),
            'complexity_chatgpt': result.metrics.get('complexity_chatgpt'),
            'complexity_deepseek': result.metrics.get('complexity_deepseek'),
            'similarity_details': result.metrics.get('similarity_details', {}),
            'details_chatgpt': result.metrics.get('details_chatgpt', {}),
            'details_deepseek': result.metrics.get('details_deepseek', {})
        }

        return Response(response_data)

    except BenchmarkResult.DoesNotExist:
        return Response(
            {'error': f'Resultado con ID {result_id} no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )

    except Exception as e:
        logger.error(f"Error en metrics_api: {str(e)}", exc_info=True)
        return Response(
            {'error': 'Error al recuperar métricas'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
