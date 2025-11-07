from app.routers import opencv_app_router
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse, PlainTextResponse
import tempfile
import shutil
from app.services import (
    VideoAnalyzer,
    VIDEOS_PROCESSED,
    PROCESSING_TIME,
    PROCESSING_ERRORS,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from app.repository import save_analysis_result
import time


@opencv_app_router.post("/analyze")
async def analyze_video(file: UploadFile = File()):
    """
    Загружает видеофайл, анализирует его, и возвращает список "нарушений".
    """
    start_time = time.time()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_video_path = tmp.name
    analyzer = VideoAnalyzer()

    try:
        violations = analyzer.analyze(temp_video_path)
        analysis_id = await save_analysis_result(file.filename, violations)
        VIDEOS_PROCESSED.inc()  # Увеличиваем счетчик успешных обработок

        processing_time = time.time() - start_time
        PROCESSING_TIME.observe(processing_time)

        return JSONResponse(
            {
                "status": "ok",
                "analysis_id": analysis_id,
                "file_name": file.filename,
                "violations_found": len(violations),
                "violations": violations,
                "processing_time_sec": round(processing_time, 2),
            }
        )
    except Exception as e:
        PROCESSING_ERRORS.inc()  # Фиксируем ошибку
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


# --- 🔹 Эндпоинт для Prometheus ---
@opencv_app_router.get("/metrics")
def metrics():
    """Отдаёт метрики Prometheus."""
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)
