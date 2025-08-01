# China?
Since all users generally use this module, China Rom developments are integrated into this module. So this module is recommended for official China Rom. 

> [!CAUTION]
> This module will permanently remove 32-bit support from your Magisk installation. The only way to restore it is by completely reinstalling Magisk and your other Zygisk modules. Please understand this consequence before proceeding.

---

## 🚀 Module Versions: PIFS vs. PIFB

This project offers two distinct versions to suit different needs. Choose the one that best fits your device and use case.

| Feature / Aspect      | PIFS (Advanced) 🧠                                        | PIFB (Lite) 🍃                                             |
| --------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| **Full Name**         | Play Integrity Fix **Advanced**                            | Play Integrity Fix **Lite**                                |
| **Core Method**       | New, improved infrastructure from Lsposed developers.      | Older, lightweight method.                                 |
| **Targeting**         | Granular control: Affects only apps in `target.txt`.       | Global: Hooks only the Google Services Framework (GSF).    |
| **Bootloader Hiding** | ✅ Yes, includes advanced Bootloader hiding.               | ❌ No, basic props only.                                   |
| **RAM Usage**         | Higher                                                     | Lower                                                      |
| **Android Requirement** | Android 11+                                              | Android 10+                                                |
| **ROM Compatibility** | Any ROM (Official China ROM recommended)                   | Any ROM (Official China ROM recommended)                   |
| **Hardware Key**      | Not strictly required.                                     | TEE (Trusted Execution Environment) must be functional.    |

> [!WARNING]
> Frequent integrity checks can lead to your device's fingerprint/keybox being blocked by Google. **Avoid checking unnecessarily.**

---

## 📋 Requirements

Before installing, ensure your device meets these requirements:

*   **Root Solution:** Magisk or KernelSU
*   **Zygisk:** Enabled
*   **CPU Architecture:** 64-bit (arm64-v8a)
*   **ROM:** Official ROM is highly recommended for best results (especially China ROM).

---

## ✨ Key Features

### General Features
*   **Motherboard Spoofing:**
    *   **`ro.product.board` -> `MP`:** Sets the motherboard identifier to `MP` (Mass Production), making it appear as a standard retail device.
    *   **`ro.boot.hwc` -> `CN`:** Sets the hardware country code to China. This can help bypass regional restrictions on some Xiaomi devices.
*   **32-bit Support Removal:** Disables 32-bit components in Magisk and Zygisk-dependent modules (like LSPosed) to reduce unnecessary RAM usage.
*   **Zygote 32-bit Lazyload (Xiaomi):** On supported Xiaomi devices, the 32-bit Zygote process will only launch when a 32-bit app is opened, saving RAM at the cost of a slight initial launch delay for those apps. Also disables 32-bit dex2oat optimization.
*   **Disable LSPosed Logs:** Prevents apps from detecting Zygisk by reading LSPosed properties via `getprop`.
*   **Dynamic Prop Hiding:** If Shamiko is installed, the module avoids setting redundant properties. If Shamiko is not present, it applies basic properties to help bypass simple bootloader checks.

### Maintenance & Self-Healing (PIFS Only)
To provide a seamless "set it and forget it" experience, the module incorporates intelligent, automated systems that work in the background to maintain compliance and resilience.

*   **Dynamic Security Patch Spoofing:** Breathe new life into older devices. The module intelligently detects if your device's security patch is more than 6 months old. If so, it automatically spoofs the patch date to a recent, plausible value, helping you pass integrity checks even on unsupported hardware. This process is fully automatic, requiring zero user intervention.
*   **Proactive Keybox Rotation:** To stay one step ahead of Google's detection methods, the module actively refreshes its disguise. During specific actions (like an update), it attempts to download a fresh, random, and strong-rated `keybox.xml` from the community-driven KeyboxHub. Your existing keybox is safely backed up and restored if the download fails, ensuring you're never left vulnerable. This self-updating mechanism significantly increases your long-term success rate for passing `STRONG` integrity.

### Version-Specific Features
*   **Advanced Bootloader Hiding (PIFS Only):** Actively prevents applications from detecting an unlocked bootloader. By default, this targets all applications for maximum effectiveness.
*   **Prop & Certificate Spoofing:**
    *   **PIFB (Lite):** A simple and classic hook that only targets the GMS (Google Mobile Services) process to spoof the device certificate.
    *   **PIFS (Advanced):** A modern and customizable method that spoofs the certificate only for apps defined in `target.txt`.
    *   *Both versions* automatically use a random keybox file on each boot to evade detection.

---

## 🛠️ Configuration & File Paths

You can customize the module's behavior by creating or modifying the files below.

### Fingerprint File (PIFB Only)
Used to spoof the device fingerprint.
*   **Path:** `/data/adb/pif.json`

### Target Apps File (PIFS Only)
A list of package names that the module will target.
*   **Path:** `/data/adb/tricky_store/target.txt`
> [!NOTE]
> To customize this list, you **must first delete** the script below, which auto-populates it on every boot.
> `/data/adb/tricky_store/AllAppsTarget.sh`

### Keybox File (PIFS & PIFB)
Used for certificate spoofing to pass the `STRONG` integrity check.
   **PIFB Path:** `/data/adb/keybox.xml`
   **PIFS Path:** `/data/adb/tricky_store/keybox.xml`
   **Guide:** To find and contribute keybox files, visit

[KeyboxHub](https://tryigit.dev/keybox/).

[Keybox Checker](https://tryigit.dev/keybox/checker/).

### Security Patch File (PIFS Only)
Spoofs the security patch date, which can help pass integrity checks on EOL (End-of-Life) devices running Android 13+. This file does not exist by default; you must create it.
   **Path:** `/data/adb/tricky_store/security_patch.txt`
   **Example Content** (for January 1, 2025):
    ```
    20250101
    ```

## ⚙️ Advanced Settings (Use with Caution)

### Add All System Apps to Magisk's DenyList
This experimental feature automatically adds all system apps to the Magisk DenyList. It is disabled by default due to potential conflicts.

> [!WARNING]
> This feature may cause instability or break modules that modify system files (e.g., custom GPU drivers). **Do not use on Custom ROMs.** To enable it, move the corresponding script file into its active path.

   **PIFB Script:** `/data/adb/SystemAppAdd.sh`
   **PIFS Script:** `/data/adb/tricky_store/AllTargetMagiskhide.sh`

### How to Check Your Motherboard's Hardware Country
Run this command in a terminal to see your device's factory region code:
```sh
getprop ro.boot.hwc
```

## 💬 Community & Disclaimer

**Telegram:** For discussions and community support, join the [Clever Tech Telegram Group](https://t.me/cleverestech).

> [!NOTE]
> This project is shared "as-is" for users who find it helpful. This GitHub repository primarily serves to distribute updates and is a fork of another project (see changelog for attribution).
