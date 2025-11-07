from typing import List, Dict
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.schemas import Base, VideoAnalysis, Violation
from settings import settings


# Асинхронный движок для работы с video_db
engine = create_async_engine(settings.db_url, echo=False, future=True)
AsyncSessionLocal = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)


async def ensure_database_exists():
    """
    Проверяет наличие БД video_db, если нет — создаёт её.
    Использует подключение к "postgres" (системной базе).
    """
    root_engine = create_async_engine(
        settings.system_db_url, isolation_level="AUTOCOMMIT"
    )
    async with root_engine.connect() as conn:
        # Проверяем, существует ли база
        result = await conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = 'video_db'")
        )
        exists = result.scalar() is not None
        if not exists:
            await conn.execute(
                text("CREATE DATABASE video_db OWNER postgres ENCODING 'UTF8';")
            )
            print("✅ База данных video_db создана.")
        else:
            print("ℹ️ База данных video_db уже существует.")
    await root_engine.dispose()


async def init_db():
    """
    Инициализация базы данных: создание таблиц, если их нет.
    """
    await ensure_database_exists()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Таблицы успешно созданы / обновлены.")


async def save_analysis_result(file_name: str, violations: List[Dict]):
    """Сохраняет результаты анализа видео в БД"""
    async with AsyncSessionLocal() as session:
        analysis = VideoAnalysis(file_name=file_name)
        session.add(analysis)
        await session.flush()  # получаем ID

        for v in violations:
            session.add(
                Violation(
                    analysis_id=analysis.id,
                    frame=v["frame"],
                    type=v["type"],
                    confidence=v["confidence"],
                )
            )
        await session.commit()
        return analysis.id
