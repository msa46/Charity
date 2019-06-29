from flask_restplus import Api
from .Charity import api as charity_api
from .Campaign import api as campaign_api
from .Destitute import api as destitute_api
from .Financial import api as financial_api
api = Api(
    title='Charity project',
    version='0.1',
    description='Implementation of Charity as Database project'
)

api.add_namespace(charity_api)
api.add_namespace(campaign_api)
api.add_namespace(destitute_api)
api.add_namespace(financial_api)