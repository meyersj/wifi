package main

import (
	"github.com/BurntSushi/toml"
	"github.com/yvasiyarov/gorelic"
	"log"
)

type Config struct {
	Port     string
	Postgres string
	NewRelic string
}

func ReadConfig(filename string) *Config {
	var conf Config
	if _, err := toml.DecodeFile(filename, &conf); err != nil {
		log.Println("Failed to decode config file: ", filename)
		log.Fatal("Try copying sample-config.toml to config.toml and set parameters")
	}
	return &conf
}

func main() {
	conf := ReadConfig("config.toml")
	if conf.NewRelic != "" {
		agent := gorelic.NewAgent()
		agent.Verbose = true
		agent.NewrelicLicense = conf.NewRelic
		agent.Run()
	}
	StartServer(conf)
}
