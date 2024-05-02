import os
from typing import Dict
from jinja2 import Environment, FileSystemLoader
import dataframe_image as dfi
import matplotlib.pyplot as plt
import pandas as pd

from config import (
    COLOR_SCHEME,
    GRAPH_STYLE,
    HIGHLIGHTED_METRIC,
    METRICS,
    OUTPUT_FORMAT,
    OUTPUT_SCHEMAS,
)
from postprocess import postprocess_csv, postprocess_free, postprocess_mpstat, postprocess_nvidia_smi


class AnalysisResults:
    results: Dict[str, pd.DataFrame]
    # High to low
    color_h2l = COLOR_SCHEME
    # Low to high
    color_l2h = COLOR_SCHEME + "_r"
    destdir = "static"

    def __init__(self) -> None:
        self.results = dict()
        for format, schema in OUTPUT_SCHEMAS.items():
            self.results[format] = pd.DataFrame(columns=schema)

    def set_destdir(self, dst):
        self.destdir = dst

    def __repr__(self) -> str:
        result = []
        for format, data in self.results.items():
            result.append(f"{format}:\n {data.head(10)}")
        return "\n".join(result)

    def __render_page(self):
        for datafmt, data in self.results.items():
            if data.empty:
                continue
            (hl_metric, h2l) = HIGHLIGHTED_METRIC[datafmt]
            # float_cols = [col for col in data.columns if col != "title" and col != hl_metric  ]
            # data[float_cols] = data[float_cols].map('{:.2f}'.format)#.astype(float)
            cmap = self.color_h2l if h2l else self.color_l2h
            styled = data.style \
                .background_gradient(subset=[hl_metric], cmap=cmap) \
                .hide() \
                .format(precision=1, thousands="", decimal=".") 

            print(f"Guardando en {self.destdir}/table_{datafmt}.{OUTPUT_FORMAT}")
            dfi.export(
                # data.style.background_gradient(subset=["first%"], cmap=COLOR_SCHEME),
                # .format("{:,.2f}".format),
                styled,
                f"{self.destdir}/table_{datafmt}.{OUTPUT_FORMAT}",
                table_conversion="matplotlib",
            )

        environment = Environment(loader=FileSystemLoader("templates/"))
        template = environment.get_template("graph.html")
        content = template.render()
        with open("./tmp/index.html", "w+") as f:
            f.write(content)
        plt.savefig(f"{self.destdir}/graph.{OUTPUT_FORMAT}", bbox_inches="tight", dpi=400)

    def render_all(self):  # , metric):
        self.__postprocess_data()
        metric = METRICS[0]
        self.results["csv"].plot.bar(y=metric, **GRAPH_STYLE)
        if not os.path.exists(self.destdir):
            os.mkdir(self.destdir)
        self.__render_page()

    def add_entry(self, filename: str, row):
        """
        Agregamos de a una row
        """
        file = filename.split("/")[-1]
        title = file.split(".")[0]
        ext = file.split(".")[-1]
        self.results[ext].loc[len(self.results[ext])] = [title, *row]

    def __postprocess_data(self):
        self.results["csv"] = postprocess_csv(self.results["csv"])
        self.results["free"] = postprocess_free(self.results["free"])
        self.results["mpstat"] = postprocess_mpstat(self.results["mpstat"])
        self.results["nvidia-smi"] = postprocess_nvidia_smi(self.results["nvidia-smi"])
