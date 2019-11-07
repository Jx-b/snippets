#!/usr/bin/env python3

### Script to produce volcano plots in plotly

import numpy as np
import pandas as pd
import plotly.graph_objects as go

#define significant fc and p-val thresholds
p_thresh = 0.001
fc_thresh = 3

#helper function to assign color based on significance
def is_significant(fc, p_val):
    if p_val < p_thresh:
        if fc > fc_thresh:
            return 'red'
        if fc < -1*fc_thresh:
            return 'blue'
    return 'gray'
    
    

if __name__ == '__main__':

    #import data
    df = pd.read_csv("volcano_data.txt", sep="\t")

    #assign colour based on significance
    color = df.apply(lambda x: is_significant(x["logFC"],x['adj.P.Val']), axis= 1)
    
    #if you want to highlight some gene of interest list them here
    gene_of_interest = ["Egf", "Ctgf", "Rbp1", "Eef2k"]
    color_highlight='black'

    #draw plot
    data= [go.Scatter(
        x= df['logFC'],
        y= -1*np.log10(df['adj.P.Val']),
        text= df['SYMBOL'],
        hoverinfo='text',
        textposition='top center',
        mode='markers',
        marker=dict(
            color=color)
        ),
        go.Scatter(
        x= df.loc[df['SYMBOL'].isin(gene_of_interest),'logFC'],
        y= -1*np.log10(df.loc[df['SYMBOL'].isin(gene_of_interest),'adj.P.Val']),
        text= df.loc[df['SYMBOL'].isin(gene_of_interest),'SYMBOL'],
        textposition='top center',
        mode='markers+text',
        marker=dict(
            color=color_highlight)
        )]

    shapes=[
            # Line Horizontal
            go.layout.Shape(
                type="line",
                xref="paper",
                x0=0,
                y0=-1*np.log10(p_thresh),
                x1=1,
                y1=-1*np.log10(p_thresh),
                line=dict(
                    color="gray",
                    width=1,
                    dash="dash")
            ),
            # Line Vertical
            go.layout.Shape(
                type="line",
                yref="paper",
                x0=-1*fc_thresh,
                y0=0,
                x1=-1*fc_thresh,
                y1=1,
                line=dict(
                    color="gray",
                    width=1,
                    dash="dash"
                )
            ),
            # Line Vertical
            go.layout.Shape(
                type="line",
                yref="paper",
                x0=fc_thresh,
                y0=0,
                x1=fc_thresh,
                y1=1,
                line=dict(
                    color="gray",
                    width=1,
                    dash="dash"
                )
            )]

    layout= go.Layout(title="Volcano plot",
                      xaxis = dict(title= '$\mathrm{log_{2}(fold \: change)}$',
                                range= [-1*max(abs(df['logFC'])), max(abs(df['logFC']))]),
                      yaxis = dict(title= '$\mathrm{-log_{10}(adj. \: pval)}$'),
                      shapes = shapes,
                      showlegend= False,
                      paper_bgcolor= 'rgba(0,0,0,0)',
                      plot_bgcolor= 'rgba(0,0,0,0)'
                     )

    fig = go.Figure(data=data, layout= layout)
    fig.show(renderer="browser")