package main

import (
	"log"
	"net"
	"net/http"
	"regexp"
)

func GetInterfaceIPs() []string {
	regex := "[0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+"
	addrs, _ := net.InterfaceAddrs()
	interfaces := []string{}
	for _, addr := range addrs {
		var ip net.IP
		switch v := addr.(type) {
		case *net.IPNet:
			ip = v.IP
		case *net.IPAddr:
			ip = v.IP
		}
		match, _ := regexp.MatchString(regex, ip.String())
		if match {
			interfaces = append(interfaces, ip.String())
		}
	}
	return interfaces
}

func StartServer(c *Config) {
	db := InitDBClient(c.Postgres)
	AttachHandlers(db)
	interfaces := GetInterfaceIPs()
	for i := 0; i < len(interfaces); i++ {
		host := interfaces[i] + ":" + c.Port
		if c.Cert != "" && c.Key != "" {
			log.Println("Starting secure server at " + host)
			go http.ListenAndServeTLS(host, c.Cert, c.Key, nil)
		} else {
			log.Println("Starting server at " + host)
			go http.ListenAndServe(host, nil)
		}
	}
	select {}
}

func AttachHandlers(db *DBClient) {
	http.Handle("/", &IndexHandler{})
	http.Handle("/packet", &PacketHandler{Db: db})
	http.Handle("/query", &QueryHandler{Db: db})
	http.Handle("/user/summary", &UserSummaryHandler{Db: db})
}
