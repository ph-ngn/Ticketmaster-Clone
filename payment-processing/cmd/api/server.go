package main

import (
	"context"
	"flag"
	"fmt"
	"github.com/andyj29/btp405_project1/tree/main/payment-processing/internal/kafkaproducer"
	"log"
	"net/http"
	"os"
	"time"
)

type config struct {
	port   int
	env    string
	stripe struct {
		secret string
		key    string
	}
}

type server struct {
	config  config
	kafka   *kafkaproducer.Producer
	infoLog *log.Logger
	errLog  *log.Logger
}

func (server *server) run() error {
	serverNode := &http.Server{
		Addr:              fmt.Sprintf(":%d", server.config.port),
		Handler:           server.routes(),
		IdleTimeout:       30 * time.Second,
		ReadTimeout:       10 * time.Second,
		ReadHeaderTimeout: 5 * time.Second,
		WriteTimeout:      5 * time.Second,
	}
	server.infoLog.Println(fmt.Sprintf("Starting API server in %s mode on port %d", server.config.env, server.config.port))
	return serverNode.ListenAndServe()
}

func main() {
	var cfg config

	flag.IntVar(&cfg.port, "port", 4001, "Server port to listen on")
	flag.StringVar(&cfg.env, "env", "development", "Application environment {development|production}")
	flag.Parse()

	cfg.stripe.key = os.Getenv("STRIPE_KEY")
	cfg.stripe.secret = os.Getenv("STRIPE_SECRET")

	infoLog := log.New(os.Stdout, "INFO\t", log.Ldate|log.Ltime)
	errLog := log.New(os.Stdout, "ERROR\t", log.Ldate|log.Ltime|log.Lshortfile)

	server := &server{
		config:  cfg,
		infoLog: infoLog,
		errLog:  errLog,
		kafka:   kafkaproducer.NewProducer(context.Background(), "tcp", "localhost:9092"),
	}
	err := server.run()
	if err != nil {
		server.errLog.Fatal(err)
	}
}
