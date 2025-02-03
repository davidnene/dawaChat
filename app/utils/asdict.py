from sqlalchemy.inspection import inspect

def asdict(obj):
    """Convert SQLAlchemy object to dictionary dynamically."""
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}