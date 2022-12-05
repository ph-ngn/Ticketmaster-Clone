import {Navbar, Nav, Container, Image, Ratio} from 'react-bootstrap'
import {SyntheticEvent} from "react";
import AuthService from "../services/auth.service";
import {useNavigate} from "react-router-dom";

type Props = {
    isLoggedIn: boolean
    setIsLoggedIn: (isLoggedIn: boolean) => void
}
const Header = (props: Props) => {
    const navigate = useNavigate()
    const logoutHandler = (e: SyntheticEvent) => {
        e.preventDefault()
        AuthService.logout()
        props.setIsLoggedIn(false   )
        navigate('/')
    }

    return (
        <Navbar style={{position:"sticky", top:0, zIndex:1}} bg="light" variant="light" expand="lg" collapseOnSelect>
      <Container>

        <Navbar.Brand href="/">
            <Image src={"https://img.icons8.com/fluency/48/null/park-concert-shell.png"}></Image> Surge
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
            {props.isLoggedIn ? (
                <Nav className="ms-auto">
                    <Nav.Link onClick={logoutHandler}>Logout</Nav.Link>
                </Nav>)
                : (<Nav className="ms-auto">
                <Nav.Link href="/signup">Sign Up</Nav.Link>
                <Nav.Link href="/login">Login</Nav.Link>
            </Nav>)}
        </Navbar.Collapse>
      </Container>
    </Navbar>
    )
}

export default Header