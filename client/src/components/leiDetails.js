import React from "react";
import ReactLoading from 'react-loading';
import PropTypes from 'prop-types'
import { Link } from "react-router-dom";

class leiDetails extends React.Component {

    componentDidMount = () => {
        this.props.onPageLoad(this.props.leiName);
    }

    getDetails = (isLoading, leiDetails) => {
        if (isLoading) {
            return <ReactLoading type="spin" color="0000FF" height={100} width={100} />
        } else if (Object.keys(leiDetails).length !== 0) {
            return (
                <div className="text-center" >
                    <h3>
                        LeiIdentifier: {leiDetails.LeiIdentifier}
                    </h3>
                    <h3>
                        Name: {leiDetails.Name}
                    </h3>
                    <h3>
                        EntityStatus: {leiDetails.EntityStatus}
                    </h3>
                    <h3>
                        Country: {leiDetails.Country}
                    </h3>
                    <h3>
                        InferredJurisdiction: {leiDetails.InferredJurisdiction}
                    </h3>
                    <h3>
                        RegisteredAddress: {leiDetails.RegisteredAddress}
                    </h3>
                    <h3>
                        HeadquarteredAddress: {leiDetails.HeadquarteredAddress}
                    </h3>
                    <h3>
                        RegistrationStatus: {leiDetails.RegistrationStatus}
                    </h3>
                    <h3>
                        LegalForm: {leiDetails.LegalForm}
                    </h3>
                    <h3>
                        RegistrationStatus: {leiDetails.RegistrationStatus}
                    </h3>
                    <h3>
                        BusinessRegistryName: {leiDetails.BusinessRegistryName}
                    </h3>
                    <h3>
                        RegistrationStatus: {leiDetails.RegistrationStatus}
                    </h3>
                    <h3>
                        BusinessRegistryAlert: {leiDetails.BusinessRegistryAlert}
                    </h3>
                    <h3>
                        RegisteredBy: {leiDetails.RegisteredBy}
                    </h3>
                    <h3>
                        RecordLastUpdate: {leiDetails.RecordLastUpdate}
                    </h3>
                    <h3>
                        NextRenewalDate: {leiDetails.NextRenewalDate}
                    </h3>
                    <h3>
                        LoadTime: {leiDetails.LoadTime}
                    </h3>
                    <h3>
                        ItemTag: {leiDetails.ItemTag}
                    </h3>
                    <h3>
                        AssignmentDate: {leiDetails.AssignmentDate}
                    </h3>
                </div>
            )
        } else {
            return <div />
        }
    }

    render() {

        const { isLoading, leiDetails } = this.props 

        return (
            <div>
                {this.getDetails(isLoading, leiDetails)}
                <Link to="/">← Back to List</Link>
            </div>
        );

    }
}

leiDetails.propTypes = {
    isLoading: PropTypes.bool.isRequired,
    leiDetail: PropTypes.object.isRequired,
    leiName: PropTypes.string.isRequired,
    onPageLoad: PropTypes.func.isRequired
}

export default leiDetails;