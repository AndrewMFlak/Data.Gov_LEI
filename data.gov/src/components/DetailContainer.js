import { connect } from 'react-redux'
import leiDetail from '../components/leiDetail'


const mapStateToProps = (state) => ({
    isLoading: state.details.isLoading,
    leiDetails: state.details.data,
    leiName: state.details.leiName
})

const mapDispatchToProps = (dispatch) => ({
    onPageLoad: (leiName) => {
        dispatch(fetchLei(leiName))
    }
})

const DetailContainer = connect(
    mapStateToProps,
    mapDispatchToProps)(leiDetail)

export default DetailContainer