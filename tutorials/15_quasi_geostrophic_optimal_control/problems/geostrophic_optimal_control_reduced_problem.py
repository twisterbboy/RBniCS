# Copyright (C) 2015-2022 by the RBniCS authors
#
# This file is part of RBniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from rbnics.backends import product, sum, transpose
from rbnics.problems.base import LinearReducedProblem


def GeostrophicOptimalControlReducedProblem(ParametrizedReducedDifferentialProblem_DerivedClass):

    GeostrophicOptimalControlReducedProblem_Base = LinearReducedProblem(
        ParametrizedReducedDifferentialProblem_DerivedClass)

    class GeostrophicOptimalControlReducedProblem_Class(GeostrophicOptimalControlReducedProblem_Base):

        class ProblemSolver(GeostrophicOptimalControlReducedProblem_Base.ProblemSolver):
            def matrix_eval(self):
                problem = self.problem
                N = self.N
                assembled_operator = dict()
                for term in ("a", "a*", "c", "c*", "m", "n"):
                    assembled_operator[term] = sum(product(problem.compute_theta(term), problem.operator[term][:N, :N]))
                return (assembled_operator["m"] + assembled_operator["a*"]
                        + assembled_operator["n"] - assembled_operator["c*"]
                        + assembled_operator["a"] - assembled_operator["c"])

            def vector_eval(self):
                problem = self.problem
                N = self.N
                assembled_operator = dict()
                for term in ("f", "g"):
                    assembled_operator[term] = sum(product(problem.compute_theta(term), problem.operator[term][:N]))
                return (assembled_operator["g"]
                        + assembled_operator["f"])

        # Perform an online evaluation of the cost functional
        def _compute_output(self, N):
            assembled_operator = dict()
            for term in ("m", "n", "g", "h"):
                assert self.terms_order[term] in (0, 1, 2)
                if self.terms_order[term] == 2:
                    assembled_operator[term] = sum(product(self.compute_theta(term), self.operator[term][:N, :N]))
                elif self.terms_order[term] == 1:
                    assembled_operator[term] = sum(product(self.compute_theta(term), self.operator[term][:N]))
                elif self.terms_order[term] == 0:
                    assembled_operator[term] = sum(product(self.compute_theta(term), self.operator[term]))
                else:
                    raise ValueError("Invalid value for order of term " + term)
            self._output = (0.5 * (transpose(self._solution) * assembled_operator["m"] * self._solution)
                            + 0.5 * (transpose(self._solution) * assembled_operator["n"] * self._solution)
                            - transpose(assembled_operator["g"]) * self._solution
                            + 0.5 * assembled_operator["h"])

        def _online_size_from_kwargs(self, N, **kwargs):
            if N is None:
                # then either,
                # * the user has passed kwargs, so we trust that he/she has doubled y and p for us
                # * or self.N was copied, which already stores the correct count of basis functions
                return GeostrophicOptimalControlReducedProblem_Base._online_size_from_kwargs(self, N, **kwargs)
            else:
                # then the integer value provided to N would be used for all components: need to double
                # it for y and p
                N, kwargs = GeostrophicOptimalControlReducedProblem_Base._online_size_from_kwargs(self, N, **kwargs)
                for component in ("ypsi", "yq", "ppsi", "pq"):
                    N[component] *= 2
                return N, kwargs

    return GeostrophicOptimalControlReducedProblem_Class
