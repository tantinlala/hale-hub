from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource
from hale_hub.home_stats import get_formatted_home_stats
from hale_hub.outlet_interface import toggle_outlet, turn_on_outlet, turn_off_outlet
from hale_hub.automations import toggle_automation_state, get_automation_states


rest_api_blueprint = Blueprint('rest_api_blueprint', __name__)
rest_api_wrap = Api(rest_api_blueprint)


class HomeStatsAPI(Resource):
    def get(self):
        return jsonify(get_formatted_home_stats())


rest_api_wrap.add_resource(HomeStatsAPI, '/home_stats', endpoint='home_stats')


class OutletsAPI(Resource):
    def post(self, command):
        content = request.get_json(silent=True)
        for outlet_id in content['outlet_ids']:
            if command == 'toggle':
                toggle_outlet(outlet_id)
            elif command == 'on':
                turn_on_outlet(outlet_id)
            elif command == 'off':
                turn_off_outlet(outlet_id)

        return 'Got outlet request!'


rest_api_wrap.add_resource(OutletsAPI, '/outlets/<string:command>', endpoint='outlets')


class GetAutomationStatesAPI(Resource):
    def get(self):
        return jsonify(get_automation_states())


rest_api_wrap.add_resource(GetAutomationStatesAPI, '/get_automation_states', endpoint='get_automation_states')


class ToggleAutomationAPI(Resource):
    def post(self):
        content = request.get_json(silent=True)
        toggle_automation_state(content['key'])

        return 'Got toggle automation request'


rest_api_wrap.add_resource(ToggleAutomationAPI, '/toggle_automation', endpoint='toggle_automation')
