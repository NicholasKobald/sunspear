from datetime import datetime
from sqlalchemy import Table, Column, DateTime, Integer, String, Text, MetaData, ForeignKey, UniqueConstraint
import types as custom_types


metadata = MetaData()

objects_table = Table('sgactivitystream_objects', metadata,
                      Column('id', String(32), primary_key=True),
                      Column('object_type', String(256), nullable=False),
                      Column('display_name', String(256), default=''),
                      Column('content', Text, default=''),
                      Column('published', DateTime(timezone=True), nullable=False),
                      Column('updated', DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now()),
                      Column('image', custom_types.JSONSmallDict(4096), default={}),
                      Column('other_data', custom_types.JSONDict(), default={}))

activities_table = Table('sgactivitystream_activities', metadata,
                         Column('id', String(32), primary_key=True),
                         Column('verb', String(256), nullable=False),
                         Column('actor_id', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE'), nullable=False),
                         Column('object_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('target_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('author_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('generator_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('provider_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('content', Text, default=''),
                         Column('published', DateTime(timezone=True), nullable=False),
                         Column('updated', DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now()),
                         Column('icon', custom_types.JSONSmallDict(4096), default={}),
                         Column('other_data', custom_types.JSONDict(), default={}))

replies_table = Table('replies', metadata,
                      Column('id', String(32), primary_key=True),
                      Column('in_reply_to', ForeignKey('sgactivitiystream_activities.id', ondelete='CASCADE'), nullable=False),
                      Column('actor', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE'), nullable=False),
                      Column('published', DateTime(timezone=True), nullable=False),
                      Column('updated', DateTime(timezone=True)),
                      Column('content', Text, nullable=False),
                      Column('other_data', custom_types.JSONDict()))

likes_table = Table('likes', metadata,
                    Column('id', String(32), primary_key=True),
                    Column('in_reply_to', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE'), nullable=False),
                    Column('actor', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE'), nullable=False),
                    Column('published', DateTime(timezone=True), nullable=False),
                    Column('content', Text),
                    Column('other_data', custom_types.JSONDict()),
                    UniqueConstraint('actor', 'in_reply_to'))

to_table = Table('to', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('object', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                 Column('activity', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

bto_table = Table('bto', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('object', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                  Column('activity', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

cc_table = Table('cc', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('object', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                 Column('activity', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

bcc_table = Table('bcc', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('object', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                  Column('activity', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

tables = {
    'objects': objects_table,
    'activities': activities_table,
    'replies': replies_table,
    'likes': likes_table,
    'to': to_table,
    'bto': bto_table,
    'cc': cc_table,
    'bcc': bcc_table,
}
