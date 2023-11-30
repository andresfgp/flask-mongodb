# Flask and MongoDB CRUD API

A simple CRUD API built with Flask and MongoDB for managing contacts.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/andresfgp/flask-mongodb.git
    cd flask-mongodb
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up MongoDB:**

   - Create a MongoDB Atlas account and configure your cluster.
   - Update the `MONGO_URI` in `app.py` with your MongoDB connection string.

## Usage

1. **Run the Flask application:**

    ```bash
    python app.py
    ```

2. The API will be available at `http://127.0.0.1:5000/`.

## API Endpoints

- **Create a contact:**

    ```
    POST /contact
    Body: {"name": "Andres Garcia", "email": "andres.garcia@gmail.com"}
    ```

- **Read all contacts:**

    ```
    GET /contact
    ```

- **Read one contact:**

    ```
    GET /contact/<id>
    ```

- **Update a contact (Replace):**

    ```
    PUT /contact/<id>
    Body: {"name": "Updated Name", "email": "updated.email@example.com"}
    ```

- **Partially update a contact (PATCH):**

    ```
    PATCH /contact/<id>
    Body: {"name": "Updated Name"}
    ```

- **Delete a contact:**

    ```
    DELETE /contact/<id>
    ```

## Dependencies

- Flask==2.1.1
- Flask-PyMongo==2.3.0
- pymongo[srv]

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Push to your fork and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
