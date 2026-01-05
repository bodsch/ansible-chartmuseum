
# Ansible Role:  `chartmuseum`

Installs and configure a [chartmuseum](https://github.com/helm/chartmuseum) server on varoius linux systems.


[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/bodsch/ansible-chartmuseum/main.yml?logo=github&branch=main)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-chartmuseum?logo=github)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-chartmuseum?logo=github)][releases]
[![Ansible Downloads](https://img.shields.io/ansible/role/d/bodsch/chartmuseum?logo=ansible)][galaxy]

[ci]: https://github.com/bodsch/ansible-chartmuseum/actions
[issues]: https://github.com/bodsch/ansible-chartmuseum/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-chartmuseum/releases
[galaxy]: https://galaxy.ansible.com/ui/standalone/roles/bodsch/chartmuseum/

If `latest` is set for `chartmuseum_version`, the role tries to install the latest release version.
**Please use this with caution, as incompatibilities between releases may occur!**

The binaries are installed below `/usr/local/opt/chartmuseum/${chartmuseum_version}` and later linked to `/usr/bin`.
This should make it possible to downgrade relatively safely.

The chartmuseum archive is stored on the Ansible controller, unpacked and then the binaries are copied to the target system.
The cache directory can be defined via the environment variable `CUSTOM_LOCAL_TMP_DIRECTORY`.
By default it is `${HOME}/.cache/ansible/chartmuseum`.
If this type of installation is not desired, the download can take place directly on the target system.
However, this must be explicitly activated by setting `chartmuseum_direct_download` to `true`.


## Requirements & Dependencies

Ansible Collections

- [bodsch.core](https://github.com/bodsch/ansible-collection-core)
- [bodsch.scm](https://github.com/bodsch/ansible-collection-scm)

```bash
ansible-galaxy collection install bodsch.core
ansible-galaxy collection install bodsch.scm
```
or
```bash
ansible-galaxy collection install --requirements-file collections.yml
```

### Operating systems

Tested on

* Arch Linux
* Debian based
    - Debian 12 / 13
    - Ubuntu 22.04 / 24.04

> **RedHat-based systems are no longer officially supported! May work, but does not have to.**


## usage

**Currently, only `local` storage is supported.**


```yaml
chartmuseum_version: '0.16.3'

chartmuseum_system_group: chartmuseum
chartmuseum_system_user: "{{ chartmuseum_system_group }}"
chartmuseum_config_dir: /etc/chartmuseum

chartmuseum_direct_download: false

chartmuseum_release:
  download_url: https://get.helm.sh

chartmuseum_systemd:
  unit:
    after:
      - syslog.target
      - network.target
    wants: []
    requires: []
  service:
    limits:
      nofile:
        soft: ""
        hard: ""

chartmuseum_service: {}
```

### `chartmuseum_service`

```yaml
chartmuseum_service:
  debug: true
  listen:
    host: 127.0.0.1
    port: 8080
  chart_url: ""
  depth: 1
  log:
    json: true
    latency_integer: false
    health: false
  storage:
    backend: local
    local:
      rootdir: /var/cache/chartmuseum
  cache:
    redis:
      address: "127.0.0.1:6379"
      password: ""
      db: "0"
    interval: "30m"
  metrics: true
```


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-chartmuseum/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
