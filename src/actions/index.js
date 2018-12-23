import axios from "axios"
// import sqlite3 from "sqlite3"

// let nextLeiId = 0

// const BASEURL = "";
// const APIKEY = "";

// const sqlite3 = require('sqlite3').verbose();
// open database
let db = new sqlite3.Database('LEIscrape.db.sqlite', (err) => {
    if (err) {
        return console.error(err.message);
    }
    return console.log('Connected to MongoDB database.');
});

// close the database connection
db.close((err) => {
    if (err) {
        return console.error(err.message);
    }
    console.log('Close the database connection.');
});

export const setVisibilityFilter = (filter) => ({
    type: 'SET_VISIBILITY_FILTER',
    filter
})
export const toggleLEI = (id) => ({
    type: 'TOGGLE_LEI',
    id
})
export const requestData = (key) => ({
    type: "REQUEST_DATA",
    key
})

export const receiveData = (key, data) => ({
    type: "RECEIVE_DATA",
    key,
    data
})

export const saveSelectedLEI = (LEIName) => ({
    type: "SAVE_LEI",
    LEIName
})

export function fetchLEI(LEIName) {
    return function(dispatch) {
        dispatch(requestData("REQUEST_Data"))
        return axios.get(BASEURL + LEIName + APIKey).then(
            function(data) {
                console.log(data)
                setTimeout(function() {dispatch(receiveData(LEIName, data.data))}, 2500)
            }
        )
    }
}