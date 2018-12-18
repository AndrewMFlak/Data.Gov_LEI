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
// app.use(express.static("client/build"));

// Add routes, both API and view
app.use(LEIController);

// Set up promises with mongoose
// mongoose.Promise = global.Promise;


// mongoose.connect(
//     process.env.MONGODB_URI || "mongodb://localhost/27017",
//     {
//       useMongoClient: true
//     }
//   );


app.listen(PORT, function() {
     console.log(`🌎  ==> API Server now listening on PORT ${PORT}!`);
     console.log('Home: ',`http://localhost:6868`);
     });

