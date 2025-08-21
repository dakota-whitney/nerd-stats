"use client";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Container, Navbar, Nav } from 'react-bootstrap';

ChartJS.register(ArcElement, Tooltip, Legend);

export default function NavBar({navLinks}) {
  return (
    <Navbar collapseOnSelect expand="md" className="bg-body-tertiary">
      <Container fluid>
        <Navbar.Brand href="/">NerdStats</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto">
          {navLinks.map(({name, href}, i) => {
            return (
              <Nav.Link key={i} href={href}>
                {name}
              </Nav.Link>
            );
          })}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};