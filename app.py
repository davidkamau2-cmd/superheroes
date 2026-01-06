from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import db, Hero, Power, HeroPower
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

@app.route('/')
def index():
    """Welcome page with API documentation"""
    return jsonify({
        "message": "Welcome to Superheroes API!",
        "status": "running",
        "available_endpoints": {
            "heroes": {
                "GET /heroes": "Get all heroes",
                "GET /heroes/:id": "Get specific hero with powers"
            },
            "powers": {
                "GET /powers": "Get all powers",
                "GET /powers/:id": "Get specific power",
                "PATCH /powers/:id": "Update power description"
            },
            "hero_powers": {
                "POST /hero_powers": "Create hero-power association"
            }
        },
        "examples": {
            "get_heroes": "http://127.0.0.1:5555/heroes",
            "get_hero": "http://127.0.0.1:5555/heroes/1",
            "get_powers": "http://127.0.0.1:5555/powers",
            "get_power": "http://127.0.0.1:5555/powers/1"
        },
        "documentation": "See README.md for full API documentation"
    })

def send_hero_power_email(hero_power):
    """Send email notification when a new hero-power association is created"""
    try:
        msg = Message(
            subject=f"New Power Added: {hero_power.hero.super_name}",
            recipients=['admin@superheroes.com'],  # Change this
            body=f"""
            A new power has been assigned!
            
            Hero: {hero_power.hero.name} ({hero_power.hero.super_name})
            Power: {hero_power.power.name}
            Strength: {hero_power.strength}
            Description: {hero_power.power.description}
            
            This is an automated notification from the Superheroes API.
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes])

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict(only=('id', 'name', 'super_name', 'hero_powers')))

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict(only=('id', 'name', 'description')) for power in powers])

@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict(only=('id', 'name', 'description')))

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            power.description = data['description']
        db.session.commit()
        return jsonify(power.to_dict(only=('id', 'name', 'description')))
    except (ValueError, AssertionError) as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        hero_power = HeroPower(
            strength=data.get('strength'),
            power_id=data.get('power_id'),
            hero_id=data.get('hero_id')
        )
        db.session.add(hero_power)
        db.session.commit()
        
         # Send email notification
        send_hero_power_email(hero_power)
        
        return jsonify(hero_power.to_dict(only=('id', 'hero_id', 'power_id', 'strength', 'hero', 'power'))), 201
    except (ValueError, AssertionError) as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5555)