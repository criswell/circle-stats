// The following is a sample config file for circle-stat
// Please remove the comments, then save the file as JSON before using!
{
    // 'repos' is a list of repositories, on the local machine, which we want
    // to keep track of
    "repos" : [
        {
            "path" : "/some/absolute/path/to/the/repo",

            // 'highlight-branches' are those branches which are special and
            // we want to highlight
            "highlight-branches" : [
                "master",
                "release",
                "..."
            ],

            // 'title' is the title for the generated page. You can use the
            // following substitutions in this string:
            //    {date}    : The date the page was generated
            "title" : "my_repository {date}",

            // 'colors' is an array of the colors to be used for each dataset
            //
            // It should contain an array of the following:
            //    "branch" : [ RED, GREEN, BLUE ]
            //  where "branch" is the branch name, and RED/GREEN/BLUE are
            //  integers specifying the RGB color.
            //
            // The default color should be specified with an empty string,
            // "", for the branch name
            "colors" : {
                "" : [ 220, 220, 220 ],
                "master" : [ 151, 187, 205 ]

            }
        },
        {
            "path" : "/some/path",
            "highlight-branches" : [
                "master"
            ],
            "title" : "some_repo {date}",
            "colors" : {
                "" : [ 198, 69, 123 ],
                "master" : [ 111, 222, 333 ]
            }
        },
        // etc....
    ],

    // This is the URL for the database. It should be in a format parsable by
    // SQLAlchemy. See here:
    //    http://docs.sqlalchemy.org/en/latest/core/engines.html#sqlalchemy.create_engine
    "database-url" : "sqlite:////some/path/to/data/circle-stats.dat",

    // For data collection, this determines how many days back we should go
    "date-offset" : {
        "days" : -1
    },

    // This determines how many days worth of data we should retain
    "max-days" : 60,

    // true if we only care about weekdays
    "weekdays-only" : true,

    // "charts" contains an array of charts we'd like to generate on each
    // page.
    //
    // Each chart must contain the following:
    //    "label"       : The label of the chart
    //    "data-type"   : The type of analysis this chart contains. Can be one
    //                    of "average", ...
    //    "chart-type"  : The type of chart to create. Can be one of "bar",
    //                    "line", ...
    //    "duration:    : The number of days back this chart will contain.
    "charts" : [
        {
            "label" : "Seven Day Averages",
            "data-type" : "average",
            "chart-type" : "bar",
            "duration" : 7
        },
        {
            "label" : "Thirty Day Averages",
            "data-type" : "average",
            "chart-type" : "line",
            "duration" : 30
        }
    ]
}
