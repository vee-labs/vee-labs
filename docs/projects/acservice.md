# ACServiceApp

> Field service ticketing system for AC technicians — native Android.

ACServiceApp is a mobile app for managing air-conditioning service jobs. Technicians can create tickets, update status, add comments, and close jobs. All data syncs in real time via Firebase Firestore.

## Features

- **Ticket management** — create, view, update, and close service tickets
- **Real-time sync** — Firestore keeps all devices up to date instantly
- **Authentication** — Firebase Email/Password auth with session management
- **Comments** — technicians and admins can thread comments on each ticket
- **Role-aware UI** — different views for technicians vs. admin users

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Kotlin |
| Platform | Android (native) |
| Architecture | MVVM (ViewModel + Repository) |
| Database | Firebase Firestore |
| Auth | Firebase Authentication |
| Navigation | Jetpack Navigation Component |
| Build | Gradle (Kotlin DSL) |

## Architecture

```
app/src/main/java/com/acservice/app/
├── MainActivity.kt
├── data/
│   ├── model/
│   │   ├── Ticket.kt
│   │   ├── Comment.kt
│   │   └── User.kt
│   └── repository/
│       ├── AuthRepository.kt
│       └── TicketRepository.kt
├── ui/
│   ├── auth/
│   │   ├── LoginActivity.kt
│   │   └── LoginViewModel.kt
│   └── tickets/
│       ├── TicketListFragment.kt
│       ├── TicketDetailFragment.kt
│       ├── CreateTicketFragment.kt
│       └── (ViewModels)
└── utils/
    ├── SessionManager.kt
    └── Extensions.kt
```

## Firestore Data Model

```
/tickets/{ticketId}
  - title, description, status
  - assignedTo, createdBy
  - createdAt, updatedAt

/tickets/{ticketId}/comments/{commentId}
  - text, authorId, createdAt

/users/{uid}
  - name, email, role
```

## Security Rules

Firestore rules enforce:
- Authenticated users only
- Users can only write their own profile
- Tickets readable by all authenticated users
- Comments writable only by the author

## Setup

```bash
# 1. Create Firebase project at console.firebase.google.com
# 2. Enable Email/Password Authentication
# 3. Create Firestore database (production mode)
# 4. Download google-services.json → app/

# Build and run
./gradlew assembleDebug
```

## Status

Active development. Internal use / private beta.

→ [Back to Projects](/projects/)
