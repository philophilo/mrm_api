import graphene
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType
from api.block.models import Block as BlockModel
from api.room.schema import Room
from api.office.models import Office
from helpers.room_filter.room_filter import room_join_location
from utilities.utility import validate_empty_fields
from helpers.auth.authentication import Auth


class Block(SQLAlchemyObjectType):
    class Meta:
        model = BlockModel


class CreateBlock(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        office_id = graphene.Int(required=True)
    block = graphene.Field(Block)

    @Auth.user_roles('Admin')
    def mutate(self, info, **kwargs):
        validate_empty_fields(**kwargs)
        block_name = BlockModel.query.filter_by(name=kwargs['name'].title()).all() # noqa
        if len(block_name) > 0:
            raise GraphQLError("Block aleady exists")
        get_office = Office.query.filter_by(id=kwargs['office_id']).first()
        if get_office is None:
            raise GraphQLError("Office not found")
        location = get_office.location.name
        if location.lower() == 'nairobi':
            block = BlockModel(**kwargs)
            block.save()
        else:
            raise GraphQLError("You can only create block in Nairobi")
        return CreateBlock(block=block)


class Query(graphene.ObjectType):
    all_blocks = graphene.List(Block)
    get_rooms_in_a_block = graphene.List(
        lambda: Room,
        block_id=graphene.Int()
    )

    def resolve_all_blocks(self, info):
        query = Block.get_query(info)
        return query.all()

    def resolve_get_rooms_in_a_block(self, info, block_id):
        query = Room.get_query(info)
        new_query = room_join_location(query)
        result = new_query.filter(BlockModel.id == block_id)
        return result


class Mutation(graphene.ObjectType):
    create_block = CreateBlock.Field()
