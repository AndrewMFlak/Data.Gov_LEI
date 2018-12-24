import React from "react";
import ReactLoading from 'react-loading';
import PropTypes from 'prop-types'
import { Link } from "react-router-dom";

class leiDetail extends React.Component {

    componentDidMount = () => {
        this.props.onPageLoad(this.props.leiName);
    }

    getDetails = (isLoading, leiDetail) => {
        if (isLoading) {
            return <ReactLoading type="spin" color="0000FF" height={100} width={100} />
        } else if (Object.keys(leiDetail).length !== 0) {
            return (
                <div className="text-center" >
                    <h3>
                        LeiIdentifier: {leiDetail.LeiIdentifier}
                    </h3>
                    <h3>
                        Name: {leiDetail.Name}
                    </h3>
                    <h3>
                        EntityStatus: {leiDetail.EntityStatus}
                    </h3>
                    <h3>
                        Country: {leiDetail.Country}
                    </h3>
                    <h3>
                        InferredJurisdiction: {leiDetail.InferredJurisdiction}
                    </h3>
                    <h3>
                        RegisteredAddress: {leiDetail.RegisteredAddress}
                    </h3>
                    <h3>
                        HeadquarteredAddress: {leiDetail.HeadquarteredAddress}
                    </h3>
                    <h3>
                        RegistrationStatus: {leiDetail.RegistrationStatus}
                    </h3>
                    <h3>
                        LegalForm: {leiDetail.LegalForm}
                    </h3>
                    <h3>
                        RegistrationStatus: {leiDetail.RegistrationStatus}
                    </h3>
                    <h3>
                        BusinessRegistryName: {leiDetail.BusinessRegistryName}
                    </h3>
                    <h3>
                        RegistrationStatus: {leiDetail.RegistrationStatus}
                    </h3>
                    <h3>
                        BusinessRegistryAlert: {leiDetail.BusinessRegistryAlert}
                    </h3>
                    <h3>
                        RegisteredBy: {leiDetail.RegisteredBy}
                    </h3>
                    <h3>
                        RecordLastUpdate: {leiDetail.RecordLastUpdate}
                    </h3>
                    <h3>
                        NextRenewalDate: {leiDetail.NextRenewalDate}
                    </h3>
                    <h3>
                        LoadTime: {leiDetail.LoadTime}
                    </h3>
                    <h3>
                        ItemTag: {leiDetail.ItemTag}
                    </h3>
                    <h3>
                        AssignmentDate: {leiDetail.AssignmentDate}
                    </h3>
                </div>
            )
        } else {
            return <div />
        }
    }

    render() {

        const { isLoading, leiDetail } = this.props 

        return (
            <div>
                {this.getDetails(isLoading, leiDetail)}
                <Link to="/">← Back to List</Link>
            </div>
        );

    }
}

leiDetail.propTypes = {
    isLoading: PropTypes.bool.isRequired,
    leiDetail: PropTypes.object.isRequired,
    leiName: PropTypes.string.isRequired,
    onPageLoad: PropTypes.func.isRequired
}

export default leiDetail;