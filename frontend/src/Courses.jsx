import { Card, Button, Badge } from "react-bootstrap";
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import NavigationComponent from "./NavigationComponent";

function Courses() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_BACKEND_SERVICE}/courses/`)
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data: ", error));
  }, []);

  return (
    <>
      <NavigationComponent />
      <div className="Courses">
        <div className="d-flex flex-wrap">
          {data.map((item) => (
            <Card key={item._id} style={{ width: "18rem", margin: "10px" }}>
              <Card.Body>
                <Card.Title>{item.name}</Card.Title>
                <Card.Text>{item.date}</Card.Text>
                <Badge pill bg="success">
                  {item.domain}
                </Badge>
                <Card.Text>Rating: {item.rating.count}</Card.Text>
                <Link to={`/course/${item._id}`}>
                  <Button variant="primary">Audit Course</Button>
                </Link>
              </Card.Body>
            </Card>
          ))}
        </div>
      </div>
    </>
  );
}

export default Courses;
