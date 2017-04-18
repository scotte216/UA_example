from Data import common
from flask import Flask, request, abort
from flask_restful import Resource, Api, reqparse
from json import dumps


app = Flask(__name__)
api = Api(app)


# @require_authorization
class NamedUsersList(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start')
        start = parser.parse_args()['start']
        try:
            query, next_page = common.get_page(start)
            if next_page:
                result = {'named_users': query,
                          'next_page': request.base_url + '?start=' + next_page}
            else:
                result = {'named_users': query}
            return result
        except Exception as e:
            # Abort codes as appropriate for type of exception
            # Log e
            abort(500)


# @require_authorization
class NamedUsers(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        user_id = parser.parse_args()['id']
        query = common.get(user_id)
        result = {}
        if query:
            result = {'ok': True,
                      'named_user': query}
        else:
            abort(404, 'User not found -- ' + user_id)
        return result


# @require_authorization
class Associate(Resource):
    def post(self):
        args = request.get_json()
        try:
            common.associate(args['channel_id'], args['device_type'], args['named_user_id'])
        except KeyError:
            abort(400)
        return {'ok': True}


# @require_authorization
class Disassociate(Resource):
    def post(self):
        args = request.get_json()
        try:
            common.disassociate(args['channel_id'], args['device_type'])
        except KeyError:
            abort(400)
        return {'ok': True}


api.add_resource(NamedUsersList, '/api/named_users')
api.add_resource(NamedUsers, '/api/named_users/')
api.add_resource(Associate, '/api/named_users/associate')
api.add_resource(Disassociate, '/api/named_users/disassociate')

if __name__ == '__main__':
    app.run()
