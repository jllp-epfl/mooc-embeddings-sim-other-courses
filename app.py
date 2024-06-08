import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from config import load_toml_config_file
from utils import truncate_name, load_mooc_descriptions, load_course_descriptions
from layout import generate_main_layout
import dash

global selected_course_name
global plot_data
global moocs_descr

moocs_descr = {}

config = load_toml_config_file(config_file_path="data/config.toml")
if config is None:
    print("Error: could not load config file")
    exit()

# loading data
plot_data = pd.DataFrame()
info_msg = config["general"]["info_msg"]

moocs_descr = load_mooc_descriptions(
    mooc_descriptions_path=config["general"]["moocs_with_descriptions_path"]
)

if moocs_descr is None:
    print("Error: could not load the MOOCs data")
    exit()


df = load_course_descriptions(
    course_descriptions_path=config["general"]["dataset_path"]
)
if df is None:
    print("Error: could not load the course data")
    exit()

selected_course_name = df.index[0]

# initializing app
app = dash.Dash(
    __name__,
    requests_pathname_prefix=config["general"]["path_name_prefix"],
    prevent_initial_callbacks="initial_duplicate",
)

app.title = "Course Retriever"

# generating layout
mooc_course_titles_list = df.index
app.layout = generate_main_layout(mooc_course_titles_list)
if app.layout is None:
    print("Error: could not load the course data")
    exit()


@app.callback(
    [
        Output("mooc-source-title", "children", allow_duplicate=True),
        Output("other-course-title", "children", allow_duplicate=True),
        Output("other-course-description", "children", allow_duplicate=True),
        Output("mooc-source-description", "children"),
        Output("graph", "figure", allow_duplicate=True),
    ],
    [Input(component_id="dropdown", component_property="value")],
)
def build_graph(selected_course):
    global plot_data
    global selected_course_name

    selected_course_name = selected_course

    description = moocs_descr[selected_course]
    name_max_len = config["general"]["name_max_len"]
    course_data = df.loc[selected_course].dropna()

    recommendations = []
    course_codes = []
    professors = []
    descriptions = []
    scores = []
    colors = []
    course_types = []

    for data in course_data.values:
        parts = data.split("\t\t")
        course_name = parts[0]
        score = float(parts[1])
        course_type = parts[2]  # "mooc" or "non-mooc"
        course_code = parts[3]
        professor = parts[4]
        description = parts[5]
        course_codes.append(course_code)
        professors.append(professor)
        descriptions.append(description)

        truncated_course_name = truncate_name(course_name, name_max_len)

        recommendations.append(truncated_course_name)
        scores.append(score)
        course_types.append(course_type)

        if course_type == "mooc":
            colors.append(config["general"]["mooc_courses_bar_color"])
        else:
            colors.append(config["general"]["other_courses_bar_color"])

    plot_data = pd.DataFrame(
        {
            "course_name": recommendations,
            "course_code": course_codes,
            "cosine_distance": scores,
            "professor": professors,
            "course_type": course_types,
            "color": colors,
            "other_course_description": descriptions,
        }
    )

    plot_data = plot_data.iloc[::-1].reset_index(drop=True)

    # we create the bar chart figure
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=plot_data["course_name"],
            x=plot_data["cosine_distance"],
            orientation="h",
            marker_color=plot_data["color"],
            customdata=plot_data[["course_code", "professor", "course_type"]],
            hovertemplate="<b>%{y}</b><br>"
            + "Cosine Distance: %{x}<br>"
            + "Course Code: %{customdata[0]}<br>"
            + "Professor: %{customdata[1]}<br>"
            + "Course Type: %{customdata[2]}<br>"
            + "<extra></extra>",  # <extra></extra> to hide the trace name
        )
    )

    # we display the name of the selected MOOC course
    fig.update_layout(
        title=f"Closest courses to: {selected_course}",
        xaxis_title="Cosine Distance",
        yaxis_title="",
    )

    fig.update_layout(
        margin=dict(
            l=config["general"]["left_margin"],
            t=config["general"]["top_margin"],
            b=config["general"]["bottom_margin"],
        )
    )
    fig.update_xaxes(
        range=[config["general"]["axes_x_start"], config["general"]["axes_x_end"]]
    )

    other_course_title = info_msg
    other_course_description = ""

    return (
        selected_course_name,
        other_course_title,
        other_course_description,
        description,
        fig,
    )


@app.callback(
    [
        Output("other-course-description", "children", allow_duplicate=True),
        Output("other-course-title", "children", allow_duplicate=True),
    ],
    [Input("graph", "clickData")],
)
def display_click_data(clickData):
    if clickData is None:
        return "", info_msg
    else:
        try:
            course_code = clickData["points"][0]["customdata"][0]
            selected_row = plot_data[plot_data["course_code"] == course_code].iloc[0]
            selected_title = selected_row["course_name"]
            selected_description = selected_row["other_course_description"]
            course_type = selected_row["course_type"]
            print(f"course_type={course_type}")
            return selected_description, selected_title
        except IndexError:
            return "Information not found. Please try another selection."


if __name__ == "__main__":
    app.run_server(
        host=config["general"]["hostname"],
        debug=False,
        port=config["general"]["port"],
        threaded=True,
    )
