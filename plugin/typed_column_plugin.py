from typing import Optional, Callable

from mypy.plugin import Plugin, AttributeContext
from mypy.types import Type, Instance
from mypy.subtypes import is_subtype

class TypedColumnPlugin(Plugin):
    def get_attribute_hook(self, fullname: str) -> Optional[Callable[[AttributeContext], Type]]:
        # Fullname isn't very useful, because we don't know the name of the
        # base model (as its instead embedded in the signature of TypedColumn.
        return typed_column_callback

def is_typed_column(typ: Type) -> bool:
    # TODO If theres a way to get the TypedColumn by name, we could use is_subtype instead.
    # Unlike other types, its hard to directly inject it this way...
    return isinstance(typ, Instance) and typ.type.fullname() == 'typed_sqlalchemy.declarative.TypedColumn'

def typed_column_callback(ctx: AttributeContext) -> Type:
    # Short circuit fast if we aren't even looking at a typed column.
    if not is_typed_column(ctx.default_attr_type):
        return ctx.default_attr_type

    left_type = ctx.type
    default_attr_type = ctx.default_attr_type

    assert isinstance(default_attr_type, Instance)
    if not isinstance(left_type, Instance):
        return ctx.default_attr_type

    base_model_type = default_attr_type.args[0]
    actual_ret_type = default_attr_type.args[1]

    if is_subtype(left_type, base_model_type):
        return actual_ret_type
    return ctx.default_attr_type

def plugin(version):
    return TypedColumnPlugin
