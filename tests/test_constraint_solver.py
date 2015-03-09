#
# Copyright (C) 2015 Christopher Bura
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA
#

from nose.tools import assert_equal, assert_raises, assert_false, assert_true, raises
from cassowary import RequiredFailure

from pythoncad.new_api import Drawing, Layer, Point, Segment
from pythoncad.new_api import HorizontalConstraint, VerticalConstraint, FixedConstraint, LengthConstraint
from pythoncad.new_api import HorizontalLengthConstraint

def test_solver():
    drawing = Drawing()

    layer = Layer(title='Layer')
    drawing.add_layer(layer)

    point1 = Point(0, 0)
    point2 = Point(5, 5)
    layer.add_entity(point1)
    layer.add_entity(point2)

    constraint = HorizontalConstraint(point1, point2)
    drawing.add_constraint(constraint)

    assert_false(point1.y == point2.y)

    drawing.solve()
    drawing.update()

    assert_true(point1.y == point2.y)

    constraint2 = VerticalConstraint(point1, point2)
    drawing.add_constraint(constraint2)

    assert_false(point1.x == point2.x)

    drawing.solve()
    drawing.update()

    assert_true(point1.x == point2.x)

    assert_equal(point1.x, 0)
    assert_equal(point1.y, 0)
    assert_equal(point2.x, 0)
    assert_equal(point2.y, 0)

@raises(RequiredFailure)
def test_fixed_constraint():
    drawing = Drawing()

    layer = Layer(title='Layer')
    drawing.add_layer(layer)

    point1 = Point(0, 0)
    point2 = Point(5, 5)
    layer.add_entity(point1)
    layer.add_entity(point2)

    drawing.add_constraint(FixedConstraint(point1))
    drawing.add_constraint(FixedConstraint(point2))
    drawing.add_constraint(HorizontalConstraint(point1, point2))

    drawing.solve()

def test_horizontal_segment():
    drawing = Drawing()

    layer = Layer(title='Layer')
    drawing.add_layer(layer)

    segment = Segment(Point(0, 0), Point(5, 5))
    layer.add_entity(segment)

    constraint = HorizontalConstraint(segment)
    drawing.add_constraint(constraint)

    assert_false(segment.p1.y == segment.p2.y)

    drawing.solve()
    drawing.update()

    assert_true(segment.p1.y == segment.p2.y)

def test_length_constraint():
    drawing = Drawing()
    layer = Layer(title='Layer')
    drawing.add_layer(layer)

    point1 = Point(10, 10)
    point2 = Point(20, 20)
    layer.add_entity(point1)
    layer.add_entity(point2)

    horizontal_constraint = HorizontalConstraint(point1, point2)
    drawing.add_constraint(horizontal_constraint)

    drawing.solve()
    drawing.update()

    assert_true(point1.y == point2.y)

    length_constraint = LengthConstraint(point1, point2, 50)
    drawing.add_constraint(length_constraint)

    drawing.solve()
    drawing.update()

    assert_true(point2.x == 60)

def test_horizontal_length_constraint():
    drawing = Drawing()
    layer = Layer(title='Layer')
    drawing.add_layer(layer)

    point1 = Point(10, 10)
    point2 = Point(20, 20)
    layer.add_entity(point1)
    layer.add_entity(point2)

    horizontal_constraint = HorizontalConstraint(point1, point2)
    drawing.add_constraint(horizontal_constraint)

    drawing.solve()
    drawing.update()

    assert_true(point1.y == point2.y)

    length_constraint = HorizontalLengthConstraint(point1, point2, 50)
    drawing.add_constraint(length_constraint)

    drawing.solve()
    drawing.update()

    assert_true(point2.x == 60)
