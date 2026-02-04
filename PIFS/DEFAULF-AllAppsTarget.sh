# Rename to AllAppsTarget.sh once completed.
# Move path: /data/adb/tricky_store/AllAppsTarget.sh

# Telegram: t.me/cleverestech

#!/bin/sh

find_busybox() {
  [ -n "$BUSYBOX" ] && return 0
  for path in /data/adb/modules/busybox-ndk/system/*/busybox /data/adb/magisk/busybox /data/adb/ksu/bin/busybox /data/adb/ap/bin/busybox; do
    if [ -x "$path" ]; then
      BUSYBOX="$path"
      return 0
    fi
  done
  return 1
}

if ! find_busybox; then
  echo "Error: BusyBox not found. This script requires Magisk or KernelSU."
  exit 1
fi

su -c "magisk --denylist add com.google.android.gms com.google.android.gms.unstable" 2>/dev/null
su -c "magisk --denylist add com.google.android.gsf com.google.process.gservices" 2>/dev/null
su -c "magisk --denylist add com.google.android.gsf com.google.process.gapps" 2>/dev/null

su -c "> /data/adb/tricky_store/target.txt"
su -c "pm list packages | $BUSYBOX awk -F: '{print \$2}' > /data/adb/tricky_store/target.txt"

KEYBOX_ACTION_DIR="/data/adb/tricky_store"
KEYBOX_ACTION_PATH="$KEYBOX_ACTION_DIR/keybox.xml"
KEYBOX_ACTION_URL="https://tryigit.dev/keybox/download.php?id=random_strong"

echo " "
echo "🔄 Processing keybox.xml update via action..."

su -c "mkdir -p \"$KEYBOX_ACTION_DIR\""

if su -c "[ -f \"$KEYBOX_ACTION_PATH\" ] && mv \"$KEYBOX_ACTION_PATH\" \"${KEYBOX_ACTION_PATH}.backup\""; then
  echo "  - Backed up existing keybox.xml to keybox.xml.backup"
fi

echo "  - Attempting to download a new random keybox from server..."
if su -c "$BUSYBOX wget -q -O \"$KEYBOX_ACTION_PATH\" \"$KEYBOX_ACTION_URL\""; then
  echo "  - New keybox.xml downloaded successfully."
else
  echo "  ⚠️ Failed to download new keybox.xml."
  echo "     Please check your internet connection."
  if su -c "[ -f \"${KEYBOX_ACTION_PATH}.backup\" ]"; then
    su -c "mv \"${KEYBOX_ACTION_PATH}.backup\" \"$KEYBOX_ACTION_PATH\""
    echo "  - Restored backup keybox.xml."
  else
    echo "  ⚠️ No backup keybox.xml found to restore."
  fi
fi
