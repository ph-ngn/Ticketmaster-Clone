import {SyntheticEvent, useState} from "react";
import {useStripe, useElements, PaymentElement} from '@stripe/react-stripe-js';
import {Alert, Button, Spinner} from "react-bootstrap";

const CheckoutForm = () => {
    const stripe = useStripe()
    const elements = useElements()

    const [errorMessage, setErrorMessage] = useState<string>()
    const [spinner, setSpinner] = useState(false)
    const handleSubmit = async (event: SyntheticEvent) => {
        event.preventDefault()
        setSpinner(true)
        if (!stripe || !elements) {
            return
        }
        const {error} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: "http://localhost:3000/payment-completion"
            },
        })
        if (error) {
            setErrorMessage(error.message)
        }
        setSpinner(false)

    }
    return (
        <form onSubmit={handleSubmit}>
            <PaymentElement className={"mb-2"}/>
            <Button disabled={!stripe} variant="primary" type="submit" className="my-3">
                Submit
            </Button>
            <hr/>
            {spinner && <Spinner animation="border"></Spinner>}
            {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
        </form>
    )
}
export default CheckoutForm;