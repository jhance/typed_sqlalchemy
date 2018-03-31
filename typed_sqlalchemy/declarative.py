from six import with_metaclass

from sqlalchemy.clause import FilterClause
from sqlalchemy.declarative import as_declarative, DeclarativeMeta
from sqlalchemy.sql.visitors.VisitableType import VisitableType
from sqlalchemy import Column

from typing import Generic, GenericMeta, TypeVar, Union, Any

# Metaclass needed to define TypedColumn properly.
class VisitableGeneric(GenericMeta, VisitableType):
    pass

class DeclarativeGeneric(GenericMeta, DeclarativeMeta):
    pass

# BaseModel class
B = TypeVar('B')

# Attribute type
T = TypeVar('T')

# Primary key type
P = TypeVar('P')


class TypedColumn(with_metaclass(VisitableGeneric, Generic[B, T], Column)):
    def __eq__(self, other):
        # type: (Any) -> FilterClause
        pass

@as_declarative(metaclass=DeclarativeGeneric)
class DefaultBaseModel(Generic[P]):
    pass
