# APIOverflow
a super cool api hub :)

# Installation Instructions

Before running the application, ensure that Docker is installed and running on your machine. Then, navigate to the project directory APIOverflow where docker-compose.yml is located. Ensure that the Docker images are built and ran without using cache to ensure latest code and dependencies by running the following command in the terminal:

```
docker compose build --no-cache; docker compose up
```
Finally, to access the application, open your web browser and navigate to http://localhost:3000.

Additionally, we provide the option to run backend tests via pytest using the docker environment. To run these tests, run the following command in the terminal:
```
docker compose build --build-arg TEST=t; docker compose up
```

Our system currently supports a single superadmin user who by default has all permissions enabled. Initially, this is the only user with the permissions to approve or disapprove new services / pending service updates. The default provided login details for this
user are:

username: superadmin \
password: superadminpassword

We have provided some example yaml (to demonstrate swagger implementation) and pdf files in the /files folder to help you test our work.

# Key Feature Summary

See Report for more details

## Authentication and User Management
- Multi-tier user systerm (Guest, Registered User, Admin, Superadmin)
- Email-based verification system
- Secure password reset functionality
- Profile management with customisable icons

## API Service Management
- Structured API upload system supporting name, description, and tags
- Swagger/OpenAPI specification integration
- Version control
- Documentation 

## Search and Discovery
- Comprehensive search functionality with filters
- Tag-based categorisation
- Ranked tag system for improved discoverability

## Review and rating system
- Upvoting/downvoting mechanism
- Owner response capability
- Comment management

## User management (promote/demote/delete)
- Service approval workflow
- Content moderation capabilities
- Maps to requirements that “Administrator user should have full privilege”

