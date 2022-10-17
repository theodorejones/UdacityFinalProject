from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Renter, Rental
#from auth import AuthError, requires_auth



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return jsonify({'message': 'Udacity Capstone Project'})

    #########################
    # Renters
    #########################
    @app.route('/renters', methods=['GET'])
    #@requires_auth('get:renters')
    def get_renters(token):
        try:
            renters_details = list(map(Renter.format, Renter.query.all()))
            return jsonify({"success": True,
                            "renters": renters_details,
                            "total_renters": len(Renter.query.all()),
                            }), 200
        except Exception:
            abort(404)

    @app.route('/renters/<int:renter_id>', methods=['DELETE'])
    #@requires_auth('delete:renters')
    def delete_renter(token, renter_id):
        try:

            renter = Renter.query.filter(Renter.id == renter_id).one_or_none()
            if renter is None:
                abort(404)

            renter.delete()
            return jsonify({
                "success": True,
                "message": "this renter id deleted",
                "delete": renter_id,
                "total_renters": len(Renter.query.all())
            }), 200
        except Exception:
            abort(422)

    @app.route('/renters', methods=['POST'])
    #@requires_auth('post:renters')
    def create_renter(token):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if any(arg is None for arg in [new_name, new_age, new_gender]
               )or'' in[new_name, new_age, new_gender]:
            abort(400)
        try:
            new_renter = Renter(name=new_name, age=new_age, gender=new_gender)
            new_renter.insert()
            return jsonify({
                "success": True,
                "created": new_renter.id
            }), 200
        except Exception:
            abort(422)

    @app.route('/rentals', methods=['POST'])
    #@requires_auth('post:rentals')
    def create_rental(token):
        body = request.get_json()
        new_title = body.get('title', None)

        if any(arg is None for arg in [new_title])or'' in[new_title]:
            abort(400)
        try:
            new_rental = Rental(title=new_title)
            new_rental.insert()
            return jsonify({
                "success": True,
                "created": new_rental.id
            }), 200
        except Exception:
            abort(422)

    @app.route('/renters/<int:id>', methods=['PATCH'])
    #@requires_auth('patch:renters')
    def patch_renter(jwt, id):
        renter = Renter.query.filter(Renter.id == id).one_or_none()
        print('Renter ', renter)
        if renter is None:
            print('returning 404')
            abort(404)
        data = request.get_json()
        print('data ', data)
        name = data.get('name')
        age = data.get('age')
        gender = data.get('gender')
        try:
            renter.name = name
            renter.age = age
            renter.gender = gender
            print('inside try block')
            renter.update()
        except Exception:
            print('update renter failed with 422')
            abort(422)
        renters = Renter.query.all()
        try:
            print('Get all renters')
            renters = [renter.format() for renter in renters]
            return jsonify({
                'success': True,
                'renters': renters
            }), 200
        except Exception:
            print('got exception 500')
            abort(500)

    ##########################
    # Rentals
    ##########################
    @app.route('/rentals', methods=['GET'])
    #@requires_auth('get:rentals')
    def get_rentals(token):
        try:
            rentals_details = list(map(Rental.format, Rental.query.all()))
            return jsonify({"success": True,
                            "rentals": rentals_details,
                            "total_rentals": len(Rental.query.all())
                            }), 200
        except Exception:
            abort(404)

    @app.route('/rentals/<int:rental_id>', methods=['DELETE'])
    #@requires_auth('delete:rentals')
    def delete_rental(token, rental_id):
        try:
            rental = Rental.query.filter(Rental.id == rental_id).one_or_none()
            if rental is None:
                abort(404)

            rental.delete()
            return jsonify({
                "success": True,
                "message": "this rental id deleted",
                "delete": rental_id,
                "total_rentals": len(Rental.query.all())
            }), 200
        except Exception:
            abort(422)

    @app.route('/rentals/<int:rental_id>', methods=['PATCH'])
    #@requires_auth('patch:rentals')
    def edit_rental(token, rental_id):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            rental = Rental.query.filter(Rental.id == rental_id).one_or_none()
            if rental is None:
                abort(404)
            if any(arg is None for arg in [new_title])or'' in[new_title]:
                abort(400)

            rental.title = new_title
            rental.release_date = new_release_date

            rental.update()
            return jsonify({
                "success": True,
                "rental": [Rental.query.get(rental_id).format()]
            }), 200

        except Exception:
            abort(401)

    #########################
    # Error Handling
    #########################
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    '''@app.errorhandler(401)
    def Unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized Error"
        }), 401

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response'''

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
