import axios from "axios"

const BASE_URL = "http://127.0.0.1:5000"

type RegisterData = {
    username: string
    email: string
    password: string
    account_type: string
    secret_key: string
}

type LoginData = {
    email: string
    password: string
}

const headers = {
    headers: {
        'Content-Type': 'application/json',
    }
}

class AuthService {
    register(registerData: RegisterData) {
        return axios.post(BASE_URL+'/signup',
            registerData,
            headers)
    }

    login(loginData: LoginData) {
        return axios.post(BASE_URL+'/login',
            loginData,
            headers)
            .then(response => {
                if(response.data.token) {
                    localStorage.setItem("user", JSON.stringify(response.data))
                }
            })
    }

    logout() {
        localStorage.removeItem('user')
    }

    getCurrentUser() {
        const user = localStorage.getItem('user')
        return JSON.parse(user!)
    }
}

export default new AuthService()