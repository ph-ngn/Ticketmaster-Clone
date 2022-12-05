import Header from './components/Header'
import {Container} from 'react-bootstrap'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"
import './App.css'
import HomePage from "./pages/HomePage"
import SignupPage from "./pages/SignupPage"
import LoginPage from "./pages/LoginPage"
import CheckoutPage from "./pages/CheckoutPage"
import PaymentCompletion from "./pages/PaymentCompletion"
import OrderPage from "./pages/OrderPage";
import {useEffect, useState} from "react";
import AuthService from "./services/auth.service";

const App = () => {

    const [isLoggedIn, setIsLoggedIn] = useState(false)

    useEffect(()=> {
        const user = AuthService.getCurrentUser()
        if (user && user.token) {
            setIsLoggedIn(true)
        }
    },[])

    return (
        <Router>
            <Header isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}/>
            <main>
                <Container>
                    <Routes>
                        <Route path="/" element={<HomePage isLoggedIn={isLoggedIn} />}/>
                        <Route path="/signup" element={<SignupPage/>}/>
                        <Route path="/login" element={<LoginPage setIsLoggedIn={setIsLoggedIn} />}/>
                        <Route path="/checkout" element={<CheckoutPage />}/>
                        <Route path="/payment-completion" element={<PaymentCompletion/>}/>
                        <Route path="/order" element={<OrderPage />}/>
                    </Routes>
                    <div className="wave"></div>
                    <div className="wave"></div>
                    <div className="wave"></div>
                </Container>
            </main>

        </Router>
    )
}

export default App