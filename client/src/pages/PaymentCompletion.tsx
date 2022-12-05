import {Button} from "react-bootstrap";
import {useNavigate} from "react-router-dom";

const PaymentCompletion = () => {
    const navigate = useNavigate()
    return (
        <>
            <h2>Thank you! 🎉 We've sent the order receipt and tickets to your email</h2>
            <Button type={"button"} onClick={()=> {navigate('/')}} className="my-3">Done</Button>
        </>
    )
}

export default PaymentCompletion