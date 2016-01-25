Setting up API Server
=====================

You must have `go` installed and your `$GOPATH` set and PostgreSQL installed.

Install Go packages
```bash
go get github.com/lib/pq
go get github.com/BurntSushi/toml
go get github.com/yvasiyarov/gorelic
```

Assuming you have built an empty Postgres database called `wifi`
```bash
psql -f sql/create.sql -d wifi
psql -f sql/manuf.sql -d wifi
```

Setup config file
```bash
cp sample-config.toml config.toml
```

Set postgres uri and newrelic token if you want to monitor it.

Run
```bash
go build
./go-server
```

Setup as service using `wifi.conf` as a starting point for an upstart script.
You will need to modify the parameters so it matches you system. Once modified
copy it to `/etc/init`
```bash
sudo cp wifi.conf /etc/init/wifi.conf
sudo service wifi start
```
