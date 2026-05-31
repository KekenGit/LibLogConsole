# LibLogConsole Four OOP Pillars Study Guide

## Purpose of This Guide

This guide explains how the LibLogConsole project uses the four pillars of object-oriented programming:

1. Abstraction
2. Encapsulation
3. Inheritance
4. Polymorphism

Use this as a reviewer for code explanation, oral defense, reporting, or studying the project structure.

## Quick Project Overview

LibLogConsole is a console-based library visitor log system. It can:

1. Check in visitors.
2. Check out visitors.
3. View current occupancy.
4. Generate a daily report.
5. Display the four OOP pillars used in the code.

The important OOP files are:

| File | Important Classes |
| --- | --- |
| `visitor_record.py` | `Person`, `VisitorRecord` |
| `liblog_function.py` | `LibraryLogSystem` |
| `csv_handler.py` | `StorageBackend`, `CSVStorage` |
| `report_generator.py` | `Report`, `DailyReport` |

## Pillar 1: Abstraction

### Simple Meaning

Abstraction means showing only the important behavior and hiding the detailed implementation.

In simple words:

> The user or another class knows what something can do, but does not need to know every detail of how it does it.

### Where It Appears in the Code

Abstraction appears in:

| Code | Location | Purpose |
| --- | --- | --- |
| `StorageBackend` | `csv_handler.py` | Defines required storage actions. |
| `Report` | `report_generator.py` | Defines required report behavior. |

### Code Idea

`StorageBackend` defines these required methods:

```python
load_data()
save_all(visitors)
append_record(visitor)
```

It does not explain the full CSV process inside the abstract class. It only says that any storage class must provide these actions.

`Report` defines this required method:

```python
build()
```

This means every report class must know how to build report text.

### Why This Is Useful

The system can depend on the idea of storage or reporting without being locked into only one implementation.

For example, today the project uses CSV storage. In the future, it could use database storage if a new class follows the same required methods.

### How to Explain in Defense

> Abstraction is used through abstract base classes like `StorageBackend` and `Report`. These classes define the important actions that storage and report classes must have, while hiding the detailed implementation from the rest of the program.

## Pillar 2: Encapsulation

### Simple Meaning

Encapsulation means keeping data and related methods together inside a class. It also protects the data by controlling how it is accessed or changed.

In simple words:

> The object owns its data, and the program uses methods or properties to work with that data.

### Where It Appears in the Code

Encapsulation appears mainly in:

| Code | Location | Purpose |
| --- | --- | --- |
| `VisitorRecord` | `visitor_record.py` | Stores and controls one visitor transaction. |
| `LibraryLogSystem` | `liblog_function.py` | Manages the visitor list, storage object, and capacity. |

### Code Idea

`VisitorRecord` stores visitor data in private-style attributes such as:

```python
self._name
self._address
self._date
self._time_in
self._time_out
self._duration
```

The program does not directly change these attributes everywhere. It uses properties and methods such as:

```python
visitor.name
visitor.time_in
visitor.check_out()
visitor.to_dict()
```

The `check_out()` method updates `time_out` and `duration` together. This is important because those values should stay connected.

### Why This Is Useful

Encapsulation keeps visitor data organized and prevents the program from randomly changing important values in many places.

For example, instead of manually setting `time_out` and `duration` in different files, the system calls:

```python
visitor.check_out()
```

That method handles the checkout update properly.

### How to Explain in Defense

> Encapsulation is used in `VisitorRecord` because the visitor data is stored inside the object using private-style attributes. The program accesses the data through properties and updates checkout details using the `check_out()` method.

## Pillar 3: Inheritance

### Simple Meaning

Inheritance means one class can receive or reuse features from another class.

In simple words:

> A child class can inherit data or behavior from a parent class.

### Where It Appears in the Code

Inheritance appears in:

| Child Class | Parent Class | Location |
| --- | --- | --- |
| `VisitorRecord` | `Person` | `visitor_record.py` |
| `CSVStorage` | `StorageBackend` | `csv_handler.py` |
| `DailyReport` | `Report` | `report_generator.py` |

### Code Idea

`VisitorRecord` inherits from `Person`:

```python
class VisitorRecord(Person):
```

This means `VisitorRecord` receives common person information such as name and address from `Person`.

`CSVStorage` inherits from `StorageBackend`:

```python
class CSVStorage(StorageBackend):
```

This means `CSVStorage` must follow the storage structure required by `StorageBackend`.

`DailyReport` inherits from `Report`:

```python
class DailyReport(Report):
```

This means `DailyReport` is a specific type of report.

### Why This Is Useful

Inheritance reduces repetition and shows relationships between classes.

For example:

1. A visitor is a type of person.
2. CSV storage is a type of storage backend.
3. A daily report is a type of report.

### How to Explain in Defense

> Inheritance is used when `VisitorRecord` inherits from `Person`, `CSVStorage` inherits from `StorageBackend`, and `DailyReport` inherits from `Report`. This shows parent-child relationships and allows child classes to reuse or follow the structure of parent classes.

## Pillar 4: Polymorphism

### Simple Meaning

Polymorphism means different classes can use the same method name but have their own behavior.

In simple words:

> Same action name, different class implementation.

### Where It Appears in the Code

Polymorphism appears in:

| Parent Method | Implemented By | Location |
| --- | --- | --- |
| `load_data()` | `CSVStorage` | `csv_handler.py` |
| `save_all()` | `CSVStorage` | `csv_handler.py` |
| `append_record()` | `CSVStorage` | `csv_handler.py` |
| `build()` | `DailyReport` | `report_generator.py` |

### Code Idea

The abstract class `Report` requires a `build()` method.

`DailyReport` provides its own version:

```python
def build(self):
```

The abstract class `StorageBackend` requires storage methods.

`CSVStorage` provides CSV-specific versions:

```python
def load_data(self):
def save_all(self, visitors):
def append_record(self, visitor):
```

### Why This Is Useful

The program can work with a general type but still get the correct behavior from the actual class.

Example:

```python
report = DailyReport(get_visitors(), today)
save_report(report, filename)
```

The `save_report()` function calls:

```python
report.build()
```

Because the report object is a `DailyReport`, Python uses the `DailyReport.build()` method.

### How to Explain in Defense

> Polymorphism is used because classes like `CSVStorage` and `DailyReport` implement methods required by their abstract parent classes. The program can call common method names like `build()` or `load_data()`, and the correct class-specific behavior will run.

## How the Four Pillars Work Together

### Check-In Process

1. `Main.py` calls `check_in()`.
2. `check_in()` gathers visitor input.
3. `LibraryLogSystem.check_in_visitor()` creates a `VisitorRecord`.
4. `VisitorRecord` encapsulates the visitor information.
5. `CSVStorage.append_record()` saves the visitor to the CSV file.

OOP pillars used:

| Pillar | Example |
| --- | --- |
| Abstraction | Storage is represented through `StorageBackend`. |
| Encapsulation | Visitor details are stored inside `VisitorRecord`. |
| Inheritance | `VisitorRecord` inherits from `Person`. |
| Polymorphism | `CSVStorage` implements `append_record()` from `StorageBackend`. |

### Report Generation Process

1. `Main.py` calls `generate_report()`.
2. `generate_report()` creates a `DailyReport`.
3. `DailyReport.build()` prepares the report text.
4. `save_report()` saves the report to a text file.

OOP pillars used:

| Pillar | Example |
| --- | --- |
| Abstraction | `Report` requires a `build()` method. |
| Encapsulation | `DailyReport` stores its visitors and report date. |
| Inheritance | `DailyReport` inherits from `Report`. |
| Polymorphism | `save_report()` can call `report.build()`. |

## Short Recitation Script

Use this if you need a quick explanation:

> Our LibLogConsole system demonstrates the four pillars of OOP. Abstraction is shown through abstract classes like `StorageBackend` and `Report`, which define required behavior without showing all implementation details. Encapsulation is shown in `VisitorRecord`, where visitor data is stored inside private-style attributes and accessed through properties and methods. Inheritance is shown when `VisitorRecord` inherits from `Person`, `CSVStorage` inherits from `StorageBackend`, and `DailyReport` inherits from `Report`. Polymorphism is shown because concrete classes like `CSVStorage` and `DailyReport` implement the same required method names from their parent classes, such as `append_record()` and `build()`, with their own specific behavior.

## Common Questions and Answers

### 1. What is the main class that handles the system logic?

`LibraryLogSystem` handles the main system logic. It manages visitor records, capacity, check-in, check-out, and communication with storage.

### 2. What class represents one visitor transaction?

`VisitorRecord` represents one visitor transaction. It stores the visitor's date, name, reason, address, school, signature, time in, time out, and duration.

### 3. Why is `VisitorRecord` an example of encapsulation?

Because it keeps visitor data inside the object and provides methods like `check_out()`, `to_dict()`, and `is_active_on()` to control how the data is used or changed.

### 4. Why is `StorageBackend` an example of abstraction?

Because it defines what storage must do, such as `load_data()`, `save_all()`, and `append_record()`, without depending on the exact storage method.

### 5. How does inheritance appear in the code?

Inheritance appears when:

1. `VisitorRecord` inherits from `Person`.
2. `CSVStorage` inherits from `StorageBackend`.
3. `DailyReport` inherits from `Report`.

### 6. How does polymorphism appear in the code?

Polymorphism appears because child classes implement methods from their parent classes. For example, `DailyReport` has its own `build()` method, and `CSVStorage` has its own `load_data()`, `save_all()`, and `append_record()` methods.

### 7. Why use OOP instead of only functions?

OOP makes the program easier to organize, explain, maintain, and extend. Visitor data belongs in `VisitorRecord`, system actions belong in `LibraryLogSystem`, storage belongs in `CSVStorage`, and reports belong in `DailyReport`.

### 8. If the system used a database in the future, what class could be added?

A new class like `DatabaseStorage` could be added. It would inherit from `StorageBackend` and implement `load_data()`, `save_all()`, and `append_record()` for a database instead of a CSV file.

## Quick Quiz

Answer these to test yourself.

1. What are the four pillars of OOP?
2. What class stores one visitor's transaction?
3. What class does `VisitorRecord` inherit from?
4. What abstract class does `CSVStorage` inherit from?
5. What method does `DailyReport` implement from `Report`?
6. Why is `check_out()` part of encapsulation?
7. What class manages check-in and check-out logic?
8. What pillar allows different classes to use the same method name with different behavior?

## Quick Quiz Answers

1. Abstraction, encapsulation, inheritance, and polymorphism.
2. `VisitorRecord`.
3. `Person`.
4. `StorageBackend`.
5. `build()`.
6. Because it controls how `time_out` and `duration` are updated inside the object.
7. `LibraryLogSystem`.
8. Polymorphism.

## Memory Tips

| Pillar | Easy Memory |
| --- | --- |
| Abstraction | Shows what it does, hides how it works. |
| Encapsulation | Keeps data and methods together inside a class. |
| Inheritance | A child class gets features or structure from a parent class. |
| Polymorphism | Same method name, different behavior depending on the object. |

## Final Key Point

The four pillars are not separate from the program features. They support the actual system:

1. Visitors are represented as objects.
2. The system logic is managed by a class.
3. Storage and reports use abstract parent classes.
4. Concrete classes provide their own behavior while following the same structure.
