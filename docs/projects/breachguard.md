---
description: Privacy-first password and email breach monitor for Android and iOS.
updated: 2026-05-17
---

# BreachGuard

> Privacy-first password and email breach monitor for Android and iOS.

BreachGuard lets users check whether their passwords or email addresses have appeared in known data breaches — using the [HaveIBeenPwned](https://haveibeenpwned.com) database — without ever transmitting sensitive data.

## Privacy Model

Passwords are **never sent to any server**. The process:

1. SHA-1 hash computed **on-device**
2. Only the **first 5 characters** of the hash sent to the HIBP API
3. API returns all hashes matching that prefix
4. Full hash matched **locally**

This is **k-anonymity** — the server learns nothing about the actual password. Emails are stored in `flutter_secure_storage` (AES-256 on Android, Keychain on iOS). No analytics events include credential data.

## Features

- Check passwords against 10B+ breached records (k-anonymity)
- Monitor email addresses for new breach notifications
- Push notifications via Firebase Cloud Messaging
- Freemium — basic checks free; monitoring behind RevenueCat subscription (`pro_access` entitlement) with 7-day trial
- AdMob banner + interstitial for free tier

## Stack

| Layer | Technology |
| --- | --- |
| Framework | Flutter (Dart) |
| Android build | AGP 8.7, Kotlin 2.1, Gradle 8.11.1, compileSdk/targetSdk 36, minSdk 23 |
| Backend | Firebase Auth, Firestore, FCM |
| Breach API | HaveIBeenPwned v3 |
| Monetization | RevenueCat `purchases_flutter` v10 |
| Ads | Google AdMob (`google_mobile_ads` v5+) |
| Background | WorkManager v0.9 |
| Secure storage | `flutter_secure_storage` |

## Architecture

```text
lib/
├── main.dart               # Entry point, service init, WorkManager callbackDispatcher
├── app/                    # MaterialApp root + named routes
├── core/                   # Constants, theme, utilities
├── models/                 # Breach, MonitoredEmail
├── services/               # HIBP, RevenueCat, AdMob, FCM, SecureStorage
├── features/               # Screens by feature (dashboard, password, email, paywall, settings, onboarding)
└── widgets/                # Shared UI components
```

## Security Highlights

- Passwords hashed locally — never transmitted
- Only 5-char hash prefix sent (k-anonymity)
- Emails in AES-256 encrypted storage
- `android:usesCleartextTraffic="false"` enforced
- No credentials in analytics events

## Setup

```bash
# 1. Flutter dependencies
flutter pub get

# 2. Firebase — add config files
#    android/app/google-services.json
#    ios/Runner/GoogleService-Info.plist

# 3. RevenueCat — set keys in lib/core/constants.dart
#    YOUR_REVENUECAT_ANDROID_KEY / YOUR_REVENUECAT_IOS_KEY
#    Create entitlement: pro_access

# 4. AdMob — replace test ad unit IDs in lib/core/constants.dart before release

# 5. HIBP API Key — users enter in-app via Settings → stored in encrypted local storage

# 6. Run
flutter run
```

See `RELEASE_SETUP.md` for full pre-release checklist (Firebase, RevenueCat, AdMob, keystore signing).

## Key Files

| File | Purpose |
| --- | --- |
| `lib/services/hibp_service.dart` | k-anonymity password check — local SHA-1 + prefix API call |
| `lib/services/subscription_service.dart` | RevenueCat v10 — `PurchaseResult` API, `PlatformException` error handling |
| `lib/core/constants.dart` | All third-party keys and ad unit IDs (replace before release) |
| `RELEASE_SETUP.md` | Pre-release checklist |
| `ANDROID_STUDIO_SETUP.md` | Android Studio build guide |

## Recent Changes

- **AdMob fix** — replaced invalid placeholder App ID with Google test IDs; app now boots cleanly (`MobileAdsInitProvider` validates at process start)
- **Android build fixes** — `purchases_flutter` v6 → v10 (v1 embedding removed); `workmanager` v0.5 → v0.9; AGP 8.7, Kotlin 2.1, Gradle 8.11.1, targetSdk 36
- **Launcher icons** — generated adaptive icons (all densities) with shield foreground + dark background
- **Android Studio setup** — migrated `settings.gradle` to Flutter 3.22+ `pluginManagement` format
- **Initial implementation** — full production build: k-anonymity, HIBP email monitoring, RevenueCat subscription, AdMob, FCM, dark terminal-green theme

## Status

Active development. Not yet publicly released.

→ [Back to Projects](/projects/)
