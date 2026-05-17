# BreachGuard

> Privacy-first password and email breach monitor for Android and iOS.

BreachGuard lets users check whether their passwords or email addresses have appeared in known data breaches — using the [HaveIBeenPwned](https://haveibeenpwned.com) database — without ever transmitting sensitive data.

## Privacy Model

Passwords are **never sent to any server**. The process:

1. SHA-1 hash is computed **on-device**
2. Only the **first 5 characters** of the hash are sent to the HIBP API
3. The API returns all hashes matching that prefix
4. The full hash is matched **locally**

This is called **k-anonymity** — the server learns nothing about the actual password.

Emails are stored using `flutter_secure_storage` (AES-256 on Android, Keychain on iOS). No analytics events include credential data.

## Features

- Check passwords against 10B+ breached records (k-anonymity)
- Monitor email addresses for new breach notifications
- Push notifications via Firebase Cloud Messaging
- Freemium model — basic checks free, monitoring via RevenueCat subscription
- AdMob integration for free tier

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flutter (Dart) |
| Backend | Firebase (Auth, Firestore, FCM) |
| Breach API | HaveIBeenPwned v3 |
| Monetization | RevenueCat (`pro_access` entitlement) |
| Ads | Google AdMob |
| Secure storage | `flutter_secure_storage` |

## Architecture

```
lib/
├── main.dart               # Entry point, service initialisation
├── app/                    # MaterialApp root + named routes
├── core/                   # Constants, theme, utilities
├── models/                 # Breach, MonitoredEmail
├── services/               # HIBP, RevenueCat, AdMob, FCM, SecureStorage
├── features/               # Screens by feature
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
# 1. Install Flutter dependencies
flutter pub get

# 2. Add Firebase config files
#    android/app/google-services.json
#    ios/Runner/GoogleService-Info.plist

# 3. Set RevenueCat keys in lib/core/constants.dart
#    YOUR_REVENUECAT_ANDROID_KEY
#    YOUR_REVENUECAT_IOS_KEY

# 4. Set HIBP API key (users enter in-app via Settings)

# 5. Run
flutter run
```

## Status

Active development. Not yet publicly released.

→ [Back to Projects](/projects/)
