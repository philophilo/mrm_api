from graphql import GraphQLError

from api.office.models import Office
from api.location.models import Location
from api.room.models import Room as RoomModel
from api.room_resource.models import Resource as ResourceModel
from helpers.auth.user_details import get_user_from_db
from helpers.room_filter.room_filter import location_join_resources, location_join_room  # noqa: E501


class Admin_roles():

    def create_rooms_update_delete_office(self, office_id):
        admin_details = get_user_from_db()
        get_office = Office.query.filter_by(id=office_id).first()
        location = Location.query.filter_by(id=get_office.location_id).first()
        if admin_details.location != location.name:
            raise GraphQLError("You are not authorized to make changes in " + location.name)  # noqa: E501

    def update_delete_rooms_create_resource(self, room_id):
        admin_details = get_user_from_db()
        location_query = location_join_room()
        room_location = location_query.filter(RoomModel.id == room_id).first()  # noqa: E501
        if admin_details.location != room_location.name:
            raise GraphQLError("You are not authorized to make changes in " + room_location.name)  # noqa: E501

    def create_office(self, location_id):
        admin_details = get_user_from_db()
        location = Location.query.filter_by(id=location_id).first()
        if location.name != admin_details.location:
            raise GraphQLError("You are not authorized to make changes in " + location.name)  # noqa: E501

    def update_resource(self, resource_id, room_id):
        admin_details = get_user_from_db()
        location_query = location_join_resources()
        resource_location = location_query.filter(ResourceModel.id == resource_id).first()  # noqa: E501

        if admin_details.location != resource_location.name:
            raise GraphQLError("You are not authorized to make changes in " + resource_location.name)  # noqa: E501
        # check room_id incase the resource room is to be updated.
        location_query = location_join_room()
        room_location = location_query.filter(RoomModel.id == room_id).first()  # noqa: E501
        if admin_details.location != room_location.name:
            raise GraphQLError("You are not authorized to make changes in " + room_location.name)  # noqa: E501

    def delete_resource(self, resource_id):
        admin_details = get_user_from_db()
        location_query = location_join_resources()
        resource_location = location_query.filter(ResourceModel.id == resource_id).first()   # noqa: E501
        if admin_details.location != resource_location.name:
            raise GraphQLError("You are not authorized to make changes in " + resource_location.name)  # noqa: E501

    def admin_location_for_analytics_view(self):
        """
        Return admin's location for viewing analytics data
        """
        admin_details = get_user_from_db()
        location = Location.query.filter_by(name=admin_details.location).first()
        return location.id


admin_roles = Admin_roles()
