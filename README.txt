Introduction
============

uu.dynamicschema provides components for persistent objects in Plone applications
to use dynamically bound (form/field) schema interface objects.  It provides a means
of creating, using, managing, and persisting user-generated schema.  It is intended
to be used in conjunction with plone.schemaeditor in Plone, and was designed for use
in applications managing data objects that are not considered managed content in
themselves (they are usually fine-grained data elements of some content object).


Dependencies
============

Requires
--------

* zope.schema >= 3.8.0

* plone.supermodel

* plone.alterego

* plone.schemaeditor

* Plone 4+

Recommended
-----------

* Use in conjunction with Dexterity-based content types when managing
  non-content object elements related to or part of a content item.

--

Author: Sean Upton <sean.upton@hsc.utah.edu>

Copyright 2011, The University of Utah.

Released as free software under the GNU GPL version 2 license.
See doc/COPYING.txt

