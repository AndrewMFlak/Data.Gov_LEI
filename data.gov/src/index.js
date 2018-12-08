import React from 'react'
import ReactDOM from 'react-dom'
import './index.css'
// import App from './Pages/App';
// import * as serviceWorker from './serviceWorker';
import { createStore, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import Root from './Root'
import leiList from './reducers'

let store = createStore(leiList, applyMiddleware(thunk))

ReactDOM.render(<Root store={ store } />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
// serviceWorker.unregister();
