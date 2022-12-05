import {Button, Form} from "react-bootstrap";
import FormContainer from "../components/FormContainer"
import {SyntheticEvent, useState} from "react"
import {useNavigate} from "react-router-dom"
import {Alert} from "react-bootstrap"
import AuthService from "../services/auth.service"

const SignupPage = () => {
    const [username, setUsername] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [accountType, setAccountType] = useState('')
    const [secretKey, setSecretKey] = useState('')
    const [error, setError] = useState('')

    let navigate = useNavigate()
    const submitHandler = async (e: SyntheticEvent) => {
        e.preventDefault()

             AuthService.register({
                username: username,
                email: email,
                password: password,
                account_type: accountType,
                secret_key: secretKey
            })
            .then(_ => {
                navigate('/login')
            })
                .catch(error => setError(error.response.data.message))
    }

    return (
        <FormContainer>
            <h1>Signup</h1>
            <Form onSubmit={submitHandler}>
                <Form.Group className="my-3" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control type="username" placeholder="Enter your username " value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    />
                </Form.Group>
                <Form.Group className="my-3" controlId="email">
                    <Form.Label>Email</Form.Label>
                    <Form.Control type="email" placeholder="Enter your email" value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    />
                </Form.Group>
                <Form.Group className="my-3" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter your password" value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    />
                </Form.Group>
                <Form.Group className="my-3" controlId="account_type">
                    <Form.Label>Account Type</Form.Label>
                    <Form.Select value={accountType} onChange={(e) => setAccountType(e.target.value)}>
                        <option>Choose your account type</option>
                        <option value="consumer">Consumer</option>
                        <option value="promoter">Promoter</option>
                        <option value="admin">Admin</option>
                    </Form.Select>
                </Form.Group>
                {accountType === 'admin' ?
                    <Form.Group className="my-3" controlId="secret_key">
                        <Form.Label>Secret Key</Form.Label>
                        <Form.Control type="secret_key" placeholder="Enter you secret key"
                                      value={secretKey}
                                      onChange={(e) => setSecretKey(e.target.value)}
                        />
                    </Form.Group> : null
                }

                <Button variant="primary" type="submit" className="my-3">
                    Submit
                </Button>
            </Form>
            {error ? <Alert variant="danger" >{error}</Alert> : null }
        </FormContainer>
    )
}

export default SignupPage