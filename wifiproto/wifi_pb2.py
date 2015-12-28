# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: wifi.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='wifi.proto',
  package='wifiproto',
  serialized_pb=_b('\n\nwifi.proto\x12\twifiproto\"{\n\x06Packet\x12\x0f\n\x07\x61rrival\x18\x01 \x01(\x01\x12\x0f\n\x07subtype\x18\x02 \x01(\t\x12\x0c\n\x04ssid\x18\x03 \x01(\t\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65stination\x18\x05 \x01(\t\x12\x0c\n\x04\x66req\x18\x06 \x01(\x05\x12\x0e\n\x06signal\x18\x07 \x01(\x05\"L\n\x07Payload\x12\x10\n\x08location\x18\x01 \x01(\t\x12\x0e\n\x06sensor\x18\x02 \x01(\t\x12\x1f\n\x04\x64\x61ta\x18\x03 \x03(\x0b\x32\x11.wifiproto.Packet')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PACKET = _descriptor.Descriptor(
  name='Packet',
  full_name='wifiproto.Packet',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='arrival', full_name='wifiproto.Packet.arrival', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subtype', full_name='wifiproto.Packet.subtype', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ssid', full_name='wifiproto.Packet.ssid', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='source', full_name='wifiproto.Packet.source', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='destination', full_name='wifiproto.Packet.destination', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='freq', full_name='wifiproto.Packet.freq', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='signal', full_name='wifiproto.Packet.signal', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=25,
  serialized_end=148,
)


_PAYLOAD = _descriptor.Descriptor(
  name='Payload',
  full_name='wifiproto.Payload',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='location', full_name='wifiproto.Payload.location', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sensor', full_name='wifiproto.Payload.sensor', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='wifiproto.Payload.data', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=150,
  serialized_end=226,
)

_PAYLOAD.fields_by_name['data'].message_type = _PACKET
DESCRIPTOR.message_types_by_name['Packet'] = _PACKET
DESCRIPTOR.message_types_by_name['Payload'] = _PAYLOAD

Packet = _reflection.GeneratedProtocolMessageType('Packet', (_message.Message,), dict(
  DESCRIPTOR = _PACKET,
  __module__ = 'wifi_pb2'
  # @@protoc_insertion_point(class_scope:wifiproto.Packet)
  ))
_sym_db.RegisterMessage(Packet)

Payload = _reflection.GeneratedProtocolMessageType('Payload', (_message.Message,), dict(
  DESCRIPTOR = _PAYLOAD,
  __module__ = 'wifi_pb2'
  # @@protoc_insertion_point(class_scope:wifiproto.Payload)
  ))
_sym_db.RegisterMessage(Payload)


# @@protoc_insertion_point(module_scope)
