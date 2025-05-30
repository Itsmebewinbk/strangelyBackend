from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_or_create_async(db: AsyncSession, model, defaults: dict = None, **kwargs):
    defaults = defaults or {}
    stmt = select(model).filter_by(**kwargs)
    result = await db.execute(stmt)
    instance = result.scalars().first()

    if instance:
        return instance, False
    params = {**kwargs, **defaults}
    instance = model(**params)
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance, True


async def get_or_create(db: Session, model, defaults: dict = None, **kwargs):
    defaults = defaults or {}

    instance = db.query(model).filter_by(**kwargs).first()

    if instance:
        return instance, False
    params = {**kwargs, **defaults}
    instance = model(**params)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance, True


async def update_or_create_async(
    db: AsyncSession, model, defaults: dict = None, **kwargs
):
    defaults = defaults or {}
    stmt = select(model).filter_by(**kwargs)
    result = await db.execute(stmt)
    instance = result.scalars().first()

    if instance:
        for key, value in defaults.items():
            setattr(instance, key, value)
        await db.commit()
        await db.refresh(instance)
        return instance, False

    params = {**kwargs, **defaults}
    instance = model(**params)
    db.add(instance)
    await db.commit()
    await db.refresh(instance)
    return instance, True


def update_or_create(db: Session, model, defaults: dict = None, **kwargs):
    defaults = defaults or {}
    instance = db.query(model).filter_by(**kwargs).first()

    if instance:
        for key, value in defaults.items():
            setattr(instance, key, value)
        db.commit()
        db.refresh(instance)
        return instance, False

    params = {**kwargs, **defaults}
    instance = model(**params)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance, True
