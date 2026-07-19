---
title: Privacy Policy
description: "How Offband handles your data. Short version: it doesn't leave your device, and there's no Offband server, account, or telemetry."
---

**Short version:** Offband has no servers, no accounts, and no telemetry. Your messages, contacts, and channels stay on your device. The app reaches out to a few third-party services only when you use the feature that needs them (maps, GIFs, offline translation, terrain), nothing else.

_Last updated: 2026-07-11_

## Who we are

Offband is a personal, open-source project (MIT), not a company. There is no Offband account, no Offband backend, and no Offband analytics. We can't see your data because it never reaches us.

## What stays on your device

Your mesh data (direct and channel messages, contacts, channels, and communities) is stored **locally on your device** and travels over the LoRa mesh through your own radio. It does not pass through any Offband server. Uninstalling the app or clearing its storage removes it.

## Third-party services (only when you use the feature)

The app connects to these outside services **only** when you use that specific feature. Each has its own privacy policy:

- **Maps (OpenStreetMap).** When you open the map, tile images are fetched from OpenStreetMap tile servers, which reveals the general area you're viewing. See [OSM privacy](https://wiki.osmfoundation.org/wiki/Privacy_Policy).
- **GIFs (GIPHY).** When you use the GIF picker, your search text is sent to GIPHY to return results. See [GIPHY privacy](https://support.giphy.com/hc/en-us/articles/360020027752-GIPHY-Privacy-Policy).
- **Offline translation (Hugging Face).** If you enable on-device translation, the language-model file is downloaded once from Hugging Face. Translation itself then runs **entirely on your device**, and your messages are not sent anywhere to be translated. See [Hugging Face privacy](https://huggingface.co/privacy).
- **Terrain / line-of-sight (Open-Meteo).** If you use elevation or line-of-sight features, the coordinates you're analysing are sent to Open-Meteo to look up terrain elevation. See [Open-Meteo terms](https://open-meteo.com/en/terms).

We don't control these services and don't receive anything back from them about you.

## Permissions and why the app asks

- **Location.** Required by Android to scan for Bluetooth devices on older versions, and to show your position on the map. Bluetooth scanning is flagged `neverForLocation`; the app does not use location for advertising or tracking, and does not send it to any server.
- **Bluetooth / USB.** To connect to and communicate with your MeshCore radio.
- **Camera.** Only to scan QR codes (contacts, channels). No photos are taken or stored.
- **Notifications.** To alert you to incoming messages.
- **Foreground service / wake lock.** To keep the connection to your radio alive while the app runs in the background.

## What we don't do

No ads. No selling or sharing of your data. No cross-app tracking. No analytics or crash-reporting SDKs. No account or sign-up.

## Data deletion

Offband is a personal, open-source app with **no accounts and no server**. All your data (messages, contacts, channels, and settings) is stored **on your device**, and Offband holds none of it. To delete your data:

- **Delete items in the app.** Remove individual contacts, channels, or messages.
- **Clear the app's data.** Android: Settings → Apps → *Offband MeshCore* → Storage → *Clear storage*. This removes all of the app's on-device data.
- **Uninstall the app.** This removes all Offband data from your device.

Offband does not retain any of your data on a server (there is none). The only data ever sent off your device is transient, for example map coordinates sent to look up terrain elevation, which is used in real time and not stored by us, so there is nothing held remotely to delete.

## Children

Offband is a general-purpose networking tool, not directed at children, and does not knowingly collect data from anyone.

## Changes

If this policy changes, we'll update this page and the date above.

## Contact

Questions: **support@offband.org**
