from typing import Union, List
import dash_html_components as html
import dash_core_components as dcc


# def generate_main_layout(df: pd.DataFrame) -> Union[html.Div, None]:
def generate_main_layout(mooc_course_titles_list: List) -> Union[html.Div, None]:
    """
    Generates the main layout

    Parameters:
    mooc_course_titles_list (List): List with the names of the courses for the

    Returns:
    Union[html.Div, None]: The generated main layout for our Dash app
    """

    try:
        main_layout = html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            ["MOOC courses (edX platform)"],
                            style={
                                "fontWeight": "bold",
                                "fontSize": "large",
                                "width": "1060px",
                                "marginBottom": "6px",
                            },
                        ),
                        dcc.Dropdown(
                            id="dropdown",
                            options=[
                                {"label": i, "value": i}
                                for i in mooc_course_titles_list
                            ],
                            value=mooc_course_titles_list[0],
                            style={
                                "width": "1060px",
                                "height": "38px",
                                "fontSize": "14px",
                                "marginTop": "6px",
                            },
                        ),
                    ],
                    style={
                        "width": "1060px",
                        "fontSize": "14px",
                        "marginLeft": "60px",
                        "marginTop": "30px",
                    },
                ),
                html.Div(
                    dcc.Graph(
                        id="graph",
                        style={"height": 560, "width": 1200},
                        config={"displayModeBar": False},
                    )
                ),
                html.Div(
                    [
                        html.Div(
                            id="mooc-source-title",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "medium",
                                "width": "520px",
                                "display": "inline-block",
                                "vertical-align": "top",
                                "text-align": "center",
                                "margin-left": "60px",
                                "margin-right": "30px",
                            },
                        ),
                        html.Div(
                            id="other-course-title",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "medium",
                                "width": "520px",
                                "display": "inline-block",
                                "vertical-align": "top",
                                "text-align": "center",
                            },
                        ),
                        html.Br(),
                        html.Div(
                            id="mooc-source-description",
                            style={
                                "width": "520px",
                                "display": "inline-block",
                                "vertical-align": "top",
                                "text-align": "left",
                                "margin-left": "60px",
                                "margin-right": "30px",
                            },
                        ),
                        html.Div(
                            id="other-course-description",
                            style={
                                "width": "520px",
                                "display": "inline-block",
                                "vertical-align": "top",
                                "text-align": "left",
                            },
                        ),
                    ]
                ),
            ]
        )
        return main_layout
    except Exception:
        print("error generating main layout")
        return None
