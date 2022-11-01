import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Renters, Rentals
from auth import AuthError, requires_auth

RECS_PER_PAGE = 12


def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    CORS Headers
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    To Keep a common pagination method to be called
    by different endpoints
    '''

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * RECS_PER_PAGE
        end = start + RECS_PER_PAGE

        recs_format = [record.format() for record in selection]
        page_recs = recs_format[start:end]
        return page_recs

    #auxiliary endpoint to get token
    '''@app.route('/authorization/url', methods=['GET'])
    def generate_auth_url():
        url = f'https://still-butterfly-7094.us.auth0.com/authorize' \
        f'?audience=udacityfinal' \
        f'&response_type=token&client_id=' \
        f'MAber3rpaDvIGkAtTP8pQVd5ttmR0xOs&redirect_uri=' \
        f'https://localhost:8080/login-results'
    return jsonify({'url': url})'''

    @app.route('/', methods=['GET'])
    def get_init():
        return jsonify({
            'success': True,
            'SampleTest': 'Hello World'
        })

    @app.route('/Renters', methods=['GET'])
    @requires_auth(permission='get:Renters')
    def get_Renters(payload):
        try:
            selections = Renters.query.order_by(Renters.id).all()
            paged_Renters = paginate_questions(request, selections)
            total_Renters = len(selections)
            return jsonify({
                'success': True,
                'Renters': paged_Renters,
                'total-Renters': total_Renters
            })
        except Exception:
            abort(422)

    @app.route('/Renters', methods=['POST'])
    @requires_auth(permission='post:Renters')
    def post_Renters(payload):
        add_Renter = request.get_json()
        Renter_name = add_Renter.get('name')
        Renter_gender = add_Renter.get('gender')
        Renter_age = add_Renter.get('age')

        if Renter_name is None:
            abort(422)

        if Renter_gender is None:
            abort(422)

        if Renter_age is None:
            abort(422)

        try:
            new_Renter = Renters(name=Renter_name,
                               gender=Renter_gender,
                               age=Renter_age)
            new_Renter.insert()

            return jsonify({
                "success": True,
                "Renter-added": new_Renter.id
            })

        except Exception:
            abort(422)

    @app.route('/Renters/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:Renters')
    def patch_Renters(payload, id):
        Renter = Renters.query.filter(Renters.id == id).first()
        if not Renter:
            abort(404)

        update_Renter_req = request.get_json()

        if update_Renter_req is None:
            abort(422)

        try:
            if 'name' in update_Renter_req:
                Renter.name = update_Renter_req['name']

            if 'gender' in update_Renter_req:
                Renter.gender = update_Renter_req['gender']

            if 'age' in update_Renter_req:
                Renter.age = update_Renter_req['age']

            Renter.update()

            return jsonify({
                "success": True,
                "Renter-updated": Renter.id
            })

        except Exception:
            abort(422)

    @app.route('/Renters/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:Renters')
    def delete_Renters(payload, id):
        Renter = Renters.query.filter(Renters.id == id).first()
        if not Renter:
            abort(404)
        try:
            Renter.delete()
            return jsonify({
                "success": True,
                "Renter-deleted": Renter.id
            })

        except Exception:
            abort(422)

    @app.route('/Rentals', methods=['GET'])
    @requires_auth(permission='get:Rentals')
    def get_Rentals(payload):
        try:
            selections = Rentals.query.order_by(Rentals.id).all()
            paged_Rentals = paginate_questions(request, selections)
            total_Rentals = len(selections)
            return jsonify({
                'success': True,
                'Rentals': paged_Rentals,
                'total-Rentals': total_Rentals
            })
        except Exception:
            abort(422)

    @app.route('/Rentals', methods=['POST'])
    @requires_auth(permission='post:Rentals')
    def post_Rentals(payload):
        add_Rental = request.get_json()
        Rental_address = add_Rental.get('address')
        Rental_rent = add_Rental.get('rent')

        if Rental_address is None:
            abort(422)

        if Rental_rls_date is None:
            abort(422)

        try:
            new_Rental = Rentals(address=Rental_address,
                               rent=Rental_rent)
            new_Rental.insert()

            return jsonify({
                "success": True,
                "Rental-added": new_Rental.id
            })

        except Exception:
            abort(422)

    @app.route('/Rentals/<int:id>', methods=['PATCH'])
    @requires_auth(permission='patch:Rentals')
    def patch_Rentals(payload, id):
        Rental = Rentals.query.filter(Rentals.id == id).first()

        if not Rental:
            abort(404)

        update_Rental_req = request.get_json()

        if update_Rental_req is None:
            abort(422)

        try:
            if 'address' in update_Rental_req:
                Rental.address = update_Rental_req['address']

            if 'rent' in update_Rental_req:
                Rental.rent = update_Rental_req['rent']

            Rental.update()

            return jsonify({
                "success": True,
                "Rental-updated": Rental.id
            })

        except Exception:
            abort(422)

    @app.route('/Rentals/<int:id>', methods=['DELETE'])
    @requires_auth(permission='delete:Rentals')
    def delete_Rentals(payload, id):
        Rental = Rentals.query.filter(Rentals.id == id).first()

        if not Rental:
            abort(404)
        try:
            Rental.delete()
            return jsonify({
                "success": True,
                "Rental-deleted": Rental.id
            })

        except Exception:
            abort(422)

    @app.errorhandler(400)
    def badRequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def accessForbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Access Denied/Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(405)
    def notAllowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def serverError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify({
            "success": False,
            "error": e.status_code,
            "message": e.error
        }), e.status_code

    return app


app = create_app()

app.app_context().push()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)