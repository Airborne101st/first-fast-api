import React from "react";
import { Container, Row, Col, Button } from "react-bootstrap";
import { Link } from "react-router-dom";

const Index = () => {
  return (
    <Container className="mt-5">
      <Row className="justify-content-md-center">
        <Col md="6" className="text-center">
          <h1>Welcome to My App</h1>
          <p>Please choose an option below to proceed.</p>
          <Link to="/login">
            <Button variant="primary" className="m-2">
              Login
            </Button>
          </Link>
          <Link to="/register">
            <Button variant="secondary" className="m-2">
              Register
            </Button>
          </Link>
        </Col>
      </Row>
    </Container>
  );
};

export default Index;
