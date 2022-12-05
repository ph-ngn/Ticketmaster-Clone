import axios from 'axios'
import AuthService from "./auth.service";

const BASE_URL = 'http://127.0.0.1:5000'

type OrderData = {
    concert: string
    currency: string
    order_items: {}
}

class ConsumerService {
    getAllConcerts(page: number = 0, limit: number = 0) {
        return axios.get(`${BASE_URL}/concerts?page=${page}&limit=${limit}`)
    }

    searchConcerts(search: string) {
        return axios.get(`${BASE_URL}/concerts?search=${search}`)
    }

    place_draft_order(token: string,order: OrderData) {
        return axios.post(BASE_URL+'/orders',
            order,
            {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                }
            }
            )
    }

}

export default new ConsumerService()