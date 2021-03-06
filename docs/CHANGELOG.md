# Milkyway Bot - Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.0.7] | 2022-01-05
### Added/Removed
- Added to use Telegram as notification instead of Slack
### Changed
### Fixed

## [1.0.6] | 2021-12-27
### Added/Removed
### Changed
### Fixed
- Fixed getting wrong OldTag

## [1.0.5] | 2021-12-07
### Added/Removed
- Added error log when OWNERS not existing
- Added disableProxy for Slack after sending notification
### Changed
### Fixed

## [1.0.4] | 2021-11-10
### Added/Removed
- Added Revoking Approval feature
### Changed
- Changed Application's name
- Changed application's structure
### Fixed

## [1.0.3] | 2021-11-06
### Added/Removed
- Added Proxy setting option used for Slack or outgoing traffic
### Changed
- Changed module directory structure
### Fixed

## [1.0.2] | 2021-11-04
### Added/Removed
- Dockerized Gitbot
### Changed
### Fixed

## [1.0.1] | 2021-11-03
### Added/Removed
- Added Slack to inform when finishing changing tag
- Added colored text to Slack msg
### Changed
### Fixed

## [1.0.0] | 2021-10-27 - Official version
### Added/Removed
### Changed
- Changed processing filenames
### Fixed

## [0.1.6] | 2021-10-26
### Added/Removed
- Removed condition to check wrong image tag
- Added to check oldTag when Repository not found
- Added logging when imageTag wrong (format)
### Changed
### Fixed
- Minor fixes

## [0.1.5] | 2021-10-25
### Added/Removed
- Add condition to check wrong image tag
### Changed
- Changed logic to check Test Environment's image tag
### Fixed

## [0.1.4] | 2021-08-18
### Added/Removed
### Changed
- Changed logic to get approvers
### Fixed
- Fixed the error when there are more than one OWNERS file

## [0.1.3] | 2021-07-26
### Added/Removed
### Changed
### Fixed
- Fixed error not creating release branch

## [0.1.2] | 2021-07-21
### Added/Removed
- Add merge request policy
- Add optional comment for Cloud version
### Changed
- Change Regex pattern to match oldTag
### Fixed

## [0.1.1] | 2021-07-21
### Added/Removed
### Changed
- Change conditions to match checkEnvironment
### Fixed

## [0.1.0] | 2021-07-20
### Added/Removed
- Release the first version
- Add a Regex module filtering old tags
- Add a validation of OWNERS file
- Add a validation of project id
- Add regex patterns to check Release tag built from CI
### Changed
### Fixed