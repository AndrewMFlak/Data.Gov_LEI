import { connect } from 'react-redux'
import { fetchLEI } from '../actions'
import leiDetail from '../components/leiDetail'

const mapStateToProps = (state) => ({
    isLoading: state.details.isLoading,
    leiDetail: state.details.data,
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
)(leiName)

export default DetailContainer