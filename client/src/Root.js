import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import App from './Pages/App'
import DetailPage from './Pages/DetailPage'

// add the appropriate routes
const Root = ({ store }) => (
    <Provider store={store}>
        <Router>
            <div>

            </div>
        </Router>
    </Provider>
)

Root.propTypes = {
    store: PropTypes.object.isRequired
}

export default Root