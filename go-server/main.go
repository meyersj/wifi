package main

import (
	"github.com/BurntSushi/toml"
	"log"
)

type Config struct {
	Port     string
	Postgres string
	Cert     string
	Key      string
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
	StartServer(conf)
}
