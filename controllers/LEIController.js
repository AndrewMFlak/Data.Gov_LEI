const path = require("path");
const router = require("express").Router();
const db = require("../models");

const LEIFunctions = {
    findAll: function(req, res) {
        db.LEIs
            .find(req.query)
            // .sort({Country:ascending})
            .then(dbModel =>res.json(dbModel))
            .catch(err => res.status(422).json(err));
    },
    findById: function(req, res) {
        db.LEIs
            .findById(req.params.id)
            .then(dbModel => res.json(dbModel))
            .catch(err => res.status(422).json(err));
    }
}

// API routes

router.get("/api/LEIs", LEIFunctions.findAll)

router.get("/api/LEIs/:id", LEIFunctions.findById)

// UPDATE
// If no API routes are hit, send the React app
router.use(function (req, res) {
    res.send(path.join(__dirname,
        "../client/build/index.html"));
});

module.exports = router;