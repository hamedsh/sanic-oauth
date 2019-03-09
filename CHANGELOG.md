# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2019-03-09

### Added

- Multi-providers configuration example (thanks to @ashleysommer)

## [0.3.0] - 2019-01-25

### Added

- Cache for user info to speed-up requests
- commitezen and commit/push hooks

## [0.2.5] - 2018-08-08

### Fixed

- `user_info_url` now can be passed via env variable `SANIC_OAUTH_USER_INFO_URL`

### Changed

- `create_oauth_factory` blueprint now will start after (!) server start to provide ability to configure aplication itself
- All requirements properly pinned

## [0.2.4] - 2018-06-13

### Fixed

- Redirect to previous page (#5)

### Changed

- GoogleProvider now use pure oauth api instead of google+ api (#2)

## [0.2.3] - 2018-05-15

### Fixed

- Redirect to oauth in case when token is expired in blueprint

## [0.2.2] - 2018-05-10

### Fixed

- Problem with `OAUTH_EMAIL_REGEX` not set

## [0.2.1] - 2018-05-10

### Added

- Ability to ignore user info
- Local email regex
- Global email regex

## [0.2.0] - 2018-05-05

### Added

- Blueprint for base oauth usage

## [0.1.2] - 2018-05-02

### Added

- Discord support
- Usefull logging in example

## [0.1.1] - 2018-01-29

### Fixed

- `setup.py` problem

[Unrelesed]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.2.4...master
[0.2.4]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.2.3...v0.2.4
[0.2.3]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.2.2...v0.2.3
[0.2.2]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.2.1...v0.2.2
[0.2.1]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.2.0...v0.2.1
[0.2.0]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.1.2...v0.2.0
[0.1.2]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.1.1...v0.1.2
[0.1.1]: https://gitlab.com/SirEdvin/sanic-oauth/compare/v0.1.0...v0.1.1
