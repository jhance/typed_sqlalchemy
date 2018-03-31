from typing_extensions import Protocol

from typing import Generic, Any, Sequence, Union, Iterable, TypeVar, Type, Optional

from sqlalchemy.orm.session import Session as _RawSession
from typed_sqlalchemy.declarative import TypedColumn
from typed_sqlalchemy.clause import FilterClause


# Refers to the "Base model" class thats attached to the session.
# This is a phantom type used by the plugin infra.
B = TypeVar('B')

# Expected to inherit from M. This can't really be encoded, but
# typed_sqlalchemy can guarantee it to be true.
M = TypeVar('M')

Q = TypeVar('Q')

P = TypeVar('P')

def typed_session(phantom, raw_session):
    # type: (Type[B], _RawSession) -> Session[B]
    return raw_session


# Object that wraps a sqlalchemy session object.
class Session(Generic[B]):
    """Protocol for a sqlalchemy session.
    """
    def query(self, *args):
        # type: (*Union[Type[B], TypedColumn[B, Any]]) -> QueryPlaceholder[Query, SingularQuery, TypedColumn]
        """QueryPlaceholder is rewritten dynamically to either Query or
        SingularQuery. (SingularQuery is used in the case where there is
        only a singular argument and it happens to be a subclass of B).
        """
        pass

    def add(self, model, _warn=True):
        # type: (B, bool) -> None
        pass

    def add_all(self, models):
        # type: (Iterable[B]) -> None
        pass

    def commit(self):
        # type: () -> None
        pass


class Query(Generic[B, Q], Iterable[Q]):
    """Actual query type. B is the base model, and Q is the return type of the
    query (often a tuple).
    """
    def filter(self, *clauses):
        # type: (*FilterClause) -> Query[B, Q]
        pass

    def one(self):
        # type: () -> Q
        pass

    def one_or_none(self):
        # type: () -> Optional[Q]
        pass

    def all(self):
        # type: () -> Sequence[Q]
        pass


class SingularQuery(Generic[B, M, P]):
    """B is the base model, M is the return type (this time not a tuple type),
    and P is the p id type for Q. (Its acceptable for I to be a tuple)
    """
    def get(self, primary_key):
        # type: (P) -> Optional[M]
        pass



_Query = TypeVar('_Query', bound=Query)
_SingularQuery = TypeVar('_SingularQuery', bound=SingularQuery)
_TypedColumn = TypeVar('_TypedColumn')
class QueryPlaceholder(object, Generic[_Query, _SingularQuery, _TypedColumn]):
    """Placeholder for a Query object.
    """
