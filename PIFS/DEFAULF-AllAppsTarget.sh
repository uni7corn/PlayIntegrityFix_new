# Rename to AllAppsTarget.sh once completed.
# Move path: /data/adb/tricky_store/AllAppsTarget.sh

# Telegram: t.me/cleverestech

#!/bin/sh

su -c "magisk --denylist add com.google.android.gms com.google.android.gms.unstable"
su -c "magisk --denylist add com.google.android.gsf com.google.process.gservices"
su -c "magisk --denylist add com.google.android.gsf com.google.process.gapps"

# Create or overwrite the target.txt file
su -c > /data/adb/tricky_store/target.txt

# Use to list all packages and process the output directly to target.txt
su -c pm list packages | awk -F: '{print $2}' > /data/adb/tricky_store/target.txt

# --- Fetch Random Keybox on action ---
# This section attempts to download a new random keybox.xml from the server.
KEYBOX_ACTION_DIR="/data/adb/tricky_store"
KEYBOX_ACTION_PATH="$KEYBOX_ACTION_DIR/keybox.xml"
KEYBOX_ACTION_URL="https://tryigit.dev/keybox/download.php?id=random_strong"

echo " "
echo "🔄 Processing keybox.xml update via action..."

# Ensure target directory exists
su -c "mkdir -p \"$KEYBOX_ACTION_DIR\""

# Backup existing keybox.xml if it exists
if su -c "[ -f \"$KEYBOX_ACTION_PATH\" ]"; then
  su -c "mv \"$KEYBOX_ACTION_PATH\" \"${KEYBOX_ACTION_PATH}.backup\""
  echo "  - Backed up existing keybox.xml to keybox.xml.backup"
fi

echo "  - Attempting to download a new random keybox from server..."
# Use su -c for curl to ensure permissions for writing to /data/adb/tricky_store
if su -c "curl -Lsf \"$KEYBOX_ACTION_URL\" -o \"$KEYBOX_ACTION_PATH\""; then
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
# --- End Fetch Random Keybox on action ---
