from __future__ import annotations, unicode_literals

import os

import pytest
import testinfra.utils.ansible_runner
from helper.molecule import get_vars, infra_hosts, local_facts

testinfra_hosts = infra_hosts(host_name="instance")

# --- tests -----------------------------------------------------------------


def test_user(host, get_vars):
    """ """
    user = get_vars.get("chartmuseum_system_user", "chartmuseum")
    group = get_vars.get("chartmuseum_system_group", "chartmuseum")

    assert host.group(group).exists
    assert host.user(user).exists
    assert group in host.user(user).groups


def test_version(host):
    """ """
    _facts = local_facts(host=host, fact="chartmuseum")

    version = _facts.get("version")

    install_dir = f"/usr/local/opt/chartmuseum/{version}"
    install_bin = f"{install_dir}/chartmuseum"
    binary_link = "/usr/bin/chartmuseum"

    print(install_dir)

    directory = host.file(install_dir)
    assert directory.is_directory

    binary = host.file(install_bin)
    assert binary.is_file

    link = host.file(binary_link)
    assert link.is_symlink
    assert link.linked_to == install_bin


def test_storage_directory(host, get_vars):
    """ """
    storage = (
        get_vars.get("chartmuseum_service", {})
        .get("storage", {})
        .get("local", {})
        .get("rootdir", None)
    )

    print(storage)

    if storage:
        directory = host.file(storage)
        assert directory.is_directory


def test_service(host, get_vars):
    service = host.service("chartmuseum")
    assert service.is_enabled
    assert service.is_running


def test_open_port(host, get_vars):
    for i in host.socket.get_listening_sockets():
        print(i)

    chartmuseum_service = get_vars.get("chartmuseum_service", {})

    print(chartmuseum_service)

    listen_address = "127.0.0.1:8080"

    if isinstance(chartmuseum_service, dict):
        _listen = chartmuseum_service.get("listen")

        if isinstance(_listen, dict):
            _address = _listen.get("host")
            _port = _listen.get("port")

            listen_address = f"{_address}:{_port}"

    service = host.socket(f"tcp://{listen_address}")
    assert service.is_listening
