import React from 'react'
import {Container, Row, Col} from 'react-bootstrap'

type props = {
    children: React.ReactNode
}
const FormContainer = (props: props) => {
    return (
        <Container className="py-3">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    {props.children}
                </Col>
            </Row>
        </Container>
    )
}

export default FormContainer