---
description: Field service ticketing system for AC technicians — native Android.
updated: 2026-05-17
---

# ACServiceApp

> Field service ticketing system for AC technicians — native Android.

ACServiceApp manages air-conditioning service jobs end-to-end. Admins create and assign tickets; technicians update status and log spare parts; office staff and admin track finances. All data syncs in real time via Firebase Firestore.

## What It Does

- **Ticket lifecycle** — NEW → ASSIGNED → IN_PROGRESS → COMPLETED, with soft-delete (30-day recycle bin + auto-purge)
- **Role-based access** — Admin, Office Staff, Technician — each role sees a different UI and has different Firestore permissions
- **Spare parts & payments** — technicians log spare parts and advance payments per ticket; amounts accumulate (never overwrite)
- **Finance screen** — monthly summary (calls, revenue, spare, petrol, labour) with per-tech breakdown and CSV export
- **Activity log** — full audit trail of status changes and actions
- **Real-time sync** — Firestore live listeners; admin ticket list refreshes on every server push

## Stack

| Layer | Technology |
| --- | --- |
| Language | Kotlin |
| Platform | Android (native, minSdk 26) |
| Architecture | MVVM — ViewModel + Repository |
| Database | Firebase Firestore (real-time listeners) |
| Auth | Firebase Authentication (username/password, no email) |
| Local DB | Room (ActivityLog, LocalUser, TicketStatus) |
| Cache | AppCache — spare parts pre-loaded at login |
| Build | Gradle Kotlin DSL, AGP 8.7, Kotlin 2.1, Gradle 8.11.1 |

## Architecture

```text
app/src/main/java/com/acservice/app/
├── App.kt                        # Seed + cache prime on startup (admin only)
├── MainActivity.kt
├── data/
│   ├── auth/FirebaseAuthBridge.kt
│   ├── cache/AppCache.kt         # In-memory spare parts cache
│   ├── firestore/                # Ticket, Spare, Comment, Rating, History repos
│   ├── local/                    # Room: ActivityLog, LocalUser
│   ├── model/Models.kt
│   └── remote/UserRepository.kt
└── ui/
    ├── admin/                    # AdminDashboard, ActivityLog, TicketList (admin)
    ├── auth/                     # Login
    ├── finance/                  # FinanceActivity — monthly summary + CSV
    ├── technician/               # TechnicianDetail monthly table
    └── tickets/                  # TicketList, TicketDetail, CreateTicket, ModifyTicket
```

## Firestore Data Model

```text
/users/{uid}
  - username (lowercase), role, displayName

/tickets/{ticketId}
  - status, technicianUsername, createdBy
  - labourCharge, advanceAmount, advanceHistory[], paymentHistory[]
  - pendingSpares[], isDeleted, deletedAt, purgeAfter
  - lastServerUpdateAt

/tickets/{ticketId}/comments/{commentId}
  - text, authorUsername, createdAt

/spareParts/{id}
  - name, price, stock
```

## Key Files

| File | Purpose |
| --- | --- |
| `TicketRepository.kt` | All Firestore ticket queries, live listeners, soft-delete, CSV export |
| `TicketListViewModel.kt` | Role-filtered queries, real-time update tracking |
| `ModifyTicketActivity.kt` | Ticket edit — role-gated fields, spare/advance accumulation |
| `FinanceActivity.kt` | Monthly finance summary with per-tech breakdown |
| `firestore.rules` | Deployed rules — role checks, recycle-bin admin-only, index guards |

## Recent Changes

- **v21** — Remove Last Call Received from tech status; cumulative spare pending (append not overwrite); real-time admin list fix (fire only on new `lastServerUpdateAt`)
- **v20** — Archive → Delete (recycle bin, 30-day purge); remove Resolved status; auth race condition fix; email fields removed from UI; lowercase username migration
- **Security hardening** — Firestore rules tightened; admin guard before deleted-ticket queries; `commit()` over `apply()` for migration prefs
- **v17b** — One-time migration to lowercase all `username` and `technicianUsername` fields in Firestore
- **v14** — Finance screen (Admin + Office Staff); `petrolAmount` field added; incentive removed

## Setup

```bash
# 1. Create Firebase project — enable Auth (username/password) + Firestore
# 2. Deploy Firestore rules: firebase deploy --only firestore:rules
# 3. Add app/google-services.json from Firebase Console
# 4. Build
./gradlew assembleDebug
```

## Status

Active development. Internal use — AC service business operations.

→ [Back to Projects](/projects/)
