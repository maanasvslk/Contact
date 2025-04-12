#!/bin/bash
# Create required directories
mkdir -p /opt/nagios/var/rw
mkdir -p /opt/nagios/var/spool/checkresults
mkdir -p /opt/nagios/var/archives

# Set permissions
chown -R nagios:nagios /opt/nagios/var
chmod -R 775 /opt/nagios/var
chown nagios:www-data /opt/nagios/var/rw
chmod g+s /opt/nagios/var/rw

# Verify config before starting
/opt/nagios/bin/nagios -v /opt/nagios/etc/nagios.cfg || exit 1

# Start services
service apache2 start
exec /opt/nagios/bin/nagios /opt/nagios/etc/nagios.cfg