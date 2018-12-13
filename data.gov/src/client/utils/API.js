import axios from "axios";

export default {
    //returns ALL leis based on parameters provided
    getLEIs: function() {
        return axios.get("/api/LEI");
    },
    //returns a single lei identifier up request
    getLEI: function(id) {
        return axios.get("/api/LEI/" + id);
    }
};