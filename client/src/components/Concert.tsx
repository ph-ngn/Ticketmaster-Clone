import Button from 'react-bootstrap/Button'
import Pagination from 'react-bootstrap/Pagination';
import {useEffect, useState, useRef, SyntheticEvent} from "react";
import ConsumerService from "../services/consumer.service";
import {useNavigate} from "react-router-dom";
import {Container, Image, Col, Carousel} from "react-bootstrap";
import Row from 'react-bootstrap/Row';
import {Form} from "react-bootstrap";
import {ListContainer, ListRow} from "@ticketmaster/aurora";
import {Modal} from "react-bootstrap";
import ReactPlayer from "react-player";


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

const Concert = () => {
    const navigate = useNavigate()
    const [data, setData] = useState<concert[]>([])
    const [search, setSearch] = useState("")
    const [active, setActive] = useState(1)
    const [show, setShow] = useState(false)
    const handleClose = () => setShow(false)
    const handleShow = () => setShow(true)

    let items = []
    for (let number = 1; number <= 4; number++) {
        items.push(
            <Pagination.Item key={number} active={number === active} onClick={() => pagination(number, 12)}>
                {number}
            </Pagination.Item>,
        );
    }
    const pagination = (page_num: number, limit: number) => {
        setActive(page_num)
        ConsumerService.getAllConcerts(page_num, limit)
            .then(response => {
                setData(response.data)
            })
    }

    const handleSearch = async (e: SyntheticEvent) => {
        e.preventDefault()
        ConsumerService.searchConcerts(search)
            .then(response => {
                setData(response.data)
                console.log(response.data)
            })
    }

    useEffect(() => {
        ConsumerService.getAllConcerts(0, 12)
            .then(response => {
                setData(response.data)
            })
    }, [])

    return (
        <div>
            <Container className="py-2">
                <Form className="d-flex w-25" onSubmit={handleSearch}>
                    <Form.Control
                        type="search"
                        placeholder="Search concerts"
                        className="me-2"
                        aria-label="Search"
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                    />
                    <Button type={"submit"}>Search</Button>
                </Form>
            </Container>
            <Container className="py-4">
                <ListContainer id={"modal-root"}>
                    {
                        data.map((concert, index) =>{
                            let [day, month, date] = new Date(concert.date).toDateString().split(" ")
                            let label = ""
                            let total = 0
                            let labelVariant = "alert"
                            const seatOffering: {[index: string]: number} = concert.seat_offering
                            for (const attr in seatOffering){
                                total += seatOffering[attr]
                            }
                            if (total < 10 && total > 0) label = "low in stock"
                            else if (total === 0) label = "sold out"
                            else {
                                label = "in stock"
                                labelVariant = "positive"
                            }
                            return (
                                <>
                                <ListRow
                                    rowItem={{
                                        title: concert.name,
                                        subTitle: `${concert.venue} - Toronto, ON`,
                                        dateTitle: `${month} ${date}`,
                                        dateSubTitle: `${day} 8:00pm`,
                                        buttonText: "See Tickets",
                                        variant: "standard",
                                        dateColor: "#C56BFF",
                                        label: label,
                                        labelVariant: labelVariant,
                                        onClick: ()=>{navigate('/order', {
                                            state: {
                                                concert_number: concert.concert_number,
                                                seat_offering: concert.seat_offering,
                                                pricing: concert.pricing
                                            }

                                        })}



                                    }}
                                    index={index}
                                    onOverflowClick={()=>{
                                    }}
                                    onExpandItem={(index: number)=>{
                                        setShow(true)
                                    }}
                                >
                                </ListRow>
                                    <Modal show={show} size="lg"
                                           aria-labelledby="contained-modal-title-vcenter"
                                           centered onHide={handleClose}>
                                        <Modal.Header closeButton>
                                            <Modal.Title>{concert.name}</Modal.Title>
                                        </Modal.Header>
                                        <Modal.Body>
                                            <Carousel>
                                               {
                                                concert.posters_urls.map(url => {
                                                    return (
                                                        <Carousel.Item>
                                                            {url.endsWith("mp4") ? <ReactPlayer className="d-block w-100" height={500} url={url} controls = {true} /> : <Image src={url} className={"d-block w-100"} height={450}></Image>}
                                                        </Carousel.Item>
                                                    )
                                                })
                                               }
                                            </Carousel>
                                        </Modal.Body>
                                        <Modal.Footer>
                                            <Button  onClick={handleClose}>
                                                Close
                                            </Button>
                                        </Modal.Footer>
                                    </Modal>
                                </>
                            )}
                        )
                    }
                </ListContainer>
                
            </Container>
            <Container>
            <Row className="justify-content-md-center">
                <Col md={"auto"}>
                    <Pagination>
                        {items}
                    </Pagination>
                </Col>
            </Row>
            </Container>
        </div>
)
}

export default Concert