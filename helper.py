from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_or_create_async(db: AsyncSession, model, defaults: dict = None, **kwargs):
    """
    Asynchronously retrieves an instance of the specified model from the database matching the given criteria,
    or creates it with the provided defaults if it does not exist.
    Args:
        db (AsyncSession): The asynchronous database session to use for the query and creation.
        model: The SQLAlchemy model class to query or create.
        defaults (dict, optional): A dictionary of default values to use when creating a new instance. Defaults to None.
        **kwargs: Field lookups to filter the query.
    Returns:
        tuple: A tuple containing the instance and a boolean indicating whether the instance was created (True) or retrieved (False).
    """

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
    """
    Retrieve an existing instance of the specified model from the database that matches the given criteria,
    or create a new one if it does not exist.
    Args:
        db (Session): The SQLAlchemy database session to use for the query and creation.
        model: The SQLAlchemy model class to query or create.
        defaults (dict, optional): A dictionary of default values to use when creating a new instance.
        **kwargs: Field lookups for filtering the query and for creating a new instance.
    Returns:
        tuple: A tuple containing the instance and a boolean indicating whether the instance was created (True) or retrieved (False).
    """

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
  
    db: AsyncSession,
    model,
    defaults: dict = None,
    **kwargs,
):
    
    """
    Asynchronously updates an existing record or creates a new one in the database.
    If a record matching the provided filter criteria (`**kwargs`) exists, it updates the record with the values from `defaults`.
    If no such record exists, it creates a new record with the combined parameters from `defaults` and `**kwargs`.
    Args:
        db (AsyncSession): The asynchronous SQLAlchemy session to use for database operations.
        model: The SQLAlchemy model class to query or create.
        defaults (dict, optional): A dictionary of fields and values to update or set on the record. Defaults to None.
        **kwargs: Arbitrary keyword arguments used as filter criteria to find the existing record.
    Returns:
        tuple: A tuple containing the instance and a boolean.
            - instance: The updated or newly created model instance.
            - created (bool): True if a new record was created, False if an existing record was updated.
    """
    

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
    """
    Creates a new instance of the given SQLAlchemy model or updates an existing one.
    If an instance matching the provided filter criteria (`kwargs`) exists, it updates the instance with the values from `defaults`.
    Otherwise, it creates a new instance with the combined parameters from `kwargs` and `defaults`.
    Args:
        db (Session): SQLAlchemy database session.
        model: SQLAlchemy model class.
        defaults (dict, optional): Fields and values to update or set on the instance. Defaults to None.
        **kwargs: Fields used to identify the instance (filter criteria).
    Returns:
        tuple: (instance, created)
            instance: The created or updated model instance.
            created (bool): True if a new instance was created, False if an existing instance was updated.
    """

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
