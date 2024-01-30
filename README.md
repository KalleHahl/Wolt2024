# Pre assignment for Wolt Summer 2024 Engineering Internship, Backend (Python)

## Description:

#### HTTP API for calculating an order's delivery fee

I took this pre assignment as an opportunity to challenge myself and tried to create as clean, readable, typed and well tested code as possible. Even though the assigned project was small in scale, I decided to go for a directory structure and divided different functionalities such as pydantic models and the class where the delivery fee calculation happens into separate folders, instead of a single file approach.

#### Technologies:

- Poetry for dependency management
- The API is built using FastAPI and Uvicorn
- Pydantic is used in validating the incoming request
- Unit tests are run with Pytest using Pythons unittest module
- FastAPIs TestClient is used in testing the endpoint
- Coverage is used for checking test coverage
- Mypy for static type checking (inspired by [this](https://www.youtube.com/watch?v=cCmAfJeiZ34) video from Wolt Tech Talks youtube channel)
- Code is formatted using Black
- Necessary commands use invokes

## Installing / Getting started

> NOTE: If you don't have poetry installed on you system, follow the instructions provided at [python-poetry.org/docs](https://python-poetry.org/docs/#installation)

_Run these commands in the projects root directory_

Install dependencies

```bash
poetry install
```

Enter poetrys virtual environment

```bash
poetry shell
```

Start the server

```bash
invoke start
```

Connection can be checked by visiting [127.0.0.1:8000](http://127.0.0.1:8000/)

Make the POST requests to http://127.0.0.1:8000/api/calculate_delivery_fee

Successfull requests are responded to with code 200

If the request body or its fields are invalid, the request is responded to with error code 422 with a response body with further details

## Command-line:

_Enter poetrys virtual environment with `poetry shell` before running these_

Tests are run with

```bash
invoke test
```

Coverage report

```bash
invoke coverage-report
```

Check for formatting errors

```bash
invoke black-check
```

Type check

```bash
invoke mypy
```
