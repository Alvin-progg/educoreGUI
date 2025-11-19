# OOP Concepts in EduCore

| Function/Definition | Purpose | Context in EduCore |
|---|---|---|
| **Class** | Blueprint for creating objects with attributes and methods. | Used for models (`Student`, `User`), schemas (`StudentCreate`), and GUI components (`EduCoreApp`, `ModernButton`). |
| **Inheritance** | A class derives properties/methods from a parent class. | Models inherit from `Base`, schemas from `BaseModel`, and GUI widgets from `ctk.CTkButton`. |
| **Encapsulation** | Bundling data and methods within a class, controlling access. | `APIClient` encapsulates HTTP logic; models encapsulate data attributes. |
| **Polymorphism** | Different classes can be used through the same interface. | Custom widgets like `ModernButton` override parent methods; schemas share the `BaseModel` interface. |
| **Method** | A function defined inside a class. | Used for API endpoints (`add_student`), GUI actions (`refresh_students`), and data validation (`validate_grade`). |
| **Constructor (`__init__`)** | Special method to initialize an object's state. | Initializes `EduCoreApp` and `APIClient`. |
| **Property/Attribute** | Class variables that store state. | Defines model fields like `student_code`, `name`, and `gwa`. |
| **String Representation (`__repr__`)** | Defines how an object is represented as a string for debugging. | Used in all model classes for clear logging. |
| **Class Configuration** | A nested class for Pydantic/SQLAlchemy settings. | `Config` class in response schemas enables ORM mode. |
| **`super()` Function** | Calls a method from a parent class. | Used in custom GUI widgets to initialize the parent component. |
| **GUI Widget Inheritance** | Creating custom widgets by extending a GUI library's components. | `ModernButton` extends `ctk.CTkButton` to create a custom look and feel. |

