
To report bugs, please set the DEBUG=1 environment variable to collect logs:

```sh
DEBUG=1 meshcot
```

Or:

```sh linenums="1"
export DEBUG=1
meshcot
```

Or:

```sh linenums="1"
echo 'DEBUG=1' >> meshcot.ini
meshcot -c meshcot.ini
```

You can view systemd/systemctl/service logs via:

```journalctl -fu meshcot```

Please use GitHub issues for support requests. Please note that MeshCOT is free open source software and comes with no warranty. See LICENSE.