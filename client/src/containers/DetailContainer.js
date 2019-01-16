import { connect } from 'react-redux'
import { fetchLEI } from '../actions'
import leiDetails from '../components/leiDetails'

const mapStateToProps = (state) => ({
    isLoading: state.details.isLoading,
    leiDetails: state.details.data,
    leiName: state.details.leiName
})

const mapDispatchToProps = (dispatch) => ({
    onPageLoad: (leiName) => {
        dispatch(fetchLEI(leiName))
    }
})

const DetailContainer = connect(
    mapStateToProps,
    mapDispatchToProps
)(leiDetails)

export default DetailContainer