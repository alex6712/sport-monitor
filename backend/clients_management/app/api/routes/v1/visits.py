from typing import Annotated
from uuid import UUID
from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    status,
    Body,
    Path, HTTPException,
)
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.session import get_session
from app.api.dependencies.tokens import validate_access_token
from app.database.tables.entities import User, Visit
from app.schemas.v1.requests import VisitRequest
from app.schemas.v1.responses import (
    CreatedResponse,
    StandardResponse,
)

router = APIRouter(
    prefix="/visits",
    tags=["visits"],
)


@router.post(
    "/start",
    response_model=CreatedResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Добавляет запись о новом посещении.",
)
async def start_visit(
    visit_data: Annotated[VisitRequest, Body()],
    _: Annotated[User, Depends(validate_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    session.add(visit := Visit(**visit_data.model_dump()))
    await session.flush()

    try:
        await session.commit()
    except Exception as _:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизвестная ошибка.",
        )

    return CreatedResponse(
        message="Посещение успешно зарегистрировано.",
        id=visit.id,
    )


@router.put(
    "/end/{visit_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Закрывает посещение.",
)
async def end_visit(
    visit_id: Annotated[UUID, Path()],
    _: Annotated[User, Depends(validate_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    visit: Visit = await session.scalar(select(Visit).where(Visit.id == visit_id))
    visit.visit_end = datetime.now(timezone.utc)

    try:
        await session.commit()
    except Exception as _:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизвестная ошибка.",
        )

    return StandardResponse(message="Посещение успешно завершено.")


@router.delete(
    "/{visit_id}",
    response_model=StandardResponse,
    status_code=status.HTTP_200_OK,
    summary="Удаляет запись о посещении.",
)
async def delete_season_ticket(
    visit_id: Annotated[UUID, Path()],
    _: Annotated[User, Depends(validate_access_token)],
    session: Annotated[AsyncSession, Depends(get_session)]
):
    await session.execute(delete(Visit).where(Visit.id == visit_id))

    try:
        await session.commit()
    except Exception as _:
        await session.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизвестная ошибка.",
        )

    return StandardResponse(message="Посещение успешно удалено.")
