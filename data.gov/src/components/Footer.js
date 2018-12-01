import React from 'react'
import FilterLink from '../containers/FilterLink'

const Footer = () => (
    <p>
        Show:
        {" "}
        <FilterLink filter="SHOW_ALL">
            All 
        </FilterLink>
            {", "}
        <FilterLink filter="LIVE">>
            Live:
        </FilterLink>
            {", "}
        <FilterLink filter="NOT-LIVE">>
            Not-live:
        </FilterLink>
    </p>
)

export default Footer