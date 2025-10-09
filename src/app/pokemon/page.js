"use client";
import { useState, useEffect, useRef } from 'react';
import Pokedex from 'pokedex-promise-v2';
import { Container, Spinner, OverlayTrigger, Popover } from 'react-bootstrap';
import DataTable from 'react-data-table-component';
import { Pie } from 'react-chartjs-2';
import { RDTFilter } from '../datatable';
import { titleCase } from '../functions';

const movesPopover = moves => {
    const movesStyle = {
        overflow: "scroll",
        scrollbarWidth: "none",
        height: "150px"
    };

    return (
        <Popover style={movesStyle}>
        <Popover.Body>
            <ul>
            {moves.map((move, i) => <li key={i}>{move}</li>)}
            </ul>
            </Popover.Body>
        </Popover>
    );
};

const columns = [
    {
        name: "Name",
        originalName: "name",
        selector: row => row.name,
        format: row => titleCase(row.name),
        width: "350px"
    },
    {
        name: "Type",
        originalName: "type",
        selector: row => row.type,
        width: "200px",
        sortable: true,
        conditionalCellStyles: [
            {
                when: row => row.type.split(" / ")[0] == "Fire",
                style: {backgroundColor: "Chocolate"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Grass",
                style: {backgroundColor: "ForestGreen"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Water",
                style: {backgroundColor: "RoyalBlue"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Electric",
                style: {backgroundColor: "Yellow", color: "black"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Normal",
                style: {backgroundColor: "Gray"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Flying",
                style: {backgroundColor: "LightSlateGray"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Ground",
                style: {backgroundColor: "DarkGoldenRod"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Poison",
                style: {backgroundColor: "Purple"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Bug",
                style: {backgroundColor: "OliveDrab"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Fighting",
                style: {backgroundColor: "OrangeRed"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Dark",
                style: {backgroundColor: "black", color: "white"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Ice",
                style: {backgroundColor: "LightSkyBlue"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Rock",
                style: {backgroundColor: "SaddleBrown"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Psychic",
                style: {backgroundColor: "PaleVioletRed"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Ghost",
                style: {backgroundColor: "BlueViolet"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Steel",
                style: {backgroundColor: "SlateGrey"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Dragon",
                style: {backgroundColor: "BlueViolet"}
            },
            {
                when: row => row.type.split(" / ")[0] == "Fairy",
                style: {backgroundColor: "Violet"}
            }
        ]
    },
    {
        name: "Abilities",
        originalName: "abilities",
        selector: row => row.abilities,
        width: "200px",
        sortable: true
    },
    {
        name: "Moves",
        originalName: "moves",
        cell: row => (
            <OverlayTrigger
                trigger="click"
                placement="right"
                overlay={movesPopover(row.moves)}
            >
            <span style={{cursor: "pointer"}}>...</span>
            </OverlayTrigger>
        )
    }
];

const P = new Pokedex();

const getPokeData = pokemon => pokemon.map(p => {
    let {types, abilities, moves} = p;

    types = types.map(({type}) => titleCase(type.name));
    abilities =  abilities.map(({ability}) => titleCase(ability.name));

    return {
        name: p.name,
        type: types.join(" / "),
        abilities: abilities.join(" / "),
        moves: moves.map(({move}) => titleCase(move.name))
    };
});

export default function Pokemon(){
    const pokeRef = useRef([]);

    const [pokemon, setPokemon] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selected, setSelected] = useState([]);

    useEffect(() => {
        P.getPokemonsList()
        .then(({results}) => results.map(({name}) => name))
        .then(pkmn => P.getPokemonByName(pkmn))
        .then(pkmn => getPokeData(pkmn))
        .then(pkmn => {
            pokeRef.current = pkmn;
            setPokemon(pkmn);
            setLoading(false);
        });
    }, []);

    const renderPie = () => {
        if(!selected.length) return <></>;

        const {originalName, conditionalCellStyles: cellStyles} = columns[1];
        const selectedTypes = selected.map(row => row[originalName]);

        const typeCounts = [...new Set(selectedTypes)].map(label => {
            console.log(label);
            const {length} = selectedTypes.filter(pType => pType === label);
            const {style: {backgroundColor}} = cellStyles.find(style => {
                const [pType] = label.split(" / ");
                const when = style.when.toString();
                return when.includes(pType);
            });
            return {
                label: label,
                count: length,
                bg: backgroundColor
            };
        });

        const pieData = {
            labels: typeCounts.map(({label}) => label),
            datasets: [{
                label: "",
                data: typeCounts.map(({count}) => count),
                backgroundColor: typeCounts.map(({bg}) => bg)
            }]
        };

        const mq = window.matchMedia("(min-width: 768px)");

        const pieOptions = {
            aspectRatio: mq.matches ? 2 : 1
        };

        return (
            <Container>
                <Pie data={pieData} options={pieOptions}/>
            </Container>
        );
    };

    return (
        <>
            <DataTable
                title="Pokémon"
                columns={columns}
                data={pokemon}
                theme="dark"
                persistTableHead
                progressPending={loading}
                progressComponent={<Spinner />}
                subHeader
                subHeaderComponent={
                    <RDTFilter
                        columns={columns}
                        dataRef={pokeRef}
                        setData={setPokemon}
                    />
                }
                selectableRows
                noContextMenu
                onSelectedRowsChange={({selectedRows}) => setSelected(selectedRows)}
                pagination
            />
            {renderPie()}
        </>
    );
};