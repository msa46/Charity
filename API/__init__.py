from flask_restplus import Api
from .Charity import api as charity_api

api = Api(
    title='Charity project',
    version='0.1',
    description='Implementation of Charity as Database project'
)

api.add_namespace(charity_api)