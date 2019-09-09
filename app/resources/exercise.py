import falcon
from webargs import fields
from webargs.falconparser import use_args


class Exercise(object):
    post_request_args = {"name": fields.Str(required=True), "description": fields.Str(required=True)}

    def __init__(self, conn, database_service):
        self.conn, self.database_service, self.resource_name = conn, database_service, self.__class__.__name__

    def on_delete(self, req, resp, id):

        try:
            q = " ".join(
                ["DELETE", "FROM", self.resource_name.lower(), "WHERE", self.resource_name.lower() + "_id = %s"])
            q_resp = self.database_service.run_delete_query(self.conn, q, [id])
            if not q_resp['status']:
                output = {"status": True, "message": q_resp['message'],
                          "data": None}
            else:
                output = {"status": True, "message": self.resource_name + " was deleted successfully!", "data": None}

            resp.status = falcon.HTTP_200
            resp.body = output
        except Exception as error:
            output = {"status": False, "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output

    def on_get(self, req, resp, id):
        try:
            cur = self.conn.cursor()

            q = " ".join(
                ["SELECT", "*", "FROM", self.resource_name.lower(), "wHERE", self.resource_name.lower() + "_id = %s"])
            q_resp = self.database_service.run_get_query(cur, q, [id])
            if not q_resp['status']:
                output = {"status": True, "message": q_resp['message'],
                          "data": None}
            else:
                output = {"status": True, "message": None,
                          'data': self.database_service.set_columns(q_resp['data'], cur)}

            resp.status = falcon.HTTP_200
            resp.body = output
        except Exception as error:
            output = {"status": False, "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output

    def on_get_collection(self, req, resp):
        try:
            cur = self.conn.cursor()
            q = " ".join(
                ["SELECT * FROM", self.resource_name.lower()])
            q_resp = self.database_service.run_get_query(cur, q, [])
            if not q_resp['status']:
                output = {"status": True, "message": q_resp['message'],
                          "data": None}
            else:
                output = {"status": True, "message": None,
                          'data': self.database_service.set_columns(q_resp['data'], cur)}

            resp.status = falcon.HTTP_200
            resp.body = output
        except Exception as error:
            output = {"status": False, "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output

    def on_put(self, req, resp, id):
        try:

            cur = self.conn.cursor()
            get_q = " ".join(
                ["SELECT name,description FROM", self.resource_name.lower(), "wHERE",
                 self.resource_name.lower() + "_id = %s"])
            get_resp = self.database_service.run_get_query(cur, get_q, [id])

            record = list(self.database_service.set_columns(get_resp['data'], cur))[0]

            request = req.media
            for index in record.keys():
                if index in request.keys():
                    record[index] = request[index]
            record['id'] = id

            update_q = " ".join(
                ["UPDATE", self.resource_name.lower(), "SET name=%s, description=%s WHERE",
                 self.resource_name.lower() + "_id=%s RETURNING ", self.resource_name.lower() + "_id;"])

            update_resp = self.database_service.run_upsert_query(self.conn, update_q, record.values())
            if not update_resp['status']:
                output = {"status": True, "message": update_resp['message'],
                          "data": None}
            else:
                response_data = {
                    "id": update_resp['data'],
                    "name": record['name'],
                    "description": record['description']
                }

                output = {"status": True, "message": self.resource_name + " is updated successfully!",
                          "data": response_data}

            resp.status = falcon.HTTP_201
            resp.body = output

        except Exception as error:
            output = {"status": False, "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output

    @use_args(post_request_args)
    def on_post_collection(self, req, resp, args):
        try:
            q = " ".join(
                ["INSERT INTO", self.resource_name.lower(),
                 "(name,description) VALUES (%s,%s) RETURNING",
                 self.resource_name.lower() + "_id;"])

            params = {'name': args['name'], 'descriptoin': args['description']}

            q_resp = self.database_service.run_upsert_query(self.conn, q, params.values())

            if not q_resp['status']:
                output = {"status": True, "message": q_resp['message'],
                          "data": None}
            else:
                response_data = {
                    "id": q_resp['data'],
                    "name": args['name'],
                    "description": args['description']
                }

                output = {"status": True, "message": self.resource_name + " is added successfully!",
                          "data": response_data}

            resp.status = falcon.HTTP_201
            resp.body = output
        except Exception as error:
            output = {"status": False, "message": str(error), "data": None}
            resp.status = falcon.HTTP_500
            resp.body = output
