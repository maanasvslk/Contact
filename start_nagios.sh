#!/bin/bash
# Fix permissions
chown -R nagios:nagios /opt/nagios/var
chmod -R 775 /opt/nagios/var

# Create necessary directories
mkdir -p /opt/nagios/var/rw
mkdir -p /opt/nagios/var/spool/checkresults
chown nagios:nagios /opt/nagios/var/rw
chown nagios:nagios /opt/nagios/var/spool/checkresults

# Start Nagios
/usr/local/nagios/bin/nagios /opt/nagios/etc/nagios.cfg