const express = require("express");
const bodyParser = require("body-parser");
const mongoose = require("mongoose")
const LEIController = require("./controllers/LEIController")
const app = express();
const PORT = process.env.PORT || 6868;

// Configure body parser for AJAX requests
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());

// Serve up static assets
app.use(express.static("client/build"));

// Add routes, both API and view
app.use(LEIController);

// Set up promises with mongoose
mongoose.Promise = global.Promise;

// Connect to the Mongo DB
mongoose.connect(
    process.env.MONGODB_URI || "mongodb://localhost/LEIs",
    {
      useMongoClient: true
    }
).then(() => {
     console.log("Connected to Database!!!!");
     }).catch((err) => {
         console.log("Not Connected to Database ERROR! ", err);
         process.exit(1);
     });

app.listen(PORT, function() {
     console.log(`🌎  ==> API Server now listening on PORT ${PORT}!`);
     console.log('Home: ',`http://localhost:6868`);
     console.log('Home: ',`http://localhost:6868/LEIs/v1.0`);
     });

