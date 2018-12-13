const path = require("path");
const router = require("express").Router();

// const db = require("../TEST.db.sqlite")
// if processing a user input we would pass through a mode.  because no we will skip this route.
// const db = require("../models");

// const sqlite3 = require('sqlite3').verbose();

// establishes database connection to sqlite
// let db = new sqlite3.Database('../TEST.db.sqlite', (err) => {
//     if (err) {
//         return console.log(err.message);
//     }
//     console.log('Connected to SQLite database');
// });

// console.log(db)




const LEIFunctions = {
    findAll: function(req, res) {
        db.LEI
            .find(req.query)
            .sort({Country:ascending})
            .then(dbModel =>res.json(dbModel))
            .catch(err => res.status(422).json(err));
    }
}

// API routes

router.get("/api/LEIs", LEIFunctions.findAll)

// If no API routes are hit, send the React app
// router.use(functions (req, res) {
//     res.send(path.join(__dirname,
//         "../client/build/index.html"))
// })

module.exports = router;