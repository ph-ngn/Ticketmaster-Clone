package kafkaproducer

import (
	"context"
	"encoding/json"
	"github.com/segmentio/kafka-go"
)

type Producer struct {
	context  context.Context
	protocol string
	address  string
}

func NewProducer(ctx context.Context, protocol string, address string) *Producer {
	return &Producer{
		context:  ctx,
		protocol: protocol,
		address:  address,
	}
}

func (producer *Producer) WriteMessages(topic string, partition int, payloads ...interface{}) (err error) {
	conn, err := kafka.DialLeader(producer.context, producer.protocol, producer.address, topic, partition)
	if err != nil {
		return err
	}
	encodedMessages := make([]kafka.Message, len(payloads))
	for index, payload := range payloads {
		payloadBytes, err := json.Marshal(payload)
		if err != nil {
			return err
		}
		encodedMessages[index] = kafka.Message{Value: payloadBytes}
	}
	_, err = conn.WriteMessages(encodedMessages...)
	if err != nil {
		return err
	}
	if err := conn.Close(); err != nil {
		return err
	}
	return nil
}
