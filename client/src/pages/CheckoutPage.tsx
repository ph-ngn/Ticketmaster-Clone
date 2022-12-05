import {Elements} from '@stripe/react-stripe-js';
import {loadStripe} from '@stripe/stripe-js';
import CheckoutForm from '../components/CheckoutForm'
import {useState, useEffect} from "react";
import {useLocation} from "react-router-dom";

const stripePromise = loadStripe('pk_test_51KNx2ZABOs8B5Mq7wGfC3FIGfkHoRLD014Yu8nC0RhU86pRj005J2wRItUHp1ZrRn3wt7PYk2spOHZKRV5WCr8ek00kjblBCca')

const CheckoutPage = () => {
   const [clientSecret, setClientSecret] = useState("")
    const location = useLocation()
    useEffect(() => {
        fetch("http://127.0.0.1:4001/api/payment-intent", {
            method: "POST",
            body: JSON.stringify({
                "order_number": location.state.order_number,
                "amount": location.state.amount * 100,
                "currency": location.state.currency,
                "order_items": location.state.order_items
            })
        }).then(async (r) => {
            const response = await r.json()
            setClientSecret(response.client_secret)
        })
    }, [])


    return (
        <>
            {stripePromise && clientSecret && (
                <Elements stripe={stripePromise} options={{clientSecret}}>
                    <h2>Order Total: {location.state.amount} {location.state.currency}</h2>
                    <hr/>
                    <CheckoutForm />
                </Elements>
            )}

        </>
    )
}

export default CheckoutPage