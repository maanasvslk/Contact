#!/bin/bash
set -e  # Exit immediately if any command fails

# Create required directories
mkdir -p /opt/nagios/var/{rw,spool/checkresults,archives}

# Set permissions
chown -R nagios:nagios /opt/nagios/var
chmod -R 775 /opt/nagios/var
chown nagios:www-data /opt/nagios/var/rw
chmod g+s /opt/nagios/var/rw

# Verify config before starting
echo "Verifying Nagios configuration..."
/opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg

# Start Apache in background
echo "Starting Apache..."
service apache2 start

# Start Nagios in foreground
echo "Starting Nagios..."
exec /opt/nagios/bin/nagios /opt/nagios/etc/nagios.cfg