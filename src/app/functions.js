export const titleCase = str => str[0].toUpperCase() + str.substring(1);

// export const getCounts = (selected, column) => {
//     const rowVals = selected.map(row => row[column]);
//     const colVals = [...new Set(rowVals)];
//     const colCounts = new Map();

//     for(const colVal in colVals){
//         const {length} = rowVals.filter(val => val === colVal);
//         colCounts.set(colVal, length);
//     };

//     return colCounts;
// };

// export const renameCols = (data, names) => data.map(row => {
//     for(const oldName in names){
//         const newName = names[oldName]
//         row[newName] = row[oldName]
//         delete row[oldName]
//     };
//     return row;
// });