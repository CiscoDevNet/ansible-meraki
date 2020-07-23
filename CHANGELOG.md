# Changelog

## v1.3.1

### Bugfixes
* meraki_device - Rewrite module to be more reliable when hostname is specified
* meraki_admin - Fix crash when specifying networks parameter

## v1.2.1

### Bugfixes
* meraki_site_to_site_vpn - Enable idempotency and changed statuses

## v1.2.0

### New Modules
* meraki_ms_link_aggregation

## v1.1.0

### New Modules
* meraki_management_interface
* meraki_mx_uplink
* meraki_site_to_site_vpn

### New Modules
* meraki_management_interface

### Features
* meraki_vlan - Add full DHCP server configuration support

## Bugfixes
* meraki_mx_l3_firewall - Fix idempotency when 'any' is passed as a parameter

## v1.0.3

### Miscellaneous
* Remove accidentally added meraki_site_to_site_vpn module which shouldn't have been published

## v1.0.2

### Bugfixes
* meraki_static_route - Fix idempotency bugs triggered with certain parameters
* meraki_mx_l3_firewall - Remove unnecessary org lookup which may crash

## v1.0.1

### Bugfixes
* meraki_mx_l3_firewall - Fix condition where firewall rules wouldn't update

## v1.0.0

### Enhancements
* meraki_organzation - A confirmation is needed to delete an organization since it can be a catastrophic change
* meraki_network - Add support for check mode
* meraki_mr_l3_firewall - Add check mode
* meraki_mx_l3_firewall - Add check mode
* meraki_ssid - Add support for check mode
* meraki_switchport - Add check mode
* Add template for inventory.networking

### New Modules
* meraki_intrusion_prevention

## v0.1.1

### Bugfixes
** Fix some sanity errors

## v0.1.0

### Enhancements
* diff generation now uses a centralized method instead of per module code

### Bugfixes
* diff now returns as snakecase instead of camelcase
* Modules which don't support check mode will now error if check mode is requested


## v0.0.1

### New Modules
* meraki_switch_storm_control

### Documentation
* Improve type documentation for module parameters
* Improve HTTP error reporting for 400 errors

### Bugfixes
* meraki_ssid - Properly formats the walled garden payload to Meraki
* Fix most linting errors (issue #13)
* Restructure tests directory
* Fix comparison check to not crash when comparing a dict to a non-dict (issue #6)
* Enable integration tests within collection
* Fix linting errors
* Fix crash when unbinding a template in check mode with net_id (issue #19)
* meraki_firewalled_services recognizes net_id
* Content filtering integration test deletes network after completion

## v0.0.0
* Initial commit of collection into Ansible Galaxy
