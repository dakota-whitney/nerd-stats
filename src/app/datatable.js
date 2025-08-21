import { useState } from 'react';
import { Form, Container, Row, Col } from 'react-bootstrap';

export const RDTExpander = ({data, column}) => {
    const expanderStyle = {
        fontSize: "12.5px",
        fontStyle: "italic",
        padding: "10px"
    };

    return <div style={expanderStyle}>{data[column]}</div>
};

export const RDTFilter = ({columns, dataRef, setData})  => {
    const [searchColumn, setSearchColumn] = useState(columns[0].originalName);

    const selectSearchColumn = e => {
        const column = columns.find(col => col.name == e.target.value);
        setSearchColumn(column.originalName);
    };

    const filterColumn = e => {
        const {value: searchText} = e.target;
        if(!searchText) return setData(dataRef.current);

        const filteredData = dataRef.current.filter(row => {
            const cellLower = row[searchColumn].toLowerCase();
            const textLower = searchText.toLowerCase();
            return cellLower.includes(textLower);
        });

        setData(filteredData);
    };

    return (
        <Container fluid>
        <Row>
        <Col md={2}>
            <Form.Select
                aria-label="Column select"
                onChange={selectSearchColumn}
                size="sm"
            >
                {columns.map(({name}, i) => {
                    return (
                        <option key={i} value={name}>
                        {name}
                        </option>
                    )
                })}
            </Form.Select>
        </Col>
        <Col md={10}>
            <Form.Control
                aria-label="Text search"
                onChange={filterColumn}
                size="sm"
            />
        </Col>
        </Row>
        </Container>
    );
};