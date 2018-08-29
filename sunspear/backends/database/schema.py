from datetime import datetime
from sqlalchemy import Table, Column, DateTime, Integer, String, Text, MetaData, ForeignKey, UniqueConstraint
import types as custom_types


metadata = MetaData()

objects_table = Table('sgactivitystream_streamobject', metadata,
                      Column('id', String(32), primary_key=True, nullable=True),
                      Column('object_type', String(256), nullable=False),
                      Column('display_name', String(256), default=''),
                      Column('sunspear_id', String(256), nullable=True),
                      Column('badge_id', ForeignKey('sgrecognition_badge.id', ondelete='SET NULL')),
                      Column('badgerecipient_id', ForeignKey('sgrecognition_badgerecipient.id', ondelete='SET NULL')),
                      Column('checkin_id', ForeignKey('sgcheckin_checkin.id', ondelete='SET NULL')),
                      Column('goal_id', ForeignKey('sggoals_goal.id', ondelete='SET NULL')),
                      Column('keyresult_id', ForeignKey('sggoals_kyresult.id', ondelete='SET NULL')),
                      Column('oneonone_id', ForeignKey('sgoneonone_oneonone.id', ondelete='SET NULL')),
                      Column('sgnetwork_id', ForeignKey('sgnetworks_sgnetwork.container_ptr_id', ondelete='SET NULL')),
                      Column('team_id', ForeignKey('sgteam_team.id', ondelete='SET NULL')),
                      Column('userprofile_id', ForeignKey('core_userprofile.id', ondelete='SET NULL')),
                      Column('content', Text, default=''),
                      Column('published', DateTime(timezone=True), nullable=False),
                      Column('updated', DateTime(timezone=True), default=datetime.now(), onupdate=datetime.now()),
                      Column('image', custom_types.JSONSmallDict(4096), default={}),
                      Column('other_data', custom_types.JSONDict(), default={}))

activities_table = Table('sgactivitystream_streamactivity', metadata,
                         Column('id', String(32), primary_key=True),
                         Column('verb', String(256), nullable=False),
                         Column('unique_verb', String(256), nullable=False),
                         Column('actor_id', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE'), nullable=False),
                         Column('object_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('target_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('author_id', ForeignKey('sgactivitystream_objects.id', ondelete='SET NULL')),
                         Column('sgnetwork_id', ForeignKey('sgnetworks_sgnetwork.container_ptr_id', ondelete='CASCADE'), nullable=True),
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

to_table = Table('sgactivitystream_to', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('obj_id', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                 Column('activity_id', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

bto_table = Table('sgactivitystream_bto', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('obj_id', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                  Column('activity_id', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

cc_table = Table('sgactivitystream_cc', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('obj_id', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                 Column('activity_id', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

bcc_table = Table('sgactivitystream_bcc', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('obj_id', ForeignKey('sgactivitystream_objects.id', ondelete='CASCADE')),
                  Column('activity_id', ForeignKey('sgactivitystream_activities.id', ondelete='CASCADE')))

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
