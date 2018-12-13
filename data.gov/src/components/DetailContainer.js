import React from 'react'
import ReactLoading from 'react-loading';
import PropTypes from 'prop-types';
import { Link } from "react-router-dom";

class LEIDetail extends React.Component {
    componentDidMount = () => {
        this.props.onPageLoad(this.props.LEIName)
    }

    getDetails = (isLoading, LEIDetails) => {
        if (isLoading) {
            return <ReactLoading type="spin" color="#0000FF" height={100} width={100} />
        } else if (Object.keys(LEIDetails).length !== 0) {
            return (
                <div className="text-center" >
                    <img
                        className="img-responsive"
                        src={movieDetails.Poster}
                        style={{ margin: "0 auto" }}
                        alt="sample"
                    />
                    <h3>
                        Director(s): {LEIDetails.Director}
                    </h3>
                    <h3>
                        Genre: {LEIDetails.Genre}
                    </h3>
                    <h3>
                        Released: {LEIDetails.Released}
                    </h3>
                </div>
            )
        } else {
            return <div />
        }
    }

    render() {
        const {isLoading, LEIDetails } = this.props

        return (
            <div>
            {this.getDetails(isLoading, LEIDetails)}
            <Link to="/">← Back to List</Link>
        </div>
        );
    }
}
LEIDetail.propTypes = {
    isLoading: PropTypes.bool.isRequired,
    LEIDetails: PropTypes.object.isRequired,
    LEIName: PropTypes.string.isRequired,
    onPageLoad: PropTypes.func.isRequired
}

export default LEIDetail