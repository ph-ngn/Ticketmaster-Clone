import FormContainer from "../components/FormContainer";
import {Form} from "react-bootstrap";
import {SyntheticEvent, useState} from "react";
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row'
import {Button} from "react-bootstrap";
import ConsumerService from "../services/consumer.service";
import {useLocation, useNavigate} from "react-router-dom";
import AuthService from "../services/auth.service";

type OrderItem = {
    seat_type: string
    quantity: number
}

const OrderPage = () => {
    const navigate = useNavigate()
    const location = useLocation()
    const [orderItems, setOrderItems] = useState<OrderItem[]>(Object.keys(location.state.seat_offering).map(key => ({seat_type: key, quantity: 0})))

    const updateOrderItem = (seat_type: string, value: number, index: number) => {
        let newOrderItems = [...orderItems]
        newOrderItems[index].seat_type = seat_type
        newOrderItems[index].quantity = value
        setOrderItems(newOrderItems)
    }

    const submitHandler = (e: SyntheticEvent) => {
        e.preventDefault()
        let items: any = {}
        orderItems.map(order_item => {
            items[order_item.seat_type] =  order_item.quantity
        })
        const user = AuthService.getCurrentUser()
        if (user && user.token){

            ConsumerService.place_draft_order(user.token,{
                concert: location.state.concert_number,
                currency: "CAD",
                order_items: items
            }).then(response => {
                navigate('/checkout', {
                    state: {
                        order_number: response.data.order_number,
                        amount: response.data.total,
                        currency: response.data.currency,
                        order_items: items
                    }
                })
            }).catch()}
    }
    return (
        <FormContainer>
            <Form onSubmit={submitHandler}>
                <h4>Select Tickets</h4>
                <hr/>
                    {

            Object.keys(location.state.seat_offering).map((key, index) => {
                return (
                    <Form.Group className="mt-2 mb-2" controlId="username">
                        <Form.Label>{key.toUpperCase()} - Ticket price: {location.state.pricing[key]} CAD</Form.Label>
                        {location.state.seat_offering[key] > 0 ? <p>Available: {location.state.seat_offering[key]}</p>: <p>Sold out</p>}
                        <Row>
                            <Col>
                            <Form.Range value={orderItems[index].quantity} max={location.state.seat_offering[key]} onChange={(e) => {updateOrderItem(key, Number(e.target.value), index)}}></Form.Range>
                            </Col>
                        <Col xs="2">
                            <Form.Control value={orderItems[index].quantity} onChange={(e) => {updateOrderItem(key, Number(e.target.value), index)}}/>
                        </Col>
                        </Row>

                    </Form.Group>
                )})
        }
                <Button type="submit">Check out</Button>&nbsp;&nbsp;&nbsp;
            </Form>
        </FormContainer>
    )
}

export default OrderPage