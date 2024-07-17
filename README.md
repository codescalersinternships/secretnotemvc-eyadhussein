# Secret Note MVC

## Project Description
This is a web application that allows users to securely share self-destructing secret notes. It is built with Django and utlizes sqlite.

## Features
- **Note Creation**: Users can create new notes with titles, content, expiration dates, and view limits.
- **Authentication**: User registration, login, and logout functionalities are implemented.
- **Note Listing**: Users can view a list of their created notes.
- **Note Detail**: Detailed view of each note, with automatic expiration and view limits.
- **Rate Limiting**: Protects against excessive requests using IP-based rate limiting.
- **Deployment**: Docker configuration for easy deployment.

## How To Install

Clone the repository:
```bash
git clone git@github.com:codescalersinternships/secretnotemvc-eyadhussein.git
cd secretnotemvc-eyadhussein
```

## How To Run

### Run without docker
1. Create a virtual environment and activate it:
```bash
make create-virtualenv
make activate-virtualenv
```

2. Install dependencies:
```bash
make install-requirements
```

3. Apply migrations:
```bash
make migrate
```

4. Run app:
```bash
make runserver
```

### Run using docker
1. Build docker image:
```bash
make docker-build
```
2. Run image:
```bash
make docker-run
```

The app will be running on port 8000


## How to Test
```bash
make test
```


