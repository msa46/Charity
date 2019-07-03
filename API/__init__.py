from flask_restplus import Api
from .Charity import api as charity_api
from .Campaign import api as campaign_api
from .Destitute import api as destitute_api
from .Financial import api as financial_api
from .NonFinancial import api as non_financial_api
from .Member import api as member_api
from .Worker import api as worker_api

api = Api(
    title='Charity project',
    version='0.1',
    description='Implementation of Charity as Database project'
)

api.add_namespace(charity_api)
api.add_namespace(campaign_api)
api.add_namespace(destitute_api)
api.add_namespace(financial_api)
api.add_namespace(non_financial_api)
api.add_namespace(member_api)
api.add_namespace(worker_api)