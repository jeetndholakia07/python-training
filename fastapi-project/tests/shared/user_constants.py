from app.schemas.user_schema import Role

USER_NAME = "John Doe"
VALID_EMAIL = "john.doe@example.com"
INVALID_EMAIL = "john@"
VALID_PASSWORD = "Password@123"
INVALID_PASSWORD = "mypwd"
PASSWORD_HASH = "password-hash"
ROLE_COMPANY = Role.C
ROLE_EMPLOYEE = Role.E
ROLE_ADMIN = Role.A
USER_GUID = "550e8400-e29b-41d4-a716-446655440099"
INVALID_GUID = "user-guid"
RANDOM_GUID = "00000000-0000-0000-0000-000000000000"
RANDOM_GUID2 = "550e8400-e29b-41d4-a716-44665544000Z"
RANDOM_GUID3 = "not-a-uuid"
VALID_TOKEN = "valid.jwt.token"
INVALID_TOKEN = "invalid.token"