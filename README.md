# China ROM Integration

Since the majority of users rely on this module for their devices, developments specific to the official China ROM have been integrated. Therefore, this module is highly recommended for users on the official China ROM.

***

## Module Versions PIFS and PIFB

This project offers two distinct versions to suit different needs. Choose the version that best fits your device and use case.

### PIFS Advanced
* Full Name: Play Integrity Fix Advanced
* Core Method: New and improved infrastructure from LSPosed developers
* Targeting: Granular control which affects only apps specified in the target.txt file
* Bootloader Hiding: Yes, includes advanced bootloader hiding
* RAM Usage: Higher
* Android Requirement: Android 11 and above
* ROM Compatibility: Any ROM, official China ROM is recommended
* Hardware Key: Not strictly required

### PIFB Lite
* Full Name: Play Integrity Fix Lite
* Core Method: Older and lightweight method
* Targeting: Global, hooks only the Google Services Framework GSF
* Bootloader Hiding: No, provides basic properties only
* RAM Usage: Lower
* Android Requirement: Android 10 and above
* ROM Compatibility: Any ROM, official China ROM is recommended
* Hardware Key: TEE Trusted Execution Environment must be functional

> [!WARNING]
> Frequent integrity checks can lead to your device fingerprint or keybox being blocked by Google. Avoid performing checks unnecessarily.

***

## Requirements

Before proceeding with the installation, ensure your device meets the following requirements:

* Root Solution: Magisk or KernelSU
* Zygisk: Enabled
* CPU Architecture: 64 bit arm64 v8a
* ROM: Official ROM is highly recommended for optimal results, especially the China ROM

***

## Key Features

### General Features

* Motherboard Spoofing: Sets the motherboard identifier to MP Mass Production, making it appear as a standard retail device. Also sets the hardware country code to China which can help bypass regional restrictions on some Xiaomi devices.
* Disable LSPosed Logs: Prevents applications from detecting Zygisk by reading LSPosed properties via getprop.
* Dynamic Prop Hiding: If Shamiko is installed, the module avoids setting redundant properties. If Shamiko is not present, it applies basic properties to help bypass simple bootloader checks.

### Maintenance and Self Healing PIFS Only

To provide a seamless experience, the module incorporates intelligent and automated systems that work in the background to maintain compliance and resilience.

* Dynamic Security Patch Spoofing: Breathes new life into older devices. The module intelligently detects if your device security patch is more than six months old. If so, it automatically spoofs the patch date to a recent and plausible value, helping you pass integrity checks even on unsupported hardware. This process is fully automatic and requires zero user intervention.
* Proactive Keybox Rotation: To stay one step ahead of Google detection methods, the module actively refreshes its disguise. During specific actions such as an update, it attempts to download a fresh, random, and strong rated keybox.xml from the community driven KeyboxHub. Your existing keybox is safely backed up and restored if the download fails, ensuring you are never left vulnerable. This self updating mechanism significantly increases your long term success rate for passing STRONG integrity.

### Version Specific Features

* Advanced Bootloader Hiding PIFS Only: Actively prevents applications from detecting an unlocked bootloader. By default, this targets all applications for maximum effectiveness.
* Prop and Certificate Spoofing: PIFB Lite utilizes a simple and classic hook that only targets the GMS Google Mobile Services process to spoof the device certificate. PIFS Advanced utilizes a modern and customizable method that spoofs the certificate only for apps defined in the target.txt file. Both versions automatically use a random keybox file on each boot to evade detection.

***

## Configuration and File Paths

You can customize the behavior of the module by creating or modifying the following files.

### Fingerprint File PIFB Only
Used to spoof the device fingerprint.
* Path: /data/adb/pif.json

### Target Apps File PIFS Only
A list of package names that the module will target.
* Path: /data/adb/tricky_store/target.txt

> [!NOTE]
> To customize this list, you must first delete the script below which automatically populates it on every boot.
> /data/adb/tricky_store/AllAppsTarget.sh

### Keybox File PIFS and PIFB
Used for certificate spoofing to pass the STRONG integrity check.
* PIFB Path: /data/adb/keybox.xml
* PIFS Path: /data/adb/tricky_store/keybox.xml

Guide: To find and contribute keybox files, visit KeyboxHub or the Keybox Checker tool.

### Security Patch File PIFS Only
Spoofs the security patch date which can help pass integrity checks on End of Life devices running Android 13 and above. This file does not exist by default, you must create it manually.
* Path: /data/adb/tricky_store/security_patch.txt
* Example Content for January 1, 2025:
  20250101

***

## Advanced Settings Use with Caution

### Add All System Apps to Magisk DenyList
This experimental feature automatically adds all system apps to the Magisk DenyList. It is disabled by default due to potential conflicts.

> [!WARNING]
> This feature may cause instability or break modules that modify system files such as custom GPU drivers. Do not use this feature on Custom ROMs. To enable it, move the corresponding script file into its active path.

* PIFB Script: /data/adb/SystemAppAdd.sh
* PIFS Script: /data/adb/tricky_store/AllTargetMagiskhide.sh

### How to Check Your Motherboard Hardware Country
Run the following command in a terminal to see your device factory region code:
getprop ro.boot.hwc

***

## Community and Disclaimer

Telegram: For discussions and community support, join the Clever Tech Telegram Group.

> [!NOTE]
> This project is shared as is for users who find it helpful. This GitHub repository primarily serves to distribute updates and is a fork of another project, please see the changelog for attribution.
