# Django Password Manager

## Description
Django Password Manager is a locally-run application designed to manage users' passwords encrypted on their machines. Users also have the option to synchronize data with their MongoDB Atlas database, allowing data synchronization across different devices.

## Features
- Locally manage encrypted passwords
- Synchronization with MongoDB Atlas for cross-device data access

## Installation
To install and run the application, execute the appropriate script for your system:
- For Linux/Mac: `./run.sh`
- For Windows: `./run.bat`

### Dependencies
Ensure that Python 3.12 is installed on your system.

## Configuration
If synchronization is desired, follow these steps:
1. Create an account on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Fill in the required variables in the `.env.example` file.
3. Rename the `.env.example` file to `.env`.

## Usage
Navigate to [localhost:8000](http://localhost:8000) in your web browser to access the application.

## Screenshots or Demo


## License
This project is released under the Apache License Version 2.0.
