CONFIG = {
    # Each marker will be shown as a vertical line in the graph.
    "markers": [
        {
            # The date(s) that this event starts.
            # Index 0 means first pass, index 1 means second pass.
            'd': ['2022-02-12', '2022-02-21'],

            # The hour (24hr format) in which this event begins. For example,
            # priorities can usually start enrolling at 8am.
            't': 8,

            # The style of the vertical line.
            # See https://matplotlib.org/3.5.0/gallery/lines_bars_and_markers/linestyles.html.
            'l': 'dotted',

            # The color of the vertical line.
            # See https://matplotlib.org/3.5.0/tutorials/colors/colors.html.
            'c': '#e06d34',

            # The name of this vertical line.
            # This will be shown in the legend.
            'n': 'Priorities Start',
            
            # Whether to shade the area between the previous vertical line and this one.
            's': False
        },

        # If you want to plot the first/second pass data, the last marker
        # must ALWAYS be the "last" event, i.e. no more events will ever 
        # occur after the date corresponding to the last index of 
        # the array corresponding to property 'd'.
        {
            'd': ['2022-02-18', '2022-02-26'],
            't': 22,
            'l': 'solid',
            'c': '#000000',
            'n': 'End (FP/SP)'
        }
    ],
    "settings": {
        # The name of this term. For example, "Spring 2022" is an example.
        "termName": "Name of Term",

        # Whether this term is during Fall, Winter, or Spring quarters.
        "isNormal": True,

        # Whether to *also* plot the total number of seats (alongside
        # enrolled/available and waitlisted count).
        "showTotal": True,

        # Whether to plot the number of students enrolled (True) or the number
        # of free seats (False). For Spring 2022, use `False`.
        "useEnrolledTtl": False,

        # Whether to show any of the "markers" (the vertical lines denoting an
        # event). If this is False, then the markers array will not be used.
        "useMarkers": True,
    }
}