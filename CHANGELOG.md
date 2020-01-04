# Changelog

## v1.0.0

## Enhancements
* meraki_network - Add support for check mode

### v0.1.2

## Enhancements
* Add template for inventory.networking file

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
