"use client"
import { useState, useEffect, useRef } from 'react';
import { Spinner, Container } from 'react-bootstrap';
import DataTable from 'react-data-table-component';
import { RDTExpander, RDTFilter } from '../datatable';
import { Pie } from 'react-chartjs-2';
// import { RDTPieChart } from '../chart';
import { titleCase } from '../functions';

const columns = [
    {
        name: "Name",
        originalName: "name",
        selector: row => row.name,
        width: "350px"
    },
    {
        name: "Frame",
        originalName: "frameType",
        selector: row => row.frameType,
        format: row => titleCase(row.frameType),
        width: "100px",
        sortable: true,
        conditionalCellStyles: [
            {
                when: row => row.frameType == "normal",
                style: {backgroundColor: "Tan"}
            },
            {
                when: row => row.frameType == "effect",
                style: {backgroundColor: "Peru"}
            },
            {
                when: row => row.frameType == "ritual",
                style: {backgroundColor: "DarkBlue"}
            },
            {
                when: row => row.frameType == "fusion",
                style: {backgroundColor: "RebeccaPurple"}
            },
            {
                when: row => row.frameType == "synchro",
                style: {backgroundColor: "Azure", color: "black"}
            },
            {
                when: row => row.frameType == "xyz",
                style: {backgroundColor: "Black"}
            },
            {
                when: row => row.frameType == "link",
                style: {backgroundColor: "MediumBlue"}
            },
            {
                when: row => row.frameType.includes("pendulum"),
                style: {backgroundColor: "Aquamarine"}
            },
            {
                when: row => row.frameType == "spell",
                style: {backgroundColor: "MediumSeaGreen"}
            },
            {
                when: row => row.frameType == "trap",
                style: {backgroundColor: "DarkMagenta"}
            }
        ]
    },
    {
        name: "Type",
        originalName: "humanReadableCardType",
        selector: row => row.humanReadableCardType,
        width: "200px",
        sortable: true
    },
    {
        name: "Race",
        originalName: "race",
        selector: row => row.race,
        width: "200px",
        sortable: true
    },
    {
        name: "Description",
        originalName: "desc",
        selector: row => row.desc,
        omit: true
    }
];

export default function YuGiOh(){
    const cardsRef = useRef([]);

    const [cards, setCards] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selected, setSelected] = useState([]);

    const renderPie = () => {
        if(!selected.length) return <></>
        const {originalName, conditionalCellStyles: cellStyles} = columns[1];

        const selectedFrames = selected.map(row => {
            let frame = row[originalName];
            if(frame.includes("pendulum")) frame = "pendulum";
            return frame;
        });

        const frameCounts = [...new Set(selectedFrames)].map(label => {
            const {length} = selectedFrames.filter(frame => frame === label);
            const {style: {backgroundColor}} = cellStyles.find(style => {
                const when = style.when.toString();
                return when.includes(label);
            });
            return {
                label: label,
                count: length,
                bg: backgroundColor
            };
        });

        const pieData = {
            labels: frameCounts.map(({label}) => label),
            datasets: [{
                label: "",
                data: frameCounts.map(({count}) => count),
                backgroundColor: frameCounts.map(({bg}) => bg)
            }]
        };

        const pieStyle = {
            display: "flex",
            flexFlow: "column nowrap",
            justifyContent: "center",
            alignItems: "center",
        };

        return (
            <Container style={pieStyle}>
                <Pie data={pieData}/>
            </Container>
        );
    };

    useEffect(() => {
        fetch("https://db.ygoprodeck.com/api/v7/cardinfo.php").
        then(res => res.json()).
        then(({data}) => {
            data = data.filter(card => !card.frameType.match(/token|skill/));
            cardsRef.current = data;
            setCards(data);
            setLoading(false);
        });
    }, []);

    return (
        <>
            <DataTable
                title="Yu-Gi-Oh!"
                columns={columns}
                data={cards}
                theme="dark"
                persistTableHead
                progressPending={loading}
                progressComponent={<Spinner />}
                subHeader
                subHeaderComponent={
                    <RDTFilter
                        columns={columns}
                        dataRef={cardsRef}
                        setData={setCards}
                    />
                }
                expandableRows
                expandableRowsComponent={RDTExpander}
                expandableRowsComponentProps={{column: "desc"}}
                selectableRows
                noContextMenu
                onSelectedRowsChange={({selectedRows}) => setSelected(selectedRows)}
                pagination
            />
            {renderPie()}
        </>
    );
};