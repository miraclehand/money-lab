from flask import Blueprint
#from yp_fin_utils.models import MarketModelFactory


api_routes = Blueprint('api_routes', __name__)

@api_routes.route('/api/simulation/<string:country>', methods=['GET'])
def query_simulation_data_route(country):
    #stock_model = MarketModelFactory.get_model('STOCK', country)

    #query = {'crud': {'$ne': 'D'}}
    #if ticker:
    #    query['ticker'] = ticker

    #stock_query = stock_model.objects.raw(query)
    #stocks = [stock.to_dict for stock in stock_query]

    #return {'stocks':stocks}
    return {}
