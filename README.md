Superheroes API Code challenge.

A Flask API for managing superheroes and their powers.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

3. Seed the database:
```bash
python seed.py
```

4. Run the application:
```bash
python app.py
```


## API Endpoints

### GET /heroes
Returns a list of all heroes.

### GET /heroes/:id
Returns a specific hero with their powers.

### GET /powers
Returns a list of all powers.

### GET /powers/:id
Returns a specific power.

### PATCH /powers/:id
Updates a power's description.

### POST /hero_powers
Creates a new hero-power association.