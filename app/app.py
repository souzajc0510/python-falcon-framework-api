import falcon
from resources import athlete
from resources import plan
from resources import exercise
from services import database_service

from middlewares import (
    ContentEncodingMiddleware,
)

conn = database_service.connect()

api = falcon.API(middleware=[
    ContentEncodingMiddleware(),
])

# api = falcon.API()
athlete = athlete.Athlete(conn, database_service)
plan = plan.Plan(conn, database_service)
exercise = exercise.Exercise(conn, database_service)

api.add_route('/athletes/{id}', athlete)
api.add_route('/athletes', athlete, suffix='collection')
api.add_route('/plans/{id}', plan)
api.add_route('/plans', plan, suffix='collection')
api.add_route('/exercises/{id}', exercise)
api.add_route('/exercises', exercise, suffix='collection')
