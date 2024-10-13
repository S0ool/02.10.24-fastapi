from fastapi import HTTPException
from sqlalchemy import select
from database import async_session_maker


class BaseRepository:
    model = None
    @classmethod
    async def get_by(cls,**filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)

            return result.scalar_one_or_none()

    @classmethod
    async def get_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)

            return result

    @classmethod
    async def get_by_id(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            model = session.execute(query)
            model = model.scalar_one_or_none()
            if model is None:
                raise HTTPException(status_code=404, detail='not found')

            return model

    @classmethod
    async def create(cls, **data):
        async with async_session_maker() as session:
            model = cls.model(**data)
            session.add(model)
            session.commit()

            return model

    @classmethod
    async def update(cls, model_id, data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            model = session.execute(query)
            model = model.scalar_one_or_none()
            if model is None:
                raise HTTPException(status_code=404, detail='not found')
            for key, value in data.items():
                setattr(model, key, value)
            session.add(model)
            await session.commit()

            return model

    @classmethod
    async def delete(cls, model_id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            model = session.execute(query)
            model = model.scalar_one_or_none()
            if model is None:
                raise HTTPException(status_code=404,detail='not found')
            session.delete(model)
            session.commit()

            return 'deleted'
