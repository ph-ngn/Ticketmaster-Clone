package main

import (
	"encoding/json"
	"github.com/andyj29/btp405_project1/tree/main/payment-processing/internal/cardprocessing"
	"net/http"
)

type paymentPayload struct {
	OrderNumber string         `json:"order_number"`
	Amount      int64          `json:"amount"`
	Currency    string         `json:"currency"`
	OrderItems  map[string]int `json:"order_items"`
}

type paymentResponse struct {
	Success      bool   `json:"success"`
	Message      string `json:"message"`
	ClientSecret string `json:"client_secret,omitempty"`
}

func (server *server) GetPaymentIntent(w http.ResponseWriter, r *http.Request) {
	defer func() {
		if r := recover(); r != nil {
			server.infoLog.Println("Recover in f", r)
		}
	}()
	var payload paymentPayload
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		server.errLog.Println(err)
		panic(err)
	}
	card := cardprocessing.Card{
		Secret: server.config.stripe.secret,
		Key:    server.config.stripe.key,
	}
	pi, msg, err := card.Charge(payload.OrderNumber, payload.Amount, payload.Currency)
	if err != nil {
		paymentRes := paymentResponse{
			Success: false,
			Message: msg,
		}
		res, err := json.MarshalIndent(paymentRes, "", "\t")
		if err != nil {
			server.errLog.Println(err)
			panic(err)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusBadRequest)
		w.Write(res)
	} else {
		paymentRes := paymentResponse{
			Success:      true,
			Message:      string(pi.Status),
			ClientSecret: pi.ClientSecret,
		}
		res, err := json.MarshalIndent(paymentRes, "", "\t")
		if err != nil {
			server.errLog.Println(err)
			panic(err)
		}
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		w.Write(res)
		// Simulate successful payment event webhook because stripe requires webhooks to be publicly available
		err = server.kafka.WriteMessages("completedOrder", 0, payload)
		server.infoLog.Println("Hit the api")
		if err != nil {
			server.errLog.Println(err)
		}
	}
}
