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


from sympy.geometry import Point, Segment, Circle


class Drawing(object):
    def __init__(self, title='', *args, **kwargs):
        super(Drawing, self).__init__(*args, **kwargs)
        self.title = title
        self.layers = []

    @property
    def layer_count(self):
        return len(self.layers)

    def add_layer(self, layer):
        # Remove layer from any existing drawing
        try:
            layer.drawing.remove_layer(layer)
        except AttributeError:
            pass

        self.layers.append(layer)
        layer.drawing = self

    def remove_layer(self, layer):
        try:
            self.layers.remove(layer)
            layer.drawing = None
        except ValueError:
            # Layer not part of this drawing
            pass

    def filter_layers(self, layers, exclude):
        # If no layers are specified then filter them all
        if layers is None:
            layers = self.layers
        return [layer for layer in layers if layer not in exclude]

    def hide_layers(self, layers=None, exclude=[]):
        for layer in self.filter_layers(layers, exclude):
            layer.hide()

    def show_layers(self, layers=None, exclude=[]):
        for layer in self.filter_layers(layers, exclude):
            layer.show()

    def isolate_layer(self, layer):
        """
        Shows a single layer while setting all others to hidden
        """
        # Show and then hide with exclude to prevent possible flickering of
        # entities on layer when used with a gui
        layer.show()
        self.hide_layers(exclude=[layer])


class Layer(object):
    def __init__(self, title='', *args, **kwargs):
        super(Layer, self).__init__(*args, **kwargs)
        self.title = title
        self.drawing = None
        self.entities = []
        self.visible = True

    @property
    def entity_count(self):
        return len(self.entities)

    # def is_bound(self):
        # pass

    def add_entity(self, entity):
        # Remove entity from any existing layer
        try:
            entity.layer.remove_entity(entity)
        except AttributeError:
            pass

        self.entities.append(entity)
        entity.layer = self

    def remove_entity(self, entity):
        try:
            self.entities.remove(entity)
            entity.layer = None
        except ValueError:
            # Entity is not bound to this layer
            pass

    def hide(self):
        """
        Hides layer without hiding each individual entity. Allows a layer to be
        temporarily hidden without affecting the previous state.
        """
        self.visible = False

    def show(self):
        self.visible = True

    # TODO: Mixin? Shared with drawing
    def filter_entities(self, entities, exclude):
        # If no entities are specified then filter them all
        if entities is None:
            entities = self.entities
        return [entity for entity in entities if entity not in exclude]

    def hide_entities(self, entities=None, exclude=[]):
        for entity in self.filter_entities(entities, exclude):
            entity.hide()

    def show_entities(self, entities=None, exclude=[]):
        for entity in self.filter_entities(entities, exclude):
            entity.show()


class LayerEntity(object):
    def __init__(self, *args, **kwargs):
        self.layer = None
        self.visible = True

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True

    def is_visible(self):
        """
        Tests whether the object is currently visible on the scene. Entities
        can be hidden individually or the entire layer can be hidden.
        """
        if self.visible and self.layer.visible:
            return True
        return False


class Point(LayerEntity, Point):
    pass


class Segment(LayerEntity, Segment):
    pass


class Circle(LayerEntity, Circle):
    pass
