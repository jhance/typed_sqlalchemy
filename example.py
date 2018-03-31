from uuid import UUID, uuid4
from typed_sqlalchemy.declarative import DefaultBaseModel, TypedColumn
from typed_sqlalchemy.session import typed_session

from typing import NewType, Text

FooId = NewType('FooId', UUID)

class FooModel(DefaultBaseModel[FooId]):
    id = TypedColumn() # type: TypedColumn[FooModel, FooId]

    string_field = TypedColumn # type: TypedColumn[FooModel, Text]

session = typed_session(DefaultBaseModel, None)
reveal_type(session)
query = session.query(FooModel)
reveal_type(query)

foo = query.get(FooId(uuid4()))
reveal_type(foo)

foo_id, foo_str = session.query(FooModel.id, FooModel.string_field).filter(
    FooModel.id == FooId(uuid4()),
).one()
reveal_type(foo_id)
reveal_type(foo_str)
