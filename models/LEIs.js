const mongoose = require("mongoose")
const Schema = mongoose.Schema;

const LEISchema = new Schema({
    id: {type: String, required: true },
    EntityStatus: {type: String, required: true },
    Country: {type: String, required: true },
    InferredJurisdiction: {type: String, required: true},
    RegisteredAddress: {type: String, required: true},
    HeadquarteredAddress: {type: String, required: true},
    LeiIdentifier: {type: String, required: true},
    Name: {type: String, required: true},
    RegistrationStatus: {type: String, required: true},
    LegalForm: {type: String, required: true},
    BusinessRegistryName: {type: String, required: true},
    BusinessRegistryAlert: {type: String, required: true},
    RegisteredBy: {type: String, required: true},
    AssignmentDate: {type: String, required: true},
    RecordLastUpdate: {type: String, required: true},
    NextRenewalDate: {type: String, required: true},
    ItemCount: {type: String, required: true},
    ItemTag: {type: String, required: true},
    LoadTime: {type: String, required: true}
});
const LEIs = mongoose.model("LEIs", LEISchema);

module.exports = LEIs;