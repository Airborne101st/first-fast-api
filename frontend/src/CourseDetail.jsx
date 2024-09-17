import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Card, Badge, Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faThumbsUp } from "@fortawesome/free-solid-svg-icons";
import NavigationComponent from "./NavigationComponent";

function CourseDetail() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [likes, setLikes] = useState(0);

  const handleLike = () => {
    setLikes(likes + 1);
  };

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/courses/${courseId}`)
      .then((response) => response.json())
      .then((data) => setCourse(data))
      .catch((error) =>
        console.error("Error fetching course details: ", error)
      );
  }, [courseId]);

  if (!course) {
    return <div>Loading...</div>;
  }

  return (
    <>
      <NavigationComponent />
      <div className="CourseDetail">
        <Card style={{ width: "60rem" }}>
          <Card.Body>
            <Card.Title>{course.name}</Card.Title>
            <Button variant="primary" onClick={handleLike}>
              <FontAwesomeIcon icon={faThumbsUp} />
            </Button>
            <Card.Text>{course.date}</Card.Text>
            <Badge pill bg="secondary">
              {course.domain}
            </Badge>
            <Card.Text>{course.description}</Card.Text>
            <div className="container">
              <h2>Coursework</h2>
              <div className="row">
                {course.chapters.map((item) => (
                  <div className="col-12 mb-3" key={item.name}>
                    <div className="card custom-card">
                      <div className="card-body">
                        <h5 className="card-title">{item.name}</h5>
                        <p className="card-text">{item.text}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card.Body>
        </Card>
      </div>
    </>
  );
}

export default CourseDetail;
