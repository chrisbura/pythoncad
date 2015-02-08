#
# Copyright (C) 2014 Christopher Bura
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

from nose.tools import assert_equal, assert_raises, assert_false, assert_true

from pythoncad.new_api import Drawing, Layer, Point, Segment


def test_drawing():
    drawing = Drawing(title='Gearbox')
    assert_equal(drawing.layer_count, 0)

    # Test Layer adding
    layer1 = Layer(title='1')
    layer2 = Layer(title='2')
    layer3 = Layer(title='3')
    layer4 = Layer(title='4')
    layer5 = Layer(title='5')

    drawing.add_layer(layer1)
    drawing.add_layer(layer2)

    assert_equal(drawing.layer_count, 2)

    drawing.add_layer(layer3)
    drawing.add_layer(layer4)
    drawing.add_layer(layer5)
    assert_equal(drawing.layer_count, 5)

    # Test Remove Layers
    drawing.remove_layer(layer1)
    assert_equal(drawing.layer_count, 4)

    drawing.add_layer(layer1)
    assert_equal(drawing.layer_count, 5)

    layer6 = Layer(title='Unbound Layer')
    assert_raises(ValueError, drawing.remove_layer(layer6))

    # Hide/Show layers
    drawing.hide_layers(exclude=[layer1, layer3, layer5])
    assert_false(layer2.visible)
    assert_false(layer4.visible)
    assert_true(layer1.visible)
    assert_true(layer3.visible)
    assert_true(layer5.visible)

    drawing.hide_layers()
    assert_false(layer1.visible)
    assert_false(layer3.visible)
    assert_false(layer5.visible)

    drawing.show_layers()
    assert_true(layer1.visible)
    assert_true(layer2.visible)
    assert_true(layer3.visible)
    assert_true(layer4.visible)
    assert_true(layer5.visible)

    drawing.isolate_layer(layer1)
    assert_true(layer1.visible)
    assert_false(layer2.visible)
    assert_false(layer3.visible)
    assert_false(layer4.visible)
    assert_false(layer5.visible)

def test_layer():
    drawing = Drawing()

    layer1 = Layer(title='1')
    drawing.add_layer(layer1)
    layer2 = Layer(title='2')
    drawing.add_layer(layer2)

    # Test adding entities
    point = Point(0, 0)
    layer1.add_entity(point)

    segment = Segment(Point(0, 0), Point(10, 10))
    layer2.add_entity(segment)

    assert_equal(layer1.entity_count, 1)
    assert_equal(layer2.entity_count, 1)

    assert_raises(ValueError, layer2.remove_entity(Point(0, 0)))

    layer2.add_entity(point)
    assert_equal(layer2.entity_count, 2)
    assert_equal(layer1.entity_count, 0)

    layer1.add_entity(segment)
    layer1.add_entity(point)
    assert_equal(layer1.entity_count, 2)

    # Entity Visibility
    layer2.add_entity(segment)
    layer2.hide()
    assert_true(point.is_visible())
    assert_false(segment.is_visible())
    layer2.show()
    assert_true(segment.is_visible())

    layer1.hide_entities()
    assert_true(layer1.visible)
    assert_false(point.is_visible())

    layer1.show_entities()
    assert_true(point.is_visible())
    layer1.hide_entities(exclude=[point])
    assert_true(point.is_visible())
