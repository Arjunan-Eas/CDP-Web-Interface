SSID="quacknet"
PASSWORD="ducknet!"
INTERFACE="wlan0"

# Create the Wi-Fi hotspot
echo "Creating Wi-Fi hotspot..."
sudo nmcli device wifi hotspot ssid "$SSID" password "$PASSWORD" ifname "$INTERFACE"

# Get the UUID of the newly created hotspot
echo "Retrieving the UUID of the hotspot..."
UUID=$(nmcli connection show | grep "$SSID" | awk '{print $2}')

# Check if UUID was found
if [ -z "$UUID" ]; then
    echo "Error: Hotspot UUID not found. Ensure the hotspot was created successfully."
    exit 1
fi

# Modify the connection settings
echo "Modifying connection settings for UUID $UUID..."
sudo nmcli connection modify "$UUID" connection.autoconnect yes connection.autoconnect-priority 100

echo "Installation and configuration complete."