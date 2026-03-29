# Software Requirements Specification (SRS)

## Spotter - Fitness Training Platform

**Version:** 1.0  
**Date:** February 2026  
**Status:** Release

---

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements for Spotter, a web-based platform that facilitates connections between fitness trainers and clients. The platform enables clients to post fitness requests and allows trainers to bid on those requests, establish training relationships, and deliver personalized fitness and nutrition plans.

### 1.2 Scope

Spotter is a Django-based web application that manages the entire lifecycle of trainer-client relationships, from initial connection to plan execution. The system includes user authentication, trainer portfolio management, client request posting, proposal system, and comprehensive training plan management with daily exercises and meal plans.

**Out of Scope:**

- Payment processing integration
- Video hosting (external links only)
- Real-time chat functionality
- Mobile native applications

### 1.3 Definitions, Acronyms, and Abbreviations

- **Client** - A user seeking fitness training services
- **Trainer** - A fitness professional offering training and nutrition services
- **Card** - A client's fitness request/service inquiry posted on the platform
- **Response** - A trainer's proposal to fulfill a client's card request
- **Plan** - A detailed fitness and nutrition program created from an accepted response
- **Daily Plan** - A daily breakdown of exercises and meals within a plan
- **Portfolio** - A trainer's professional profile showcasing credentials and experience
- **SRS** - Software Requirements Specification
- **FK** - Foreign Key (database relationship)
- **Pitch** - A trainer's proposal text describing their solution

### 1.4 References

- IEEE 830-1998 Standard for Software Requirements Specifications
- Django Framework Documentation (v6.0.1)
- Django Authentication Framework Documentation

### 1.5 Overview

The remainder of this SRS is organized as follows:

- Section 2 provides an overall description of the product and its environment
- Section 3 contains detailed specifications of system functionality, interfaces, and quality requirements

---

## 2. Overall Description

### 2.1 Product Perspective

Spotter is a standalone web application built with Django that serves as an intermediary platform between fitness trainers and clients. The system is independent but interacts with:

- Django's built-in authentication system
- Database (SQLite for development)
- Web browser interface for user interaction
- External video hosting services (trainer-provided URLs)

### 2.2 Product Functions

1. **User Management**
   - User registration and authentication
   - Role-based access control (Client/Trainer)
   - User profile management

2. **Trainer Portfolio Management**
   - Create and maintain professional portfolios
   - Display profession, bio, experience, and education

3. **Client Card Management**
   - Post fitness service requests (cards)
   - Track card status (Available, Pending, Closed)
   - View responses from trainers

4. **Response System**
   - Allow trainers to respond to client cards with proposals
   - Display trainer pitch, pricing, and proposed duration
   - Manage response status (Pending, Accepted, Declined)

5. **Training Plan Management**
   - Create detailed plans from accepted responses
   - Define overall plan description, duration, and active status
   - Track client-trainer relationships through plans

6. **Daily Plan & Exercise Management**
   - Break down plans into daily schedules
   - Specify exercises with sets, reps, descriptions, and video links
   - Attach meals to daily plans

7. **Comments & Progress Tracking**
   - Enable progress comments on plans for feedback and collaboration

### 2.3 User Characteristics

- **Clients:** Fitness enthusiasts seeking professional guidance, varying levels of fitness knowledge
- **Trainers:** Fitness professionals with expertise in training and nutrition
- **All Users:** Basic to intermediate computer literacy, ability to navigate web interfaces

### 2.4 Constraints

1. **Technology Constraints:**
   - Built with Django 6.0.1
   - Runs on Python-based environment
   - Requires browser support for HTML5

2. **Data Constraints:**
   - All dates and times managed through Django's timezone utilities
   - Video content stored externally (linked via URLs)

3. **Operational Constraints:**
   - Single-database deployment model
   - Web-based access only (no native mobile apps)

### 2.5 Assumptions and Dependencies

1. **Assumptions:**
   - Users have valid email addresses for registration
   - Trainers provide accurate professional information
   - Clients have realistic fitness goals
   - Network connectivity is available for platform access

2. **Dependencies:**
   - Django 6.0.1 and related packages (asgiref, sqlparse, tzdata)
   - Database backend (SQLite for development, production TBD)
   - Web server (development or production configuration)

---

## 3. Specific Requirements

### 3.1 External Interfaces

#### 3.1.1 User Interfaces

- **Registration Page:** Login/registration forms with role selection
- **Dashboard:** Home page with navigation based on user role
- **Client Interface:** View cards, track responses, manage plans
- **Trainer Interface:** View available cards, manage portfolio, create responses
- **Plan Management Interface:** Create, edit, and view training plans

#### 3.1.2 Hardware Interfaces

- Standard web server hardware supporting Django deployment

#### 3.1.3 Software Interfaces

- **Database:** SQLite (development), compatible with PostgreSQL/MySQL (production)
- **Authentication:** Django's built-in User authentication system
- **Web Framework:** Django 6.0.1 with standard ORM

### 3.2 Functions

#### 3.2.1 User Registration & Authentication

- **Requirement:** System shall allow new users to register with email and password
- **Requirement:** System shall authenticate users and maintain session management
- **Requirement:** Users shall select role (Client/Trainer) during registration

#### 3.2.2 Portfolio Management

- **Requirement:** Trainers shall create a unique portfolio (1:1 relationship with trainer user)
- **Requirement:** Portfolio shall include: profession, bio, experience, education, profile image, and last_update timestamp
- **Requirement:** Trainers shall be able to upload and update their profile picture
- **Requirement:** Trainers shall be able to update portfolio information

#### 3.2.3 Card Management

- **Requirement:** Clients shall create cards describing fitness problems and goals
- **Requirement:** Clients shall view their own cards with status tracking
- **Requirement:** Card status shall be: Available, Pending (responses received), or Closed
- **Requirement:** Cards shall be searchable by trainers

#### 3.2.4 Response System

- **Requirement:** Trainers shall submit responses to available cards
- **Requirement:** Responses shall include: pitch, price_per_day, duration_days, and status
- **Requirement:** Response status shall be: Pending, Accepted, or Declined
- **Requirement:** Clients shall accept or decline trainer responses

#### 3.2.5 Plan Creation & Management

- **Requirement:** Upon accepting a response, a plan shall be created automatically
- **Requirement:** Plans shall link client, trainer, and response
- **Requirement:** Plans shall include: description, duration_days, created_at, and isActive status
- **Requirement:** Trainers shall create daily plans within plans
- **Requirement:** Plans shall be marked as inactive upon completion

#### 3.2.6 Daily Plans & Exercises

- **Requirement:** Trainers shall create daily plans for each day of the training program
- **Requirement:** Daily plans shall contain exercises and meal information
- **Requirement:** Exercises shall include: name, description, video_url, sets, reps
- **Requirement:** Meals shall be associated with daily plans

#### 3.2.7 Progress Tracking

- **Requirement:** Users shall comment on plans for progress and feedback updates
- **Requirement:** Comments shall be timestamped and associated with specific plans

### 3.3 Performance Requirements

- **Response Time:** System shall respond to user requests within 2 seconds under normal load
- **Concurrent Users:** System shall support a minimum of 50 concurrent users
- **Database Query Time:** Database queries shall complete within 500ms
- **File Upload:** Video links shall be validated and stored without timeout (external hosting)

### 3.4 Logical Database Requirements

#### 3.4.1 Data Entities

1. **User** - Extended Django User model with role field
2. **Portfolio** - Trainer professional profile (1:1 with Trainer User)
3. **Card** - Client fitness requests (1:N with Client User)
4. **Response** - Trainer proposals (N:1 with Card, N:1 with Trainer)
5. **Plan** - Training programs (1:1 with Response, 1:N with Client, 1:N with Trainer)
6. **DailyPlan** - Daily breakdown (1:N with Plan)
7. **Exercise** - Exercise details (1:N with DailyPlan)
8. **Meal** - Meal information (1:N with DailyPlan)
9. **ProgressComment** - Feedback messages (N:1 with Plan)

#### 3.4.2 Data Flow

```
User (Client) → Card → Response (from Trainer) → Plan → DailyPlan → Exercise/Meal
                                                   ↓
                                            ProgressComment
```

### 3.5 Design Constraints

1. **Architecture:** Must use Django MTV (Model-Template-View) architecture
2. **Database:** Must maintain referential integrity using foreign keys
3. **Code Standards:** Follow PEP 8 Python style guidelines
4. **ORM:** Must use Django ORM, no raw SQL queries where possible
5. **Authentication:** Must use Django's authentication system with permission decorators

### 3.6 Software Quality Attributes

#### 3.6.1 Reliability

- System shall maintain data consistency across all transactions
- Failed requests shall not corrupt database state

#### 3.6.2 Availability

- System shall be available 99% of scheduled operating time
- Scheduled maintenance windows may be scheduled with notice

#### 3.6.3 Usability

- Interface shall be intuitive for users with basic computer skills
- All forms shall provide clear validation messages
- Navigation shall be consistent across all pages

#### 3.6.4 Maintainability

- Code shall be documented with docstrings
- Functions shall have single, clear responsibilities
- Database migrations shall be tracked and versioned

#### 3.6.5 Security

- Passwords shall be hashed using Django's default hashing algorithm
- User authentication shall be required for sensitive operations
- Cross-site request forgery (CSRF) protection shall be enabled
- SQL injection protection shall be enforced through ORM usage

#### 3.6.6 Testability

- Each module shall include unit tests
- Critical paths shall have integration tests

---

## Appendix A: Data Model Relationships

```
User (Extended Django User)
├── role: CLIENT | TRAINER
├── Portfolio (if Trainer) [1:1]
│   ├── profession
│   ├── bio
│   ├── experience
│   ├── education
│   └── profile_image_url
├── Card (if Client) [1:N]
│   ├── status: AVAILABLE | PENDING | CLOSED
│   ├── problem
│   └── goal
├── Response (if Trainer) [1:N]
│   ├── pitch
│   ├── status: PENDING | ACCEPTED | DECLINED
│   ├── price_per_day
│   ├── duration_days
│   └── planIsCreated
└── Plan [1:N]
    ├── Client FK
    ├── Trainer FK
    ├── Response FK (1:1)
    ├── description
    ├── duration
    ├── isActive
    └── DailyPlan [1:N]
        ├── description
        └── Exercise [1:N]
            ├── name
            ├── description
            ├── video_url
            ├── sets
            └── reps
        └── Meal [1:N]
            ├── details
```

---

**Document Change History:**

| Version | Date          | Author           | Description                        |
| ------- | ------------- | ---------------- | ---------------------------------- |
| 0.1     | January 2026  | Development Team | Initial SRS Document Creation      |
| 1.0     | February 2026 | Development Team | Complete revamp of documentation   |
| 1.1     | February 2026 | Development Team | Added profile picture to portfolio |
