Add comprehensive pytest suite for Swagger Petstore Pet API endpoints

- Implemented end-to-end tests covering CRUD operations on /pet endpoint:
  - Created pets with randomized data using pytest fixtures for uniqueness
  - Retrieved pets by ID to verify creation and updates
  - Updated pet status and validated changes persist correctly
  - Deleted pets to clean up after tests ensuring no leftover data

- Added extensive negative testing scenarios:
  - Verified 404 responses for invalid and non-existent pet IDs on GET requests
  - Tested API behavior with missing required fields on pet creation
  - Ensured the API gracefully handles invalid inputs with appropriate status codes

- Covered search and filtering capabilities:
  - Tested listing pets by various statuses (available, pending, sold) using parameterized tests
  - Asserted that all returned pets have the requested status

- Explored edge cases for robustness:
  - Created pets with extremely long names to test API handling of large input strings
  - Used special characters in pet names to confirm input sanitization and proper storage

- Utilized pytest fixtures for setup and teardown, providing clean test environment isolation
- Used the requests library for efficient and reliable HTTP calls with JSON payloads
- Applied strong assertions on HTTP status codes and response JSON structure/content for test reliability
- Designed tests to be modular, readable, and easily extensible for future Petstore API endpoint coverage
