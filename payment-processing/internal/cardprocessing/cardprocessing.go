package cardprocessing

import (
	"github.com/stripe/stripe-go/v72"
	"github.com/stripe/stripe-go/v72/paymentintent"
)

type Card struct {
	Secret string
	Key    string
}

type Transaction struct {
	TransactionStatusId int
	Amount              int
	Currency            string
	LastFour            string
	BankReturnCode      string
}

func (c *Card) Charge(orderNumber string, amount int64, currency string) (*stripe.PaymentIntent, string, error) {
	return c.createPaymentIntent(orderNumber, amount, currency)
}

func (c *Card) createPaymentIntent(orderNumber string, amount int64, currency string) (*stripe.PaymentIntent, string, error) {
	stripe.Key = c.Secret
	params := &stripe.PaymentIntentParams{
		Amount:   stripe.Int64(amount),
		Currency: stripe.String(currency),
	}
	params.AddMetadata("order_number", orderNumber)

	pi, err := paymentintent.New(params)
	if err != nil {
		msg := ""
		if stripeErr, ok := err.(*stripe.Error); ok {
			msg = cardErrorCodeWrapper(stripeErr.Code)
		}
		return nil, msg, err
	}
	return pi, "", nil
}

func cardErrorCodeWrapper(code stripe.ErrorCode) string {
	var msg = ""
	switch code {
	case stripe.ErrorCodeCardDeclined:
		msg = "Your card was declined"
	case stripe.ErrorCodeExpiredCard:
		msg = "Your card is expired"
	case stripe.ErrorCodeIncorrectCVC:
		msg = "Incorrect CVC code"
	case stripe.ErrorCodeIncorrectZip:
		msg = "Incorrect zip/postal code"
	case stripe.ErrorCodeAmountTooLarge:
		msg = "The amount is too large to charge to your card"
	case stripe.ErrorCodeAmountTooSmall:
		msg = "The amount is too small to charge to your card"
	case stripe.ErrorCodeBalanceInsufficient:
		msg = "Insufficient balance"
	case stripe.ErrorCodePostalCodeInvalid:
		msg = "Invalid postal code"
	default:
		msg = "Your card is declined. Try a new card"
	}
	return msg
}
