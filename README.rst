Products.PFGMasterSelect
========================

.. contents::

An add-on field for PloneFormGen using the MasterSelect widget.

Features
--------

Installation
------------

How to use
----------
Please note that PloneFormGen's QuickEdit mode does not work (yet) for this add-on.

After installing this product you can create the Master Select
and Master Multiselect fields via the "Add new..." menu in a PloneFormGen form.
Both fields allow you to specify a default value and the options available as the
common selection field does.

Additionally it provides a configuration table that contains the MasterSelect
configuration (see also MasterSelectWidget documentation for more detail):

``name`` (required)
    The target field's name
``action`` (required)
    The action to be applied on the target field. The options are
    * show/enable: Show/Enable the target field only if toggle_method evaluates to True or the field's value is in hide_value
    * hide/disable: Hide/disable the target field if toggle_method evaluates to True or the field's value is in hide_values
    * value: Set the target field's value to the result of the vocab_method
    * vocabulary: Set the target field's vocabulary to the result of the vocab_method
``vocab_method``
    A python expression evaluating to a single value or collection. The currently set value (MasterSelect) or
    values (MasterMultiSelect) are available via ``value`` and ``values`` respectively.
    Example: Set the vocabulary of a selection field using ``['xyz' + v for v in values]``
``toggle_method``
    A python expression evaluating to a boolean value. This method takes precedence to hide_values. The currently set
    value (MasterSelect) or values (MasterMultiSelect) are available via ``value`` and ``values`` respectively.
    Example: Hide a field if the selected value has length 5 or equals ``foo`` using ``len(value) == 5 or value == 'foo'``
``hide_values``
    The values that show/hide/enable/disable operate on
    Example: Hide a field if the selected value is ``a`` or ``b`` using ``a,b``
