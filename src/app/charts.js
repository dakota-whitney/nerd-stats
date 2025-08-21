"use client";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

// const getCounts = (selected, column) => {
//     const {originalName, conditionalCellStyles: cellStyles} = column;
//     const rowVals = selected.map(row => row[originalName]);

//     const colVals = [...new Set(rowVals)];
//     const colCounts = new Map();

//     for(const colVal in colVals){
//         const {length} = rowVals.filter(val => val === colVal);
//         const {style: {backgroundColor}} = cellStyles.find(style => JSON.stringify(style.when).includes(colVal));
//         colCounts.set(colVal, {count: length, bg: backgroundColor});
//     };

//     return colCounts;
// };

// export const RDTPieChart = ({selected, column, label}) => {
//     const [pieData, setPieData] = useState({});

//     useEffect(() => {
//         const counts = getCounts(selected, column);
//         const pieVals = [...counts.values()]

//         setPieData({
//             labels: [...counts.keys()],
//             datasets: [{
//                 label: label,
//                 data: pieVals.map(pieVal => pieVal.count),
//                 backgroundColor: pieVals.map(pieVal => pieVal.bg),
//                 // borderColor: [],
//                 borderWidth: 1,
//             }]
//         })
//     }, [selected, column, label])

//     return <Pie data={pieData}/>
// };