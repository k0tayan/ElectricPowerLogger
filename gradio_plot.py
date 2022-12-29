import gradio as gr
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

log_path = 'logs'


def csv_plot(file_name):
    df = pd.read_csv(file_name)
    fig = plt.figure(figsize=(15, 5))
    # dfの一列目をx軸、二列目をy軸にしてプロットする
    plt.plot(df[df.columns[0]], df[df.columns[1]])
    plt.xlabel(df.columns[0])
    plt.ylabel(df.columns[1])
    return fig


def list_csv_files(path):
    files = os.listdir(path)
    csv_files = [
        os.path.join(path, f) for f in files
        if os.path.isfile(os.path.join(path, f)) and f.endswith('.csv')
    ]
    return csv_files


csv_files = list_csv_files(log_path)

with gr.Blocks() as demo:
    with gr.Row():
        plot_input = gr.inputs.Dropdown(csv_files, default=csv_files[-1])
        plot_button = gr.Button("Plot")
    with gr.Row():
        plot_output = gr.Plot()
    plot_button.click(csv_plot, inputs=plot_input, outputs=plot_output)
demo.launch()
