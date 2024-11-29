# Models Library

**Models Library** is a Python library that provides shared Pydantic models for use across multiple services in your application. This library simplifies data validation and ensures consistency by centralizing the schemas for data objects like users, tests, and questions.

## Features

- Shared Pydantic models for:
  - **Users**: User schemas and roles.
  - **Tests**: Test creation, questions, and answers.
- Ensures consistent data validation across services.
- Lightweight and easy to integrate into your projects.

## Installation

### Using `pip`
You can install the library locally by cloning this repository and running:

```bash
pip install .
```

Or install it directly from your repository if hosted on GitHub:

```bash
pip install git+https://github.com/nataliagwardjan/interview_prep_models_library.git
```

### Dependencies
The library requires Python 3.10 or newer. All dependencies are listed in `requirements.txt`.

To install dependencies manually:

```bash
pip install -r requirements.txt
```

## Usage

### Importing Models
The library provides easy-to-use models for users, tests, and questions:

```python
from interview_prep_models_library import UserSchema, Role, TestCreateSchema, QuestioType, Level

# Example usage
user = UserSchema(
    id="123e4567-e89b-12d3-a456-426614174000",
    first_name="John",
    surname="Smith",
    email="john.smith@example.com",
    roles=[Role.REGULAR]
)

test = TestCreateSchema(
    user_id="123e4567-e89b-12d3-a456-426614174000",
    position="Software Developer",
    level=Level.JUNIOR,  
    number_of_question=25,  
    type_of_question=[QuestionType.TRUE_FALSE, QuestionType.SINGLE_CHOICE],
    skills_or_tools=["Python", "Algorithms"]  
)
```

### Docker
This library includes a `Dockerfile` to simplify deployment. Build and run the Docker container:

#### Build the Image
```bash
docker build -t interview_prep_models-library .
```

#### Run the Container
```bash
docker run -v $(pwd):/app -it interview_prep_models-library
```

## Development

### Setting Up the Virtual Environment
1. Create a virtual environment:
   ```bash
   python -m venv venv
    ```

2. Activate the environment:
   - **Linux/Mac**: 
     ```bash
     source venv/bin/activate
     ```
   - **Windows**: 
     ```bash
     venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests
To ensure your changes work as expected, write and run unit tests.

```bash
python -m unittest discover -s tests -p "*.py"
```

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

### Finalna Struktura Projektu:

```plaintext
interview_prep_models_library/
├── models/
│   ├── __init__.py
│   ├── users.py
│   └── tests.py
├── tests/
│   ├── user_tests.py
│   └── test_tests.py
├── __init__.py
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
└── setup.py
```