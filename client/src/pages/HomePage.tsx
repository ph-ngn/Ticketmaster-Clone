import {useEffect, useState} from "react";
import AuthService from "../services/auth.service";
import jwt_decode from "jwt-decode";
import Concert from "../components/Concert"
import Carousel from "react-bootstrap/Carousel";
import {Container, Image, Col, Row} from "react-bootstrap";
import Marquee from "react-fast-marquee";
import ConsumerService from "../services/consumer.service"
import ReactPlayer from "react-player";

type Props = {
    isLoggedIn: boolean
}

type concert = {
    concert_number: string,
    date: string
    name: string
    promoter: string
    seat_offering: {}
    venue: string
    pricing: {}
    posters_urls: [string]
}

const HomePage = (props: Props) => {


    const [username, setUsername] = useState('')
    const [accountType, setAccountType] = useState('')
    const [concerts, setConcerts] = useState<concert[]>([])

    useEffect(() => {
        const user = AuthService.getCurrentUser()
        if(user && user.token) {
            const decoded: any = jwt_decode(user.token)
            setUsername(decoded.sub)
            setAccountType(decoded.info)
        }
        else{
            setUsername('')
            setAccountType('')
        }
        ConsumerService.getAllConcerts(0, 5)
            .then(response => {
                setConcerts(response.data)
            })
    }, [props.isLoggedIn])

    return (
        <div>
            {username == "" && (
                <div>
                    <Container className="py-2 mb-3">
                        <Row className="justify-content-md-center">
                            <Col md={"auto"}>
                                <Marquee pauseOnHover={true} speed={50} gradientWidth={0} style={{backgroundColor: 'rgba(242,242,242,0.8)'}}><h5>Upcoming Events 🤘</h5></Marquee>
                            </Col>
                        </Row>
                    </Container>
                    
                <Carousel interval={3000}>
                        {concerts.map(concert => {

                            return (
                                <Carousel.Item>
                                    {concert.posters_urls[0].endsWith("mp4") ? <ReactPlayer className="d-block w-100" height={700} url={concert.posters_urls[0]} controls = {true} /> : <Image className="d-block w-100" height={700} src={concert.posters_urls[0]}></Image>}
                                </Carousel.Item>
                        
                            )
                        })}
                </Carousel>
            
                </div>)}
            {accountType=='consumer'? (
                <div>
                    <Container className="py-2">
                    <h4>Welcome {username && accountType ?  username :null}</h4>
                    </Container>

                    <Concert />
                </div>
            ) : null
            }
        </div>
    )
}

export default HomePage