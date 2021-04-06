# TODO

This document describes the various additional work to either make this service production-ready or further enhance its maintainability. They are listed in priority order.

1. Logging, particularly debug-level logs for the state of variables during the transformation stage
2. Metrics, especially data record counters during the extract and load phases and timers for the entire job and each ETL phase
3. Input validation, especially for the methods which first touch the extracted data
4. Improved error handling, such as in cases where methods are called with invalid input and to allow for partial errors as business needs require (as currently a single bad data point fails the entire job)
5. Additional automated testing, especially negative test cases for invalid method parameters
6. Improved separation of concerns between each phase of the ETL
7. Smaller area of responsibility within select methods for improved testability
8. Increasing configurability of the service so that critical business logic is not buried within application code and future business requirement changes are easier to address
