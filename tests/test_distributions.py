import unittest


import numpy as np

from .context import viroconcom

from viroconcom.params import ConstantParam, FunctionParam
from viroconcom.distributions import (WeibullDistribution, LognormalDistribution, NormalDistribution,
                                   KernelDensityDistribution,
                                   MultivariateDistribution)

class MultivariateDistributionTest(unittest.TestCase):
    """
    Create an example MultivariateDistribution (Vanem2012 model).
    """

    # Define dependency tuple.
    dep1 = (None, 0, None)
    dep2 = (0, None, 0)

    # Define parameters.
    shape = ConstantParam(1.471)
    loc = ConstantParam(0.8888)
    scale = ConstantParam(2.776)
    par1 = (shape, loc, scale)

    shape = FunctionParam(0.0400, 0.1748, -0.2243, "exp3")
    loc = None
    scale = FunctionParam(0.1, 1.489, 0.1901, "power3")
    par2 = (shape, loc, scale)

    del shape, loc, scale

    # Create distributions.
    dist1 = WeibullDistribution(*par1)
    dist2 = LognormalDistribution(*par2)

    distributions = [dist1, dist2]
    dependencies = [dep1, dep2]


    def test_add_distribution_err_msg(self):
        """
        Tests if the right exception is raised when distribution1 has a
        dependency.
        """

        with self.assertRaises(ValueError):
            MultivariateDistribution(self.distributions, self.dependencies)


    def test_add_distribution_iter(self):
        """
        Tests if an exception is raised by the function add_distribution when
        distributions isn't iterable but dependencies is and the other way around.
        """

        distributions = 1
        with self.assertRaises(ValueError):
            MultivariateDistribution(distributions, self.dependencies)
        dependencies = 0
        with self.assertRaises(ValueError):
            MultivariateDistribution(self.distributions, dependencies)

    def test_add_distribution_length(self):
        """
        Tests if an exception is raised when distributions and dependencies
        are of unequal length.
        """

        dep3 = (0, None, None)
        dependencies = [self.dep1, self.dep2, dep3]
        with self.assertRaises(ValueError):
            MultivariateDistribution(self.distributions, dependencies)

    def test_add_distribution_dependencies_length(self):
        """
        Tests if an exception is raised when a tuple in dependencies
        has not length 3.
        """

        dep1 = (None, None)
        dependencies = [dep1, self.dep2]
        with self.assertRaises(ValueError):
            MultivariateDistribution(self.distributions, dependencies)

    def test_add_distribution_dependencies_value(self):
        """
        Tests if an exception is raised when dependencies has an invalid value.
        """

        dep1 = (-3, None, None)
        dependencies = [dep1, self.dep2]
        with self.assertRaises(ValueError):
            MultivariateDistribution(self.distributions, dependencies)



    def test_add_distribution_not_iterable(self):
        """
        Tests the function when both distributions and dependencies
        are not iterable.
        """

        distributions = 1
        dependencies = 2
        with self.assertRaises(ValueError):
            MultivariateDistribution(distributions, dependencies)

    def test_latex_representation(self):
        """
        Tests if the latex representation is correct.
        """
        dep1 = (None, None, None)
        dep2 = (0, None, 0)
        dependencies = [dep1, dep2]
        m = MultivariateDistribution(self.distributions, dependencies)
        computed_latex = m.latex_repr(['Hs', 'Tp'])
        correct_latex = \
            ['\\text{ joint PDF: }',
             'f(h_{s},t_{p})=f_{H_{s}}(h_{s})f_{T_{p}|H_{s}}(t_{p}|h_{s})',
             '',
             '1\\text{. variable, }H_{s}: ',
             'f_{H_{s}}(h_{s})=\\dfrac{\\beta_{h_{s}}}{\\alpha_{h_{s}}}'
             '\\left(\\dfrac{h_{s}-\\gamma_{h_{s}}}{\\alpha_{h_{s}}}'
             '\\right)^{\\beta_{h_{s}}-1}\\exp\\left[-\\left(\\dfrac{h_{s}-'
             '\\gamma_{h_{s}}}{\\alpha_{h_{s}}}\\right)^{\\beta_{h_{s}}}\\right]',
             '\\quad\\text{ with }\\alpha_{h_{s}}=2.776,',
             '\\quad\\qquad\\;\\; \\beta_{h_{s}}=1.471,',
             '\\quad\\qquad\\;\\; \\gamma_{h_{s}}=0.8888.',
             '',
             '2\\text{. variable, }T_{p}: ',
             'f_{T_{p}|H_{s}}(t_{p}|h_{s})=\\dfrac{1}{t_{p}\\tilde{\\sigma}_'
             '{t_{p}}\\sqrt{2\\pi}}\\exp\\left[-\\dfrac{(\\ln t_{p}-\\tilde{'
             '\\mu}_{t_{p}})^2}{2\\tilde{\\sigma}_{t_{p}}^2}\\right]',
             '\\quad\\text{ with }\\exp{\\tilde{\\mu}}_{t_{p}}='
             '0.1+1.489h_{s}^{0.1901},',
             '\\quad\\qquad\\;\\; \\tilde{\\sigma}_{t_{p}}='
             '0.04+0.1748e^{-0.2243h_{s}}.']
        assert(computed_latex, correct_latex)


class ParametricDistributionTest(unittest.TestCase):

    def test_distribution_shape_None(self):
        """
        Tests if shape is set to default when it has value 'None'.
        """

        # Define parameters.
        shape = None
        loc = ConstantParam(0.8888)
        scale = ConstantParam(2.776)
        par1 = (shape, loc, scale)
        rv_values = [0.8, 1, 8]
        dependencies = (0, 1, 1)

        dist = NormalDistribution(*par1)
        shape_test = dist._get_parameter_values(rv_values, dependencies)[0]
        self.assertEqual(shape_test, 1)


    def test_distribution_loc_None(self):
        """
        Tests if loc is set to default when it has value 'None'.
        """

        # Define parameters.
        shape = ConstantParam(0.8888)
        loc = None
        scale = ConstantParam(2.776)
        par1 = (shape, loc, scale)
        rv_values = [0.8, 1, 8]
        dependencies = (0, 1, 1)

        dist = WeibullDistribution(*par1)
        loc_test = dist._get_parameter_values(rv_values, dependencies)[1]
        self.assertEqual(loc_test, 0)


    def test_distribution_loc_scale(self):
        """
        Tests if scale is set to default when it has value 'None'.
        """

        # Define parameters.
        shape = ConstantParam(0.8888)
        loc = ConstantParam(2.776)
        scale = None
        par1 = (shape, loc, scale)
        rv_values = [0.8, 1, 8]
        dependencies = (0, 1, 1)

        dist = NormalDistribution(*par1)
        scale_test = dist._get_parameter_values(rv_values, dependencies)[2]
        self.assertEqual(scale_test, 1)


    def test_check_parameter_value(self):
        """
        Tests if the right exception is raised when the given parameters are
        not in the valid range of numbers.
        """

        shape = None
        loc = ConstantParam(0.8888)
        scale = ConstantParam(-2.776)
        par1 = (shape, loc, scale)

        dist = WeibullDistribution(*par1)

        with self.assertRaises(ValueError):
            dist._check_parameter_value(2, -2.776)
        with self.assertRaises(ValueError):
            dist._check_parameter_value(2, np.inf)


if __name__ == '__main__':
    unittest.main()