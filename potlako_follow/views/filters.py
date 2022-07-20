from edc_dashboard.listboard_filter import ListboardFilter, ListboardViewFilters

class ListboardViewFilters(ListboardViewFilters):
    
    
    current_user = ListboardFilter(
        label='My Worklist',
        position=1,)
    

    all = ListboardFilter(
        name='all',
        label='All',
        position=2,
        lookup={})

    is_called = ListboardFilter(
        label='Called',
        position=3,
        lookup={'is_called': True})

    visited = ListboardFilter(
        label='Visited',
        position=4,
        lookup={'visited': True})

    high = ListboardFilter(
        label='High',
        position=5,
        lookup={'cancer_probability': 'high'})

    moderate = ListboardFilter(
        label='Moderate',
        position=6,
        lookup={'cancer_probability': 'Moderate'})

    low = ListboardFilter(
        label='Low',
        position=7,
        lookup={'cancer_probability': 'Low'})


class NavigationListboardViewFilters(ListboardViewFilters):
    pass

