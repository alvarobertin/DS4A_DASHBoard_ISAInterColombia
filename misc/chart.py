#https://dash.gallery/dash-deck-explorer/point-cloud-layer

import numpy as np
import laspy as lp
import numpy as np
import pandas as pd
import json
import pydeck
import dash
import dash_deck
from dash import html


def transform_colors(f):
    #https://github.com/strawlab/python-pcl/issues/171
    red = (f.red)
    green = (f.green)
    blue = (f.blue)
    # 16bit to convert 8bit data(data Storage First 8 bits case)
    red = np.right_shift(red, 8).astype(np.uint8)
    green = np.right_shift(green, 8).astype(np.uint8)
    blue = np.right_shift(blue, 8).astype(np.uint8)
    red = red.astype(np.uint32)
    green = green.astype(np.uint32)
    blue = blue.astype(np.uint32)

    return (red, green, blue)

def main():
    input_path=""
    dataname="MDS-1"

    las = lp.read(input_path+dataname+".las")

    #point_data = np.stack([las.X, las.Y, las.Z], axis=0).transpose((1, 0))

    #colors = np.stack([las.red, las.green, las.blue], axis=0).transpose((1, 0))

    point_data = np.vstack((las.x, las.y, las.z)).transpose()

    #colors = np.vstack((las.red, las.green, las.blue)).transpose()

    red, green, blue = transform_colors(las)
    
    colors = np.vstack((red, green, blue)).transpose()

    df = pd.DataFrame(data= point_data, columns=["x", "y", "z"])

    color = pd.DataFrame(data= colors, columns=["r", "g", "b"])


    m = df.join(color)

    df2 = m.sort_values(by="y")[:2000000]

    target = [df2.x.mean(), df2.y.mean(), df2.z.mean()]

    point_cloud_layer = pydeck.Layer(
        "PointCloudLayer",
        data=df2,
        get_position=["x", "y", "z"],
        get_color=["r", "g", "b"],
        get_normal=[0, 0, 15],
        auto_highlight=True,
        pickable=True,
        point_size=3,
    )
    view_state = pydeck.ViewState(
        target=target
    )
    view = pydeck.View(type="OrbitView", controller=True)

    r = pydeck.Deck(point_cloud_layer, initial_view_state=view_state, views=[view])
    
   
    Rjson = r.to_json()

    # Save the json file
    # with open('new_file.json', 'w') as f:
    #     json.dump(Rjson, f)

    app = dash.Dash(__name__)
    app.layout = html.Div(
        dash_deck.DeckGL(Rjson, id="deck-gl", style={"background-color": "#add8e6"})
    )


    if __name__ == "__main__":
        app.run_server(debug=True)


main()


