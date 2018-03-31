from mypy.plugin import Plugin, MethodContext
from mypy.types import Type, CallableType, Instance, TupleType, TypeType
from mypy.subtypes import is_subtype

class QueryPlugin(Plugin):
    def get_method_hook(self, fullname):
        if fullname == 'typed_sqlalchemy.session.Session.query':
            return session_hook
        #if fullname == 'typed_sqlalchemy.declarative.TypedColumn.__eq__':
        #    return filter_typed_col_hook
        return None

def filter_typed_col_hook(ctx: MethodContext):
    assert isinstance(ctx.type, Instance)
    # Disgusting hack (don't know how to get FilterClause directly)
    print('foo')
    print(ctx.type.type)
    for base in ctx.type.type.bases:
        print(base.type)
        print(base.args)
    return ctx.type.type.bases[0].args[0]

def session_hook(ctx: MethodContext) -> Type:
    if not isinstance(ctx.default_return_type, Instance):
        print('default ret type not instance')
        return ctx.default_return_type

    if ctx.default_return_type.type.fullname() != 'typed_sqlalchemy.session.QueryPlaceholder':
        print('default ret type not placheolder')
        print(ctx.default_return_type.type.fullname())
        return ctx.default_return_type

    assert isinstance(ctx.type, Instance)
    assert ctx.type.type.fullname() == 'typed_sqlalchemy.session.Session'

    base_model_type = ctx.type.args[0]

    # We hijack these from the generic return value in order to construct them.
    query_type_info = ctx.default_return_type.args[0].type
    singular_query_type_info = ctx.default_return_type.args[1].type
    typed_column_type_info = ctx.default_return_type.args[2].type

    # For now, we support exactly two arg types: typed columns and models.
    # We record whether we found a model because if we only have one non-model
    # then we are still a tuple, but a single model becomes a singular query.
    has_model = False
    return_types = []
    for arg_type in ctx.arg_types[0]:
        # I'm kind of surprised that its a CallableType
        if isinstance(arg_type, CallableType) and is_subtype(arg_type.ret_type, base_model_type):
            has_model = True
            return_types.append(arg_type.ret_type)

        # Case 2: TypedColumn
        elif isinstance(arg_type, Instance) and arg_type.type.fullname() == typed_column_type_info.fullname():
            return_types.append(arg_type.args[1])

    if has_model and len(return_types) == 1:
        model_type = return_types[0]
        primary_key_type = model_type.type.bases[0].args[0]

        return Instance(
            singular_query_type_info,
            # Base model, return type, primary key
            [base_model_type, return_types[0], primary_key_type],
        )
    else:
        fallback = ctx.api.named_generic_type('builtins.tuple', [])
        return Instance(
            query_type_info,
            # Base model, return type tuple 
            [base_model_type, TupleType(return_types, fallback)],
        )


def plugin(version):
    return QueryPlugin
