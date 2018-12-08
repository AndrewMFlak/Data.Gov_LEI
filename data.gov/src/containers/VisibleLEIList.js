import { connect } from 'react-redux'
import { toggleLEI } from '../actions'
import LEIList from 'components/LEIList'

const getVisibleLEIs = (LEIs, filter) => {
    switch (filter) {
        case 'SHOW_ALL':
            return LEIs
        case 'SHOW_LIKED':
            return LEIs.filter(t => !t.save)
        case 'SHOW_HATE':
            return LEIs.filter(t => t.hate)
        default:
            throw new Error('Unknown filter: ' + filter)
    }
}

const mapStateToProps = (state) => ({
    LEIs: getVisibleMovies(state.LEIs,
        state.visibleFilter),
        isLoading: state.details.isLoading,
        LEIDetails: state.details.data
})

const mapDispatchToProps = (dispatch) => ({
    onLEIClick: id => {
        dispatch(toggleLEI(id))
    },
    onLEIDetailClick: LEIName => {
        dispatch(saveSelectedLEI(LEIName))
    }
})
 const VisibleLEIList = connect(
     mapStateToProps, mapDispatchToProps)(LEIList)

export default VisibleLEIList