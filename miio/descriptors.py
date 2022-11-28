"""This module contains descriptors.

The descriptors contain information that can be used to provide generic, dynamic user-interfaces.

If you are a downstream developer, use :func:`~miio.device.Device.sensors()`,
:func:`~miio.device.Device.settings()`, and
:func:`~miio.device.Device.actions()` to access the functionality exposed by the integration developer.

If you are developing an integration, prefer :func:`~miio.devicestatus.sensor`, :func:`~miio.devicestatus.setting`, and
:func:`~miio.devicestatus.action` decorators over creating the descriptors manually.
If needed, you can override the methods listed to add more descriptors to your integration.
"""
from enum import Enum, auto
from typing import Callable, Dict, Optional, Type

import attr


@attr.s(auto_attribs=True)
class ValidSettingRange:
    """Describes a valid input range for a setting."""

    min_value: int
    max_value: int
    step: int = 1


@attr.s(auto_attribs=True)
class ActionDescriptor:
    """Describes a button exposed by the device."""

    id: str
    name: str
    method_name: Optional[str] = attr.ib(default=None, repr=False)
    method: Optional[Callable] = attr.ib(default=None, repr=False)
    extras: Dict = attr.ib(factory=dict, repr=False)


@attr.s(auto_attribs=True)
class SensorDescriptor:
    """Describes a sensor exposed by the device.

    This information can be used by library users to programatically
    access information what types of data is available to display to users.

    Prefer :meth:`@sensor <miio.devicestatus.sensor>` for constructing these.
    """

    id: str
    type: type
    name: str
    property: str
    unit: Optional[str] = None
    extras: Dict = attr.ib(factory=dict, repr=False)


class SettingType(Enum):
    Undefined = auto()
    Number = auto()
    Boolean = auto()
    Enum = auto()


@attr.s(auto_attribs=True, kw_only=True)
class SettingDescriptor:
    """Presents a settable value."""

    id: str
    name: str
    property: str
    unit: Optional[str] = None
    type = SettingType.Undefined
    setter: Optional[Callable] = attr.ib(default=None, repr=False)
    setter_name: Optional[str] = attr.ib(default=None, repr=False)
    extras: Dict = attr.ib(factory=dict, repr=False)

    def cast_value(self, value: int):
        """Casts value to the expected type."""
        cast_map = {
            SettingType.Boolean: bool,
            SettingType.Enum: int,
            SettingType.Number: int,
        }
        return cast_map[self.type](int(value))


@attr.s(auto_attribs=True, kw_only=True)
class BooleanSettingDescriptor(SettingDescriptor):
    """Presents a settable boolean value."""

    type: SettingType = SettingType.Boolean


@attr.s(auto_attribs=True, kw_only=True)
class EnumSettingDescriptor(SettingDescriptor):
    """Presents a settable, enum-based value."""

    type: SettingType = SettingType.Enum
    choices_attribute: Optional[str] = attr.ib(default=None, repr=False)
    choices: Optional[Type[Enum]] = attr.ib(default=None, repr=False)


@attr.s(auto_attribs=True, kw_only=True)
class NumberSettingDescriptor(SettingDescriptor):
    """Presents a settable, numerical value.

    If `range_attribute` is set, the named property that should return
    :class:ValidSettingRange will be used to obtain {min,max}_value and step.
    """

    min_value: int
    max_value: int
    step: int
    range_attribute: Optional[str] = attr.ib(default=None)
    type: SettingType = SettingType.Number