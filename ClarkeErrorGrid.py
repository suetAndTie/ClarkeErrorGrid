'''
CLARKE ERROR GRID ANALYSIS      ClarkeErrorGrid.py

Need Matplotlib Pyplot


The Clarke Error Grid shows the differences between a blood glucose predictive measurement and a reference measurement,
and it shows the clinical significance of the differences between these values.
The x-axis corresponds to the reference value and the y-axis corresponds to the prediction.
The diagonal line shows the prediction value is the exact same as the reference value.
This grid is split into five zones. Zone A is defined as clinical accuracy while
zones C, D, and E are considered clinical error.

Zone A: Clinically Accurate
    This zone holds the values that differ from the reference values no more than 20 percent
    or the values in the hypoglycemic range (<70 mg/dl).
    According to the literature, values in zone A are considered clinically accurate.
    These values would lead to clinically correct treatment decisions.

Zone B: Clinically Acceptable
    This zone holds values that differe more than 20 percent but would lead to
    benign or no treatment based on assumptions.

Zone C: Overcorrecting
    This zone leads to overcorrecting acceptable BG levels.

Zone D: Failure to Detect
    This zone leads to failure to detect and treat errors in BG levels.
    The actual BG levels are outside of the acceptable levels while the predictions
    lie within the acceptable range

Zone E: Erroneous treatment
    This zone leads to erroneous treatment because prediction values are opposite to
    actual BG levels, and treatment would be opposite to what is recommended.



EXAMPLES:
        look into example.ipynb


References:
[1]     Clarke, WL. (2005). "The Original Clarke Error Grid Analysis (EGA)."
        Diabetes Technology and Therapeutics 7(5), pp. 776-779.
[2]     Maran, A. et al. (2002). "Continuous Subcutaneous Glucose Monitoring in Diabetic
        Patients" Diabetes Care, 25(2).
[3]     Kovatchev, B.P. et al. (2004). "Evaluating the Accuracy of Continuous Glucose-
        Monitoring Sensors" Diabetes Care, 27(8).
[4]     Guevara, E. and Gonzalez, F. J. (2008). Prediction of Glucose Concentration by
        Impedance Phase Measurements, in MEDICAL PHYSICS: Tenth Mexican
        Symposium on Medical Physics, Mexico City, Mexico, vol. 1032, pp.
        259261.
[5]     Guevara, E. and Gonzalez, F. J. (2010). Joint optical-electrical technique for
        noninvasive glucose monitoring, REVISTA MEXICANA DE FISICA, vol. 56,
        no. 5, pp. 430434.


Made by:
Trevor Tsue
7/18/17

Editted by:
David Gerard
12/12/2023

Based on the Matlab Clarke Error Grid Analysis File Version 1.2 by:
Edgar Guevara Codina
codina@REMOVETHIScactus.iico.uaslp.mx
March 29 2013
'''


import matplotlib.pyplot as plt
import numpy as np


def plot_clarke_error_grid(
        ax: plt.axes = None, 
        format:bool = True,
        plot_params: dict = None):
    
    """
    Plot the Clarke Error Grid on the specified axes.

    Parameters:
    - ax (plt.axes, optional): Matplotlib axes to plot on. If None, the current axes are used.
    - format (bool, optional): If True, apply custom formatting using format_parameters. Default is True.
    -  plot_params (dict, optional): Dictionary containing parameters for customizing the plot format.
      If None, default parameters are used.

    Returns:
    plt.axes: Matplotlib axes containing the Clarke Error Grid plot.
    """

    if ax is None:
        ax = plt.gca()

    if  plot_params is None:
         plot_params = configure_plot_parameters()


    #Plot zone lines
    ax.plot([0,400], [0,400], ':', c= plot_params['grid_color'])                      #Theoretical 45 regression line
    ax.plot([0, 175/3], [70, 70], '-',  c= plot_params['grid_color'])
    #ax.plot([175/3, 320], [70, 400], '-',  c= plot_params['grid_color'])
    ax.plot([175/3, 400/1.2], [70, 400], '-',  c= plot_params['grid_color'])           #Replace 320 with 400/1.2 because 100*(400 - 400/1.2)/(400/1.2) =  20% error
    ax.plot([70, 70], [84, 400],'-',  c= plot_params['grid_color'])
    ax.plot([0, 70], [180, 180], '-',  c= plot_params['grid_color'])
    ax.plot([70, 290],[180, 400],'-',  c= plot_params['grid_color'])
    # ax.plot([70, 70], [0, 175/3], '-',  c= plot_params['grid_color'])
    ax.plot([70, 70], [0, 56], '-',  c= plot_params['grid_color'])                     #Replace 175.3 with 56 because 100*abs(56-70)/70) = 20% error
    # ax.plot([70, 400],[175/3, 320],'-',  c= plot_params['grid_color'])
    ax.plot([70, 400], [56, 320],'-',  c= plot_params['grid_color'])
    ax.plot([180, 180], [0, 70], '-',  c= plot_params['grid_color'])
    ax.plot([180, 400], [70, 70], '-',  c= plot_params['grid_color'])
    ax.plot([240, 240], [70, 180],'-',  c= plot_params['grid_color'])
    ax.plot([240, 400], [180, 180], '-',  c= plot_params['grid_color'])
    ax.plot([130, 180], [0, 70], '-',  c= plot_params['grid_color'])

    

    if format:
        #Set up plot
        ax.set_title( plot_params['title'])
        ax.set_xlabel( plot_params['xlabel'])
        ax.set_ylabel( plot_params['ylabel'])
        ax.set_xticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
        ax.set_yticks([0, 50, 100, 150, 200, 250, 300, 350, 400])
        ax.set_facecolor('white')

        #Set axes lengths
        ax.set_xlim(plot_params['xlim'])
        ax.set_ylim(plot_params['ylim'])
        ax.set_aspect((400)/(400))

            #Add zone titles
        if (30 > plot_params['xlim'][0] and 30 < plot_params['xlim'][1]) and (15 > plot_params['ylim'][0] and 15 < plot_params['ylim'][1]):
            ax.text(30, 15, "A",  fontsize= plot_params['font_size'])
        if (370 > plot_params['xlim'][0] and 370 < plot_params['xlim'][1]) and (370 > plot_params['ylim'][0] and 370 < plot_params['ylim'][1]):
            ax.text(370, 370, "B",  fontsize= plot_params['font_size'])
        if (280 > plot_params['xlim'][0] and 280 < plot_params['xlim'][1]) and (370 > plot_params['ylim'][0] and 370 < plot_params['ylim'][1]):
            ax.text(280, 370, "B",  fontsize= plot_params['font_size'])
        if (160 > plot_params['xlim'][0] and 160 < plot_params['xlim'][1]) and (370 > plot_params['ylim'][0] and 370 < plot_params['ylim'][1]):
            ax.text(160, 370, "C",  fontsize= plot_params['font_size'])
        if (160 > plot_params['xlim'][0] and 160 < plot_params['xlim'][1]) and (15 > plot_params['ylim'][0] and 15 < plot_params['ylim'][1]):
            ax.text(160, 15, "C",  fontsize= plot_params['font_size'])
        if (30 > plot_params['xlim'][0] and 30 < plot_params['xlim'][1]) and (140 > plot_params['ylim'][0] and 140 < plot_params['ylim'][1]):
            ax.text(30, 140, "D",  fontsize= plot_params['font_size'])
        if (370 > plot_params['xlim'][0] and 370 < plot_params['xlim'][1]) and (120 > plot_params['ylim'][0] and 120 < plot_params['ylim'][1]):
            ax.text(370, 120, "D",  fontsize= plot_params['font_size'])
        if (30 > plot_params['xlim'][0] and 30 < plot_params['xlim'][1]) and (370 > plot_params['ylim'][0] and 370 < plot_params['ylim'][1]):
            ax.text(30, 370, "E",  fontsize= plot_params['font_size'])
        if (370 > plot_params['xlim'][0] and 370 < plot_params['xlim'][1]) and (15 > plot_params['ylim'][0] and 15 < plot_params['ylim'][1]):
            ax.text(370, 15, "E",  fontsize= plot_params['font_size'])
    
    
    return ax

def configure_plot_parameters(
        title:str = "Clarke Error Grid",
        xlabel:str = "Reference Concentration [mg/dl]",
        ylabel:str = "Prediction Concentration [mg/dl]",
        xlim:tuple = (0, 400),
        ylim:tuple = (0, 400),
        font_size:int = 15,
        grid_color:str ='black'
        ):
    
    """
    Format and return a dictionary containing parameters for customizing a plot.

    Parameters:
    - title (str): Title of the plot. Default is "Clarke Error Grid".
    - xlabel (str): Label for the x-axis. Default is "Reference Concentration [mg/dl]".
    - ylabel (str): Label for the y-axis. Default is "Prediction Concentration [mg/dl]".
    - xlim (tuple): Tuple specifying the x-axis limits. Default is (0, 400).
    - ylim (tuple): Tuple specifying the y-axis limits. Default is (0, 400).
    - font_size (int): Font size for text elements in the plot. Default is 15.
    - grid_color (str): Color of the grid lines. Default is 'black'.

    Returns:
    dict: A dictionary containing the formatted parameters for customizing a plot.
    """
    
    format = {
        'title':title,
        'xlabel':xlabel,
        'ylabel':ylabel,
        'xlim':xlim,
        'ylim':ylim,
        'font_size':font_size,
        'grid_color':grid_color
    }

    return format
    

def calculate_clarke_error_zones(ref_values: np.array, pred_values: np.array, proportion: bool = False):
    """
    Compute the zones in the Clarke Error Grid based on reference and prediction values.

    Parameters:
    - ref_values (np.array): Array of reference glucose values.
    - pred_values (np.array): Array of predicted glucose values.
    - proportion (bool, optional): If True, return the proportion of data points in each zone. 
      If False (default), return the counts.

    Returns:
    np.array: An array representing the counts or proportions in each zone of the Clarke Error Grid.
              The array has 5 elements corresponding to Zones A, B, C, D, and E.

    Raises:
    AssertionError: If the lengths of reference and prediction arrays are not equal.

    Warnings:
    - If the maximum reference or prediction value exceeds the normal physiological range of glucose (<400 mg/dl).
    - If the minimum reference or prediction value is less than 0 mg/dl.
    """

    #Checking to see if the lengths of the reference and prediction arrays are the same
    assert (len(ref_values) == len(pred_values)), "Unequal number of values (reference : {}) (prediction : {}).".format(len(ref_values), len(pred_values))

    #Checks to see if the values are within the normal physiological range, otherwise it gives a warning
    if max(ref_values) > 400 or max(pred_values) > 400:
        print("Input Warning: the maximum reference value {} or the maximum prediction value {} exceeds the normal physiological range of glucose (<400 mg/dl).".format(max(ref_values), max(pred_values)))
    if min(ref_values) < 0 or min(pred_values) < 0:
        print("Input Warning: the minimum reference value {} or the minimum prediction value {} is less than 0 mg/dl.".format(min(ref_values),  min(pred_values)))

    #Statistics from the data
    zone = np.zeros(5)
    for i in range(len(ref_values)):
        if (ref_values[i] <= 70 and pred_values[i] <= 70) or (pred_values[i] <= 1.2*ref_values[i] and pred_values[i] >= 0.8*ref_values[i]):
            zone[0] += 1    #Zone A

        elif (ref_values[i] >= 180 and pred_values[i] <= 70) or (ref_values[i] <= 70 and pred_values[i] >= 180):
            zone[4] += 1    #Zone E

        elif ((ref_values[i] >= 70 and ref_values[i] <= 290) and pred_values[i] >= ref_values[i] + 110) or ((ref_values[i] >= 130 and ref_values[i] <= 180) and (pred_values[i] <= (7/5)*ref_values[i] - 182)):
            zone[2] += 1    #Zone C
        elif (ref_values[i] >= 240 and (pred_values[i] >= 70 and pred_values[i] <= 180)) or (ref_values[i] <= 175/3 and pred_values[i] <= 180 and pred_values[i] >= 70) or ((ref_values[i] >= 175/3 and ref_values[i] <= 70) and pred_values[i] >= (6/5)*ref_values[i]):
            zone[3] += 1    #Zone D
        else:
            zone[1] += 1    #Zone B

    if proportion:
        zone = np.round(100*zone/np.sum(zone))

    return zone