# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/v1/timeline.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x61pi/v1/timeline.proto\x12\x06\x61pi.v1\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\" \n\rHelloResponse\x12\x0f\n\x07message\x18\x01 \x01(\t\"$\n\x16SubjectCollectResponse\x12\n\n\x02ok\x18\x01 \x01(\x08\"%\n\x17SubjectProgressResponse\x12\n\n\x02ok\x18\x01 \x01(\x08\"$\n\x16\x45pisodeCollectResponse\x12\n\n\x02ok\x18\x01 \x01(\x08\"\x9c\x01\n\x07Subject\x12\n\n\x02id\x18\x01 \x01(\r\x12\x10\n\x04type\x18\x02 \x01(\rB\x02\x18\x01\x12\x10\n\x04name\x18\x03 \x01(\tB\x02\x18\x01\x12\x13\n\x07name_cn\x18\x04 \x01(\tB\x02\x18\x01\x12\x11\n\x05image\x18\x05 \x01(\tB\x02\x18\x01\x12\x12\n\x06series\x18\x06 \x01(\x08\x42\x02\x18\x01\x12\x12\n\nvols_total\x18\x07 \x01(\r\x12\x11\n\teps_total\x18\x08 \x01(\r\"`\n\x07\x45pisode\x12\n\n\x02id\x18\x01 \x01(\r\x12\x10\n\x04type\x18\x02 \x01(\rB\x02\x18\x01\x12\x10\n\x04name\x18\x03 \x01(\tB\x02\x18\x01\x12\x13\n\x07name_cn\x18\x04 \x01(\tB\x02\x18\x01\x12\x10\n\x04sort\x18\x05 \x01(\x01\x42\x02\x18\x01\"\x94\x01\n\x15SubjectCollectRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12 \n\x07subject\x18\x02 \x01(\x0b\x32\x0f.api.v1.Subject\x12\x12\n\ncollection\x18\x03 \x01(\r\x12\x0f\n\x07\x63omment\x18\x04 \x01(\t\x12\x0c\n\x04rate\x18\x05 \x01(\r\x12\x15\n\rcollection_id\x18\x06 \x01(\x04\"i\n\x15\x45pisodeCollectRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12\x1d\n\x04last\x18\x02 \x01(\x0b\x32\x0f.api.v1.Episode\x12 \n\x07subject\x18\x03 \x01(\x0b\x32\x0f.api.v1.Subject\"t\n\x16SubjectProgressRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x04\x12 \n\x07subject\x18\x02 \x01(\x0b\x32\x0f.api.v1.Subject\x12\x12\n\neps_update\x18\x03 \x01(\r\x12\x13\n\x0bvols_update\x18\x04 \x01(\r2\xc5\x02\n\x0fTimeLineService\x12\x36\n\x05Hello\x12\x14.api.v1.HelloRequest\x1a\x15.api.v1.HelloResponse\"\x00\x12Q\n\x0eSubjectCollect\x12\x1d.api.v1.SubjectCollectRequest\x1a\x1e.api.v1.SubjectCollectResponse\"\x00\x12T\n\x0fSubjectProgress\x12\x1e.api.v1.SubjectProgressRequest\x1a\x1f.api.v1.SubjectProgressResponse\"\x00\x12Q\n\x0e\x45pisodeCollect\x12\x1d.api.v1.EpisodeCollectRequest\x1a\x1e.api.v1.EpisodeCollectResponse\"\x00\x42\x1fZ\x1dgithub.com/bangumi/server/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.v1.timeline_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\035github.com/bangumi/server/api'
  _globals['_SUBJECT'].fields_by_name['type']._loaded_options = None
  _globals['_SUBJECT'].fields_by_name['type']._serialized_options = b'\030\001'
  _globals['_SUBJECT'].fields_by_name['name']._loaded_options = None
  _globals['_SUBJECT'].fields_by_name['name']._serialized_options = b'\030\001'
  _globals['_SUBJECT'].fields_by_name['name_cn']._loaded_options = None
  _globals['_SUBJECT'].fields_by_name['name_cn']._serialized_options = b'\030\001'
  _globals['_SUBJECT'].fields_by_name['image']._loaded_options = None
  _globals['_SUBJECT'].fields_by_name['image']._serialized_options = b'\030\001'
  _globals['_SUBJECT'].fields_by_name['series']._loaded_options = None
  _globals['_SUBJECT'].fields_by_name['series']._serialized_options = b'\030\001'
  _globals['_EPISODE'].fields_by_name['type']._loaded_options = None
  _globals['_EPISODE'].fields_by_name['type']._serialized_options = b'\030\001'
  _globals['_EPISODE'].fields_by_name['name']._loaded_options = None
  _globals['_EPISODE'].fields_by_name['name']._serialized_options = b'\030\001'
  _globals['_EPISODE'].fields_by_name['name_cn']._loaded_options = None
  _globals['_EPISODE'].fields_by_name['name_cn']._serialized_options = b'\030\001'
  _globals['_EPISODE'].fields_by_name['sort']._loaded_options = None
  _globals['_EPISODE'].fields_by_name['sort']._serialized_options = b'\030\001'
  _globals['_HELLOREQUEST']._serialized_start=33
  _globals['_HELLOREQUEST']._serialized_end=61
  _globals['_HELLORESPONSE']._serialized_start=63
  _globals['_HELLORESPONSE']._serialized_end=95
  _globals['_SUBJECTCOLLECTRESPONSE']._serialized_start=97
  _globals['_SUBJECTCOLLECTRESPONSE']._serialized_end=133
  _globals['_SUBJECTPROGRESSRESPONSE']._serialized_start=135
  _globals['_SUBJECTPROGRESSRESPONSE']._serialized_end=172
  _globals['_EPISODECOLLECTRESPONSE']._serialized_start=174
  _globals['_EPISODECOLLECTRESPONSE']._serialized_end=210
  _globals['_SUBJECT']._serialized_start=213
  _globals['_SUBJECT']._serialized_end=369
  _globals['_EPISODE']._serialized_start=371
  _globals['_EPISODE']._serialized_end=467
  _globals['_SUBJECTCOLLECTREQUEST']._serialized_start=470
  _globals['_SUBJECTCOLLECTREQUEST']._serialized_end=618
  _globals['_EPISODECOLLECTREQUEST']._serialized_start=620
  _globals['_EPISODECOLLECTREQUEST']._serialized_end=725
  _globals['_SUBJECTPROGRESSREQUEST']._serialized_start=727
  _globals['_SUBJECTPROGRESSREQUEST']._serialized_end=843
  _globals['_TIMELINESERVICE']._serialized_start=846
  _globals['_TIMELINESERVICE']._serialized_end=1171
# @@protoc_insertion_point(module_scope)
