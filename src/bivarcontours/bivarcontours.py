"""
function-contour-dimensioning-diagram.py

Crate a dimensioning diagram for the dependent variable z of an arbitrary function
with two independent variables x and y.

MIT License
Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works
and modifications, which include larger works using a licensed work, under the same license.
Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.
Contributor: Uwe Schweinsberg december 2023

ToDo:
* Parameters without input validation: The initializer accepts quite a few parameters but does not verify if
they are in the correct form/type. Depending on the rest of the program it could lead to potential errors if
incorrect data types are passed.

* click expects x_start to be a float. If the user passes a string that cannot be converted to a float, click will
raise an error. This is a simple form of type-checking that works very well at the boundaries of your systems
(where your function interacts with the user).

However, keep in mind that click type checking does not substitute good practices inside your code. It aids in
making sure inputs are of correct type but proper error handling, input checking, and type checking inside your
functions and methods are still very important.

Moreover, since Python is a dynamically typed language, the type of a variable can change during program execution.
Therefore, having type checks at critical points in your code (not just at the entry points) can help
prevent type-related bugs.

* Potential division by zero: In the compute_values function, if self.arr_step_1 or self.arr_step_2 is zero, it would
    lead to ValueError.

* Closeness of values: If the min_1 and max_1 values are too close, it could lead to problems
    with the np.arange function. The same goes for min_2 and max_2.
"""

import math

import click
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter
from numpy import sqrt
import seaborn as sns
import numpy as np
from pint import UnitRegistry

ureg = UnitRegistry()
Q_ = ureg.Quantity
color = sns.color_palette()
FIGURE_SIZE = 10
TITLE_FONTSIZE = 14
TITLE_FONTWEIGHT = 'bold'
MAX_DISPLAY_DIGITS = 4
SCALING_EXPONENT = 3
SCALING_FACTOR = 10 ** SCALING_EXPONENT


def calculate_z(formula_, x_scalar_, y_scalar_):
    # formula_ = f(x,y)
    x = x_scalar_
    y = y_scalar_
    # Test for Division by zero
    try:
        z = eval(formula_)
    except ZeroDivisionError as e:
        raise ZeroDivisionError("Division by zero: choose an other ranges for the x ond / or y variables", e)
    return z


class Contour:
    """

    This class represents a Contour object for generating contour plots.

    Attributes:
    - title (str): The title of the contour plot
    - label_1 (str): The label for the first dimension
    - label_2 (str): The label for the second dimension
    - formula (str): The formula used to calculate the contour values
    - dim_res (str): The dimensional resolution of the contour plot
    - min_1 (float): The minimum value for the first dimension
    - max_1 (float): The maximum value for the first dimension
    - step_1 (float): The step size for the first dimension
    - dim_1 (str): The dimension unit for the first dimension
    - min_2 (float): The minimum value for the second dimension
    - max_2 (float): The maximum value for the second dimension
    - step_2 (float): The step size for the second dimension
    - dim_2 (str): The dimension unit for the second dimension
    - swap_axes (bool): Indicates whether to swap the axes of the contour plot
    - verbose (bool): Indicates whether to include verbose output during computation

    Methods:
    - __init__(self, title, label_1, label_2, formula, dim_res, min_1, max_1, step_1, dim_1, min_2, max_2, step_2, dim_2, swap_axes, verbose=False): Initializes a Contour object with the
    * given parameters.
    - initialize_swapping_axes(self, dim_1, dim_2): Initializes the values for swapping the axes if necessary.
    - initialize_values(self): Initializes all necessary values for generating the contour plot.
    - initialize_dimension_one_values(self): Initializes the values for the first dimension.
    - initialize_dimension_two_values(self): Initializes the values for the second dimension.
    - _set_correct_units_for_dimension(self, dimension, min_value, max_value, step_value): Sets the correct units for a given dimension.
    - _convert_units_to_dimensionless_and_get_interval(self, min_value, max_value, step_value): Converts the units to dimensionless and returns the interval.
    - initialize_diagram_labels(self): Initializes the labels for the contour plot diagram.
    - set_values_for_contour_calc_with_scalars_scaled_to_base_units(self): Sets the values for calculating the contour with scaled base units.
    - filename_for_saved_contour_figure(self): Generates the filename for saving the contour figure.
    - compute_values(self): Computes the contour values based on the given formula and dimension values.
    - check_ticks_in_range(self, ax): Checks if the ticks are within the range of the contour plot.

    """

    def __init__(self, title, label_1, label_2, formula, dim_res, min_1, max_1, step_1, dim_1, min_2, max_2, step_2,
                 dim_2, swap_axes, verbose=False):
        self.step_2_interval = None
        self.step_1_interval = None
        self.Y = None
        self.X = None
        self.hl = None
        self.vals = None
        self.filename = None
        self.label_y = None
        self.label_x = None
        self.y_values = None
        self.x_values = None
        self.arr_step_2 = None
        self.stop_2 = None
        self.base_unit_2 = None
        self.start_2 = None
        self.arr_step_1 = None
        self.stop_1 = None
        self.base_unit_1 = None
        self.start_1 = None
        self.unity_res = None
        self.title = title
        self.label_1 = label_1
        self.label_2 = label_2
        self.formula = formula
        self.dim_res = dim_res
        self.min_1 = min_1
        self.max_1 = max_1
        self.step_1 = step_1
        self.min_2 = min_2
        self.max_2 = max_2
        self.step_2 = step_2
        self.are_axes_swapped = swap_axes.lower() == 'true'
        self.initialize_swapping_axes(dim_1, dim_2)
        self.verbose = verbose

    def initialize_swapping_axes(self, dim_1, dim_2):
        """
        This method initializes the swapping of axes.

        :param dim_1: The first dimension to be swapped.
        :param dim_2: The second dimension to be swapped.
        :return: None

        """
        if self.are_axes_swapped:
            self.dim_1 = dim_1
            self.dim_2 = dim_2
        else:
            self.dim_2 = dim_1
            self.dim_1 = dim_2

    def initialize_values(self):
        """
        Initializes the values required for the calculation and plotting of contours.

        :return: None
        """
        self.unity_res = Q_(1, self.dim_res)

        self.initialize_dimension_one_values()
        self.initialize_dimension_two_values()
        self.initialize_diagram_labels()
        self.set_values_for_contour_calc_with_scalars_scaled_to_base_units()
        self.filename_for_saved_contour_figure()

    def initialize_dimension_one_values(self):
        """
        Initializes the values related to dimension one.

        :return: None
        """
        min_1_with_unit, max_1_with_unit, step_1_with_unit = (
            self._set_correct_units_for_dimension(self.dim_1, self.min_1, self.max_1, self.step_1))
        self.start_1, self.base_unit_1, self.stop_1, self.step_1_interval = (
            self._convert_units_to_dimensionless_and_get_interval(min_1_with_unit, max_1_with_unit, step_1_with_unit))

    def initialize_dimension_two_values(self):
        """
        Initializes dimension two values.

        :return: None
        """
        min_2_with_unit, max_2_with_unit, step_2_with_unit = (
            self._set_correct_units_for_dimension(self.dim_2, self.min_2, self.max_2, self.step_2))
        self.start_2, self.base_unit_2, self.stop_2, self.step_2_interval = (
            self._convert_units_to_dimensionless_and_get_interval(min_2_with_unit, max_2_with_unit, step_2_with_unit))

    def _set_correct_units_for_dimension(self, dimension, min_value, max_value, step_value):
        """
        :param dimension: The dimension of the values being set. This should be a valid dimension recognized by the Quantity class.
        :param min_value: The minimum value allowed for the dimension.
        :param max_value: The maximum value allowed for the dimension.
        :param step_value: The step value by which the dimension values should be incremented.

        :return: A tuple containing the minimum value, maximum value, and step value, all with the appropriate units based on the dimension provided.
        """
        min_value_with_unit = Q_(min_value, dimension)
        max_value_with_unit = Q_(max_value, dimension)
        step_value_with_unit = Q_(step_value, dimension)
        return min_value_with_unit, max_value_with_unit, step_value_with_unit

    def _convert_units_to_dimensionless_and_get_interval(self, min_value, max_value, step_value):
        """
        Converts units to dimensionless and returns the start, base unit, stop, and interval.

        :param min_value: The minimum value with units.
        :param max_value: The maximum value with units.
        :param step_value: The step value with units.
        :return: A tuple containing the start (dimensionless), base unit (dimensionless),
            stop (dimensionless), and interval (dimensionless).
        """
        start = min_value.to_base_units().magnitude
        base_unit = min_value.to_base_units().units
        stop = max_value.to_base_units().magnitude
        interval = step_value.to_base_units().magnitude
        return start, base_unit, stop, interval

    def initialize_diagram_labels(self):
        """
        Initializes the labels for the x and y axes of the diagram.

        :return: None
        """
        self.label_x = self.label_2 if self.are_axes_swapped else self.label_1
        self.label_y = self.label_1 if self.are_axes_swapped else self.label_2

    def set_values_for_contour_calc_with_scalars_scaled_to_base_units(self):
        """
        Sets the values for the X and Y coordinates to be used in contour calculation.
        The X values are generated using the given start_1, stop_1, and step_1_interval parameters.
        The Y values are generated using the given start_2, stop_2, and step_2_interval parameters.

        :return: None
        """
        self.x_values = np.arange(self.start_1, self.stop_1, step=self.step_1_interval)
        self.y_values = np.arange(self.start_2, self.stop_2, step=self.step_2_interval)

    def filename_for_saved_contour_figure(self):
        """
        Generate a filename for saving a contour figure.

        :return: The generated filename for saving the contour figure.
        :rtype: str
        """
        self.filename = (f'F_{self.title}_{self.dim_res}_X_{self.dim_1}_{self.x_values[0]:.2f}-'
                         f'{self.x_values[-1]:.2f}_Y_{self.dim_2}_'
                         f'{(self.y_values[0]):.2f}-{(self.y_values[-1]):.2f}.png')

    def compute_values(self):
        """
        Compute the values for the x and y axes, as well as the contour values and labels.

        :return: None
        """
        # x and y axes values meshgrid
        self.X, self.Y = np.meshgrid(self.x_values, self.y_values)

        # calculate corresponding Z values
        # calculate contour values
        # generate contour labels
        self.vals = calculate_z(self.formula, self.X, self.Y)
        self.hl = calculate_z(self.formula, self.X, self.Y)

    def check_ticks_in_range(self, ax):
        """
        :param ax: A matplotlib Axes object representing the plot on which to check the tick values.
        :return: None

        Checks if the tick values on the x-axis and y-axis of the given Axes object are within the data range of the
        plot. If any tick value is outside of the data range, a ValueError is raised.

        Example usage:
            fig, ax = plt.subplots()
            # Assume some plot is created on ax
            obj = SomeClass()
            obj.check_ticks_in_range(ax)
        """
        x_range = ax.get_xlim()
        y_range = ax.get_ylim()

        x_ticks_in_range = all(x_range[0] <= tick <= x_range[1] for tick in self.x_values)
        y_ticks_in_range = all(y_range[0] <= tick <= y_range[1] for tick in self.y_values)
        if self.verbose:
            print('x_ticks = ', [f'{tick:2f}' for tick in self.x_values])
            print('y_ticks = ', [f'{tick:2f}' for tick in self.y_values])

        if not x_ticks_in_range:
            raise ValueError(f"x-tick values are outside of data range! {x_range[0]}-{x_range[1]}")
        elif not y_ticks_in_range:
            raise ValueError(f"y-tick values are outside of data range! {y_range[0]}-{y_range[1]}")

    def create_diagram(self):
        """
        Creates a diagram using matplotlib and saves it as an image file.

        :return: None
        """
        # create matplotlib figure (size in inches)
        fig_01 = plt.figure(figsize=(FIGURE_SIZE, FIGURE_SIZE))
        fig_01.suptitle(f'{self.title}', fontsize=TITLE_FONTSIZE, fontweight=TITLE_FONTWEIGHT)
        dia = fig_01.add_subplot(111)
        dia.grid(True)  # show grid lines
        # create diagram as subplot of fig_01
        # click.group() = c: xticks: self.y_values = frequency [Hz], yticks: self.x_values = R1 [Ω]

        """
        The tick labels on the x and y axes might not be appearing due to several reasons. Here're few suggestions 
        you can try: 

        Ensure that the values used for setting ticks (self.x_values and self.y_values) are within the 
        range of the axes. 

        Make sure the formatting of tick labels in the create_diagram function is correct for your 
        use case - especially the dynamic formatting based on the self.diagram_type. If the conditions in this 
        statement are not met, your code would not execute the set_yticklabels and this might be the reason tick 
        labels are not showing. 

        Try calling plt.show() at the end of your create_diagram function, just after 
        fig_01.savefig(self.filename, transparent=False). This will ensure the figure is displayed after all the 
        drawing commands. 

        The use of dia = fig_01.add_subplot(111, xticks=self.y_values, yticks=self.x_values, 
        xscale='log') might be causing problems. Instead, you could create your subplot using the default values and 
        change xticks and yticks later with dia.set_xticks(self.y_values) and dia.set_yticks(self.x_values)."""
        # dia = fig_01.add_subplot(111, xticks=self.y_values, yticks=self.x_values, xscale='log')

        # format the x-ticks and y-ticks of diagram
        for axis in [dia.xaxis]:
            axis.set_major_formatter(ScalarFormatter())  # display major tick values as regular decimal numbers
            axis.set_minor_formatter(NullFormatter())  # no labels at the minor ticks of the axis

        # assign x- yticks to x- y_values
        # use set_xticks or FixedLocator before set_x / xticklabels
        # use set_yticks or FixedLocator before set_y / yticklabels
        dia.set_xticks(self.x_values)
        dia.set_yticks(self.y_values)

        dia.set_xlim(min(self.x_values), max(self.x_values))
        dia.set_ylim(min(self.y_values), max(self.y_values))

        # generate y-ticks for Capacitor contour
        xticks = dia.get_xticks()
        yticks = dia.get_yticks()
        # formatting numpy array xticks and yticks with Pint
        xticks_with_unit = xticks * self.base_unit_1
        yticks_with_unit = yticks * self.base_unit_2

        # generate x - yticklabels
        dia.set_xticklabels([f'{tick.to(self.dim_1).magnitude:.2f}' for tick in xticks_with_unit])
        dia.set_yticklabels([f'{tick.to(self.dim_2).magnitude:.2f}' for tick in yticks_with_unit])

        if self.verbose:
            print('xticklabels = ', [f'{tick.to(self.dim_1):~P.2f}' for tick in xticks_with_unit])
            print('yticklabels = ', [f'{tick.to(self.dim_2):~P.2f}' for tick in yticks_with_unit])

        self.check_ticks_in_range(dia)

        # Set labels and title
        # self.min_1 = Q_(min_1, dim_1)
        dia.set_title(f"{self.formula} [{self.unity_res.units:~P}]", fontsize=14, fontweight='bold')
        dia.set_xlabel(self.label_x, fontsize=14, fontweight='bold')
        dia.set_ylabel(self.label_y, fontsize=14, fontweight='bold')
        plt.xticks(rotation=70)
        plt.yticks()

        # generate contour plot
        img = dia.contourf(self.X, self.Y, self.vals, 35, zorder=0, cmap='Spectral')

        # scale the clabel values to self.dim_res
        hl_with_unit = self.vals * self.unity_res
        scaled_hl_with_unit = hl_with_unit.to(self.dim_res)
        hl_scale_factor = hl_with_unit[0, 0].magnitude / scaled_hl_with_unit[0, 0].magnitude
        # plot scaled clabel values
        self.hl = dia.contour(self.X, self.Y, self.vals / hl_scale_factor, 35, zorder=0, colors='black')
        plt.clabel(self.hl, inline=1, fontsize=12, fmt=lambda x: f"{x:.2f}")

        print(f"diagram_name: {self.filename}")

        # plot and store fig_01
        plt.show()
        fig_01.savefig(self.filename, transparent=False)

    def run(self):
        """
        This method runs the main process of the software.

        :return: None
        """
        self.initialize_values()
        self.initialize_dimension_one_values()
        self.initialize_dimension_two_values()
        self.initialize_diagram_labels()
        self.set_values_for_contour_calc_with_scalars_scaled_to_base_units()
        self.filename_for_saved_contour_figure()
        self.compute_values()
        self.create_diagram()
        # plt.show()


@click.command()
@click.argument('title', type=str)
@click.argument('x_label', type=str)
@click.argument('y_label', type=str)
@click.argument('formula', type=str)
@click.argument('z_dim', type=str)
@click.argument('x_start', type=float)
@click.argument('x_stop', type=float)
@click.argument('x_step', type=float)
@click.argument('x_dim', type=str)
@click.argument('y_min', type=float)
@click.argument('y_max', type=float)
@click.argument('y_step', type=float)
@click.argument('y_dim', type=str)
@click.argument('swap_axes', type=str)
@click.option('--verbose', '-v', default=False, help='print verbose information on screen')
def c(title, x_label, y_label, formula, z_dim, x_start, x_stop, x_step, x_dim, y_min, y_max, y_step, y_dim, swap_axes,
      verbose):
    """

    :param title: The title of the contour plot
    :param x_label: The label of the x-axis
    :param y_label: The label of the y-axis
    :param formula: The mathematical formula used to generate the contour plot
    :param z_dim: The dimension of the z-axis
    :param x_start: The starting value of the x-axis
    :param x_stop: The stopping value of the x-axis
    :param x_step: The step size of the x-axis
    :param x_dim: The dimension of the x-axis values
    :param y_min: The minimum value of the y-axis
    :param y_max: The maximum value of the y-axis
    :param y_step: The step size of the y-axis
    :param y_dim: The dimension of the y-axis values
    :param swap_axes: The flag indicating whether to swap the x and y axes
    :param verbose: The flag indicating whether to print verbose information on the screen
    :return: None

    """
    click.echo(
        f"Running --c with title {title}, x_label {x_label}, y_label {y_label}, formula {formula}, x_start {x_start}, "
        f"x_stop {x_stop}, x_step {x_step}, x_dim {x_dim}, y_min {y_min}, y_max {y_max}, y_step {y_step}, "
        f"y_dim {y_dim}, swap_axes {swap_axes}, verbose {verbose}")
    label_x_dimension = Q_(1, x_dim).units
    label_y_dimension = Q_(1, y_dim).units
    x_label = f"{x_label} [{label_x_dimension:~P}]"
    y_label = f"{y_label} [{label_y_dimension:~P}]"
    c_c = Contour(title, x_label, y_label, formula, z_dim, y_min, y_max, y_step, y_dim, x_start, x_stop, x_step, x_dim,
                  swap_axes, verbose)
    c_c.run()


if __name__ == '__main__':
    c()
