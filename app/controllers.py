from app.routers import opencv_app_router
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import tempfile
import shutil
from app.services import VideoAnalyzer
from app.repository import save_analysis_result


@opencv_app_router.post("/analyze")
async def analyze_video(file: UploadFile = File()):
    """
    Загружает видеофайл, анализирует его, и возвращает список "нарушений".
    """
    # Сохраняем видео во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        shutil.copyfileobj(file.file, tmp)
        temp_video_path = tmp.name

    try:
        analyzer = VideoAnalyzer()
        violations = analyzer.analyze(temp_video_path)

        analysis_id = await save_analysis_result(file.filename, violations)

        return JSONResponse(
            {
                "status": "ok",
                "analysis_id": analysis_id,
                "file_name": file.filename,
                "violations_found": len(violations),
                "violations": violations,
            }
        )
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)
