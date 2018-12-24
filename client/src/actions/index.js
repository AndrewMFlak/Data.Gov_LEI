import axios from "axios"

// let nextLeiId = 0

const BASEURL = "http://localhost:6868";
// const APIKEY = "";

// const sqlite3 = require('sqlite3').verbose();
// open database

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

export function fetchLEI(LEIs) {
    return function(dispatch) {
        dispatch(requestData("REQUEST_DATA"))
        return axios.get(BASEURL + LEIs).then(
            function(data) {
                console.log(data)
                setTimeout(function() {dispatch(receiveData(LEIs, data.data))}, 2500)
            }
        )
    }
}