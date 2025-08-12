from abc import ABC, abstractmethod
from typing import Dict, Generic, List, Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy.exc import MultipleResultsFound
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.interfaces.database_repository import IDefaultRepository

T = TypeVar("T", bound=BaseModel)
M = TypeVar("M", bound=SQLModel)


class BaseRepository(Generic[T, M], IDefaultRepository[T], ABC):
    """
    Implementação base genérica da interface IDefaultRepository para SQLModel.
    Esta classe é abstrata e deve ser herdada por repositórios específicos.
    """

    def __init__(self, session: AsyncSession, model: type[M], schema: type[T]):
        self.session = session
        self.model = model
        self.schema = schema

    @abstractmethod
    async def input(self, data: T) -> M:
        pass

    async def create(self, data: T):
        db_model = await self.input(data)
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        data.id = db_model.id
        return data

    async def update(self, data: T, _id: int):
        existing_db_model = await self.session.get(self.model, _id)
        if not existing_db_model:
            raise ValueError(f"{self.model.__name__} com ID {_id} não encontrado.")

        for key, value in data.model_dump(exclude_unset=True).items():
            if value and getattr(existing_db_model, key) != value:
                setattr(existing_db_model, key, value)

        self.session.add(existing_db_model)
        await self.session.commit()
        await self.session.refresh(existing_db_model)
        return self.schema.model_validate(existing_db_model.model_dump())

    async def delete(self, _id: int):
        data = await self.session.get(self.model, _id)
        if data:
            await self.session.delete(data)
            await self.session.commit()
            return True
        return False

    async def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[T]:
        query = select(self.model)
        if filters:
            for key, value in filters.items():
                query = query.where(getattr(self.model, key) == value)

        if order_by:
            query = query.order_by(getattr(self.model, order_by))

        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self.session.exec(query)
        return list(
            map(
                lambda data: self.schema.model_validate(data.model_dump()),
                result.all(),
            )
        )

    async def get_one(self, by: Dict) -> T:
        query = select(self.model)
        if not by:
            raise ValueError("O critério 'by' não pode estar vazio.")

        for key, value in by.items():
            query = query.where(getattr(self.model, key) == value)

        result = await self.session.exec(query)
        try:
            db_instance: M = result.one_or_none()
        except MultipleResultsFound:
            raise ValueError(  # pylint: disable=W0707
                f"Mais de um {self.model.__name__} encontrado para o critério: {by}"
            )  # pylint: disable=W0707

        if db_instance is None:
            raise ValueError(
                f"Nenhum {self.model.__name__} encontrado com o critério: {by}"
            )

        return self.schema.model_validate(db_instance.model_dump())
