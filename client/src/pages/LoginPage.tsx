import {SyntheticEvent, useState} from "react"
import {Form, Button, Alert} from "react-bootstrap"
import FormContainer from "../components/FormContainer"
import {useNavigate} from "react-router-dom"
import AuthService from "../services/auth.service"

type Props = {
setIsLoggedIn: (isLoggedIn: boolean) => void
}

const LoginPage = (props: Props) => {

    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')

    let navigate = useNavigate()
    const submitHandler = async (e: SyntheticEvent) => {
        e.preventDefault()
        AuthService.login({
            email,
            password
        }).then(_ => {
            props.setIsLoggedIn(true)
            navigate('/')
        })
            .catch(error => setError(error.response.data.message))
        AuthService.getCurrentUser()


    }

    return (
        <FormContainer>
            <h1>Login</h1>
        <Form onSubmit={submitHandler}>
            <Form.Group className="my-3" controlId="email">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" placeholder="Enter your email" value={email}
                onChange={e => setEmail(e.target.value)}
                />
            </Form.Group>

            <Form.Group className="my-3" controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Enter your password" value={password}
                onChange={e => setPassword(e.target.value)}
                />
            </Form.Group>
            <Button variant="primary" type="submit" className="my-3">
                Submit
            </Button>
        </Form>
            {error ? <Alert variant="danger" >{error}</Alert> : null }
        </FormContainer>
    )
}

export default LoginPage