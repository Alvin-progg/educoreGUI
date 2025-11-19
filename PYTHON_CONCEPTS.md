# Python Concepts in EduCore

| Function/Definition | Purpose | Context in EduCore |
|---|---|---|
| **Relationship (ORM)** | Defines associations between database tables. | Links `Student` to `Course` and `Grade` models. |
| **Decorator** | Modifies the behavior of a function. | Used for API routing (`@app.get`) and data validation (`@validator`). |
| **Type Hints** | Annotates variables and parameters with expected types. | Used in all function signatures and Pydantic models for clarity and validation. |
| **Dependency Injection** | Provides dependencies (e.g., a database session) to a function externally. | FastAPI's `Depends(get_db)` supplies a database session to API endpoints. |
| **Context Manager** | Manages resource setup and cleanup. | Used implicitly by `Depends(get_db)` to handle the database session lifecycle. |
| **Foreign Key** | A database constraint that establishes a relationship between tables. | `course_code` in the `Student` model links to the `Course` model. |
| **Cascade Operations** | Automatically propagates operations (e.g., delete) to related entities. | Deleting a `Student` also deletes their associated `Grade` records. |
| **Unique Constraint** | A database constraint that ensures all values in a column are unique. | Ensures `student_code` is unique and prevents duplicate student-subject entries. |
| **Data Validation** | Ensures data integrity and correctness. | Pydantic schemas validate API inputs, such as ensuring a grade is between 1.0 and 5.0. |
| **Pydantic `BaseModel`** | A class for data validation, serialization, and documentation. | All schemas inherit from `BaseModel` to define the API data structure. |
| **Async Event Handler** | An asynchronous function that runs on a specific event, like startup. | The `@app.on_event("startup")` decorator is used to initialize database content. |
| **Exception Handling** | Manages errors to prevent application crashes. | `HTTPException` is used for API errors; `try-except` blocks handle request failures in the GUI. |
| **List Comprehension** | A concise way to create lists. | Used to build response lists for API endpoints. |
| **Dictionary** | A key-value data structure. | Used for GUI color configuration and API response bodies. |
| **Threading** | Allows for concurrent or background execution of code. | Used in the GUI to run QR code scanning in a background thread to avoid freezing the UI. |
| **Query Building (ORM)** | Constructs database queries using object-oriented syntax instead of raw SQL. | Used to fetch, filter, and order records (e.g., `db.query(Student).filter(...).first()`). |
| **Aggregation Functions** | Performs a calculation on a set of values and returns a single value. | Used to calculate average GWA (`func.avg`) and count total students (`func.count`). |
| **Default Values** | Sets a default value for a parameter or attribute. | A student's `gwa` defaults to `0.0` upon creation. |
| **Optional Types** | A type hint for values that can be `None`. | Used for nullable fields like `created_at` and `updated_at`. |
| **Server-side Defaults** | Sets a default value at the database level. | `created_at` is automatically set to the current timestamp by the database server. |
| **CRUD Operations** | The four basic functions of persistent storage: Create, Read, Update, Delete. | Implemented as RESTful API endpoints for managing students, grades, and courses. |
| **RESTful API Endpoints** | Maps HTTP methods (GET, POST, PUT, DELETE) to CRUD operations. | Used in `main.py` to define the API for the frontend to consume. |
| **Middleware** | A processing layer that intercepts and modifies requests and responses. | `CORSMiddleware` is used to allow cross-origin requests from the GUI. |
| **Event Binding** | Connects GUI events (like a key press) to handler functions. | Binds the "Enter" key to a function to trigger an action, like loading subjects. |
| **Password Hashing** | Encrypts passwords for secure storage. | `bcrypt` is used to hash user passwords before saving them to the database. |
| **Authentication** | A system for validating user login credentials. | The `/api/auth/login` endpoint and `LoginWindow` class manage user authentication. |
| **Modal Window** | A separate window that appears for a specific task. | The `LoginWindow` is a modal dialog that requires user interaction before the main app is accessible. |
| **QR Code Generation** | Creates a QR code image from data. | The `qrcode` library is used to generate a unique QR code for each student's ID. |
| **Camera Access** | Opens and reads from a webcam. | `OpenCV` is used to capture video frames for QR code scanning. |
| **QR Code Decoding** | Reads and extracts data from a QR code. | `pyzbar` is used to decode QR codes from the camera feed. |
| **Image Processing** | Manipulates images and video frames. | `OpenCV` and `Pillow` are used to process frames and resize images. |
| **File I/O** | Reads from and writes to files. | Used to save generated QR codes as PNG image files. |
| **Window Destruction** | Closes and removes a GUI window. | The login window is destroyed after a successful login. |
| **Boolean State** | A flag used to track the state of the application. | A `login_successful` flag tracks whether the user has been authenticated. |
| **Password Visibility Toggle** | A feature to show or hide a password in an input field. | A checkbox in the login window controls whether the password is shown as text or dots. |

