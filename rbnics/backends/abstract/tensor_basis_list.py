# Copyright (C) 2015-2022 by the RBniCS authors
#
# This file is part of RBniCS.
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from rbnics.backends.abstract.tensors_list import TensorsList
from rbnics.utils.decorators import AbstractBackend


@AbstractBackend
class TensorBasisList(TensorsList):
    pass
