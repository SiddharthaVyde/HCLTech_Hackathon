**MODULAR BANKING BACKEND SYSTEM**

**Project Overview:**
A scalable banking backend system built with modular architecture

The system is divided into individual modules, each performing a different set of tasks

1. User Registration & KYC:

- Creating a pydantic object for the different features required.
- Created separate APIs for Sign up, uploading documents, Validating and these files can be integrated with a database.
- We create a new entry in the existing database and the status will be "PENDING", the status will be updated after verification.
- Fastapi is used for achieving this task.

2. Account Creation

- Responsible for creating new bank accounts through a REST API built with FastAPI and SQLAlchemy.
- Built with FastAPI, SQLAlchemy, SQLite, and Pydantic for request/response validation.
- Validates minimum initial deposit per account type (Savings, Current, Salary).
- Auto-generates globally unique account numbers using Python’s uuid module, Stores and retrieves account data via ORM models with clean REST endpoints.

4. Loan Application & EMI Calculation:

- Customer will give details of the loan that he want, if approved, the system calculates the EMI based on the interest rate for the loan type.
- Build using FastAPI and can be tested through Swagger UI.
  
5. Fraud Detection:

- Extract key features from dataset which contains details of the customers(Ex: account type, balance, transaction amount etc.)
- Isolation Forest: Method is used to find the outliers(Fraud transactions) by splitting into trees. It is an unsupervised learning
- One-class SVM: An unsupervised learning algorithm that finds boundary for the normal transactions, data points falling outside that region are considered as outliers.
- Implemented preprocessing, encoding, and anomaly detection on transaction data using scikit-learn pipelines for real-time scoring.
- API endpoints were built with FastAPI to receive transaction data, process it through the pipeline, and return fraud predictions instantly.
