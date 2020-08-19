==========================
Cisco.Meraki Release Notes
==========================

.. contents:: Topics


v1.4.0
======

Minor Changes
-------------

- meraki_ssid - Add `WPA3 Only` and `WPA3 Transition Mode`

Security Fixes
--------------

- meraki_webhook - diff output may show data for values set to not display

v1.3.2
======

Minor Changes
-------------

- meraki_device - Added deprecation notices to some parameters
- meraki_network - Added deprecation notices to some parameters

Bugfixes
--------

- Fixed sanity errors in all modules including documentation and argument specs
- Remove unnecessary files from the collection package, significantly reduces package size
- meraki_ssid - Specifying tags for VLAN information would crash as it was an improper type
- meraki_webhook - Fix crash with missing variable
- meraki_webhook - Fix response when creating webhook test
