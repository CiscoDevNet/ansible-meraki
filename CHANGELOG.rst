==========================
Cisco.Meraki Release Notes
==========================

.. contents:: Topics


v2.6.2
======

Minor Changes
-------------

- Add execution-environment.yml in meta as the base to a Meraki ee
- meraki_network - Add Products to net_type list

Bugfixes
--------

- meraki_alert - Updates now properly set default destination webhook
- meraki_syslog -  Fix crash due to incorrect dictionary reference

v2.6.1
======

Minor Changes
-------------

- meraki_ssid - Add support for enterprise_admin_access and splash_guest_sponsor_domains with the latter required for creating a sponsor portal.

Bugfixes
--------

- meraki_mr_rf_profile - Fix issue with idempotency and creation of RF Profiles by name only
- meraki_syslog - Improve reliability for multiple roles or capitalization.

v2.6.0
======

Major Changes
-------------

- meraki_mr_radio - New module

Minor Changes
-------------

- meraki_mx_l7_firewall - Allow passing an empty ruleset to delete all rules
- meraki_utils - Add debugging output for failed socket connections

Bugfixes
--------

- meraki_mr_ssid - Fix issue with SSID removal idempotency when ID doesn't exist

v2.5.0
======

Minor Changes
-------------

- meraki_mr_l3_firewall - Return each MR L3 firewall rule's values in lowercase.
- meraki_mr_ssid - Add support for radius_proxy_enabled SSID setting.
- meraki_mx_l3_firewall - Return each MX L3 firewall rule's values in lowercase.
- meraki_mx_vlan - Fix dhcp_boot_options_enabled parameter

v2.4.2
======

Bugfixes
--------

- Fix some flake8 sanity errors as reported by Ansible Galaxy. Should be no functional change.

v2.4.0
======

Minor Changes
-------------

- meraki_mx_switchport - Improve documentation for response

Bugfixes
--------

- Allow a state of absent in voice vlan to allow the value to be nulled out(https://github.com/CiscoDevNet/ansible-meraki/issues/238)

v2.3.1
======

Bugfixes
--------

- meraki_ms_switchport - link_negotiation choice for 100 Megabit Auto is incorrect causing failures. (https://github.com/CiscoDevNet/ansible-meraki/issues/235).

v2.3.0
======

Minor Changes
-------------

- meraki_ms_switchport - Adding additional functionality to support the access_policy_types "MAC allow list" and "Sticky MAC allow list" port security configuration options. (https://github.com/CiscoDevNet/ansible-meraki/issues/227).
- meraki_mx_intrusion_prevention - Rename message to rule_message to avoid conflicts with internal Ansible variables.

Bugfixes
--------

- meraki_ms_switchport - access_policy_types choices are incorrect causing failures. (https://github.com/CiscoDevNet/ansible-meraki/issues/227).

v2.2.1
======

Bugfixes
--------

- meraki_mx_content_filtering - Fix crash with idempotent condition due to improper sorting

v2.2.0
======

Minor Changes
-------------

- meraki_network - Update documentation to show querying of local or remote settings.
- meraki_ssid - Add Cisco ISE as a splash page option.

Bugfixes
--------

- meraki_network - Fix bug where local or remote settings always show changed.

v2.1.3
======

Bugfixes
--------

- meraki_device - Support pagination. This allows for more than 1,000 devices to be listed at a time.
- meraki_network - Support pagination. This allows for more than 1,000 networks to be listed at a time.

v2.1.2
======

Bugfixes
--------

- Remove test output as it made the collection, and Ansible, huge.

v2.1.1
======

Bugfixes
--------

- meraki_management_interface - Fix crash when modifying a non-MX management interface.

v2.1.0
======

New Modules
-----------

- meraki_alert - Manage alerts in the Meraki cloud
- meraki_mx_l2_interface - Configure MX layer 2 interfaces

v2.0.0
======

Major Changes
-------------

- Rewrite requests method for version 1.0 API and improved readability
- meraki_mr_rf_profile - Configure wireless RF profiles.
- meraki_mr_settings - Configure network settings for wireless.
- meraki_ms_l3_interface - New module
- meraki_ms_ospf - Configure OSPF.

Minor Changes
-------------

- meraki - Add optional debugging for is_update_required() method.
- meraki_admin - Update endpoints for API v1
- meraki_alert - Manage network wide alert settings.
- meraki_device - Added query parameter
- meraki_intrusion_prevention - Change documentation to show proper way to clear rules
- meraki_malware - Update documentation to show how to allow multiple URLs at once.
- meraki_mx_l2_interface - Configure physical interfaces on MX appliances.
- meraki_mx_uplink - Renamed to meraki_mx_uplink_bandwidth
- meraki_ssid - Add `WPA3 Only` and `WPA3 Transition Mode`
- meraki_switchport - Add support for `access_policy_type` parameter

Breaking Changes / Porting Guide
--------------------------------

- meraki_device - Changed tags from string to list
- meraki_device - Removed serial_lldp_cdp parameter
- meraki_device - Removed serial_uplink parameter
- meraki_intrusion_prevention - Rename whitedlisted_rules to allowed_rules
- meraki_mx_l3_firewall - Rule responses are now in a `rules` list
- meraki_mx_l7_firewall - Rename blacklisted_countries to blocked_countries
- meraki_mx_l7_firewall - Rename whitelisted_countries to allowed_countries
- meraki_network - Local and remote status page settings cannot be set during network creation
- meraki_network - `disableRemoteStatusPage` response is now `remote_status_page_enabled`
- meraki_network - `disable_my_meraki_com` response is now `local_status_page_enabled`
- meraki_network - `disable_my_meraki` has been deprecated
- meraki_network - `enable_my_meraki` is now called `local_status_page_enabled`
- meraki_network - `enable_remote_status_page` is now called `remote_status_page_enabled`
- meraki_network - `enabled` response for VLAN status is now `vlans_enabled`
- meraki_network - `tags` and `type` now return a list
- meraki_snmp - peer_ips is now a list
- meraki_switchport - `access_policy_number` is now an int and not a string
- meraki_switchport - `tags` is now a list and not a string
- meraki_webhook - Querying test status now uses state of query.

Security Fixes
--------------

- meraki_webhook - diff output may show data for values set to not display

Bugfixes
--------

- Remove unnecessary files from the collection package, significantly reduces package size
- meraki_admin - Fix error when adding network privileges to admin using network name
- meraki_switch_stack - Fix situation where module may crash due to switch being in or not in a stack already
- meraki_webhook - Proper response is shown when creating webhook test
