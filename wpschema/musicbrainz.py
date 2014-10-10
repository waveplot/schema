# -*- coding: utf8 -*-

# Copyright (C) 2014  Ben Ockmore

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""This module defines the database models for tables within the musicbrainz
schema, including Artist, Release, Recording and Track.
"""

import datetime

from sqlalchemy import (Boolean, CHAR, Column, DateTime, ForeignKey, Integer,
                        SmallInteger, Unicode, UnicodeText, Table)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from wpschema.base import Base

class Artist(Base):

    __tablename__ = 'artist'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(UnicodeText, nullable=False)
    sort_name = Column(UnicodeText, nullable=False)

    begin_date_year = Column(SmallInteger)
    begin_date_month = Column(SmallInteger)
    begin_date_day = Column(SmallInteger)

    end_date_year = Column(SmallInteger)
    end_date_month = Column(SmallInteger)
    end_date_day = Column(SmallInteger)

    type_id = Column('type', Integer, ForeignKey('musicbrainz.artist_type.id'))
    area_id = Column('area', Integer, ForeignKey('musicbrainz.area.id'))
    gender_id = Column('gender', Integer, ForeignKey('musicbrainz.gender.id'))
    comment = Column(Unicode(255), default=u'', nullable=False)

    edits_pending = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    ended = Column(Boolean, default=False, nullable=False)

    begin_area_id = Column('begin_area', Integer,
                           ForeignKey('musicbrainz.area.id'))
    end_area_id = Column('end_area', Integer,
                         ForeignKey('musicbrainz.area.id'))

    type = relationship('ArtistType')
    gender = relationship('Gender')
    area = relationship('Area', foreign_keys=area_id)
    begin_area = relationship('Area', foreign_keys=begin_area_id)
    end_area = relationship('Area', foreign_keys=end_area_id)


class ArtistType(Base):

    __tablename__ = 'artist_type'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent = Column(Integer, ForeignKey('musicbrainz.artist_type.id'))

    child_order = Column(Integer, default=0, nullable=False)

    description = Column(UnicodeText)

    children = relationship('ArtistType')


class Gender(Base):

    __tablename__ = 'gender'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent = Column(Integer, ForeignKey('musicbrainz.gender.id'))

    child_order = Column(Integer, default=0, nullable=False)

    description = Column(UnicodeText)

    children = relationship('Gender')


class Area(Base):

    __tablename__ = 'area'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(UnicodeText, nullable=False)

    type_id = Column('type', Integer, ForeignKey('musicbrainz.area_type.id'))

    edits_pending = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    begin_date_year = Column(SmallInteger)
    begin_date_month = Column(SmallInteger)
    begin_date_day = Column(SmallInteger)

    end_date_year = Column(SmallInteger)
    end_date_month = Column(SmallInteger)
    end_date_day = Column(SmallInteger)

    ended = Column(Boolean, default=False, nullable=False)
    comment = Column(Unicode(255), default=u'', nullable=False)

    type = relationship('AreaType')


class AreaType(Base):

    __tablename__ = 'area_type'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent = Column(Integer, ForeignKey('musicbrainz.area_type.id'))

    child_order = Column(Integer, default=0, nullable=False)

    description = Column(UnicodeText)

    children = relationship('AreaType')


class Recording(Base):

    __tablename__ = 'recording'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(UnicodeText, nullable=False)

    artist_credit_id = Column(
        'artist_credit', Integer, ForeignKey('musicbrainz.artist_credit.id'),
        nullable=False
    )

    length = Column(Integer)

    comment = Column(Unicode(255), default=u'', nullable=False)
    edits_pending = Column(Integer, default=0, nullable=False)

    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    video = Column(Boolean, default=False)

    artist_credit = relationship('ArtistCredit')


class RecordingRedirect(Base):

    __tablename__ = 'recording_gid_redirect'
    __table_args__ = {'schema': 'musicbrainz'}

    gid = Column(UUID(as_uuid=True), primary_key=True)
    new_id = Column(Integer, ForeignKey('musicbrainz.recording.id'))
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class ArtistCredit(Base):

    __tablename__ = 'artist_credit'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)

    artist_count = Column(SmallInteger, nullable=False)

    ref_count = Column(Integer, default=0)

    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)


class Release(Base):

    __tablename__ = 'release'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(UnicodeText, nullable=False)

    artist_credit_id = Column(
        'artist_credit', Integer, ForeignKey('musicbrainz.artist_credit.id'),
        nullable=False
    )
    release_group_id = Column(
        'release_group', Integer, ForeignKey('musicbrainz.release_group.id'),
        nullable=False
    )
    status_id = Column('status', Integer,
                       ForeignKey('musicbrainz.release_status.id'))
    packaging_id = Column('packaging', Integer,
                          ForeignKey('musicbrainz.release_packaging.id'))
    language_id = Column('language', Integer,
                         ForeignKey('musicbrainz.language.id'))
    script_id = Column('script', Integer, ForeignKey('musicbrainz.script.id'))

    barcode = Column(Unicode(255))
    comment = Column(Unicode(255), default=u'', nullable=False)

    edits_pending = Column(Integer, default=0, nullable=False)
    quality = Column(SmallInteger, default=-1, nullable=False)

    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    packaging = relationship('ReleasePackaging')
    status = relationship('ReleaseStatus')
    language = relationship('Language')
    artist_credit = relationship('ArtistCredit')
    release_group = relationship('ReleaseGroup', backref='releases')
    script = relationship('Script')


class ReleaseRedirect(Base):

    __tablename__ = 'release_gid_redirect'
    __table_args__ = {'schema': 'musicbrainz'}

    gid = Column(UUID(as_uuid=True), primary_key=True)
    new_id = Column(Integer, ForeignKey('musicbrainz.release.id'))
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)

class ReleasePackaging(Base):

    __tablename__ = 'release_packaging'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent = Column(Integer, ForeignKey('musicbrainz.release_packaging.id'))

    child_order = Column(Integer, default=0, nullable=False)

    description = Column(UnicodeText)

    children = relationship('ReleasePackaging')


class ReleaseStatus(Base):

    __tablename__ = 'release_status'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent = Column(Integer, ForeignKey('musicbrainz.release_status.id'))

    child_order = Column(Integer, default=0, nullable=False)

    description = Column(UnicodeText)

    children = relationship('ReleaseStatus')


class Language(Base):

    __tablename__ = 'language'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)

    iso_code_2t = Column(Unicode(3))
    iso_code_2b = Column(Unicode(3))
    iso_code_1 = Column(Unicode(2))

    name = Column(Unicode(100), nullable=False)

    frequency = Column(Integer, default=0, nullable=False)

    iso_code_3 = Column(Unicode(2))


class Script(Base):

    __tablename__ = 'script'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)

    iso_code = Column(CHAR(4, convert_unicode=True), nullable=False)
    iso_number = Column(CHAR(3, convert_unicode=True), nullable=False)

    name = Column(Unicode(100), nullable=False)
    frequency = Column(Integer, default=0, nullable=False)


class ReleaseGroup(Base):

    __tablename__ = 'release_group'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID(as_uuid=True), unique=True, nullable=False)
    name = Column(UnicodeText, nullable=False)

    artist_credit_id = Column(
        'artist_credit', Integer, ForeignKey('musicbrainz.artist_credit.id'),
        nullable=False
    )
    type_id = Column('type', Integer,
                     ForeignKey('musicbrainz.release_group_primary_type.id'))

    comment = Column(Unicode(255), default=u'', nullable=False)

    edits_pending = Column(Integer, default=0, nullable=False)

    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    artist_credit = relationship('ArtistCredit')
    type = relationship('ReleaseGroupPrimaryType')


class ReleaseGroupPrimaryType(Base):

    __tablename__ = 'release_group_primary_type'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(255), nullable=False)

    parent = Column(Integer,
                    ForeignKey('musicbrainz.release_group_primary_type.id'))

    child_order = Column(Integer, default=0, nullable=False)

    description = Column(UnicodeText)

    children = relationship('ReleaseGroupPrimaryType')


class Medium(Base):

    __tablename__ = 'medium'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)

    release_id = Column('release', Integer,
                        ForeignKey('musicbrainz.release.id'), nullable=False)
    position = Column(Integer, nullable=False)
    format = Column(Integer)
    name = Column(Unicode(255))

    edits_pending = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    track_count = Column(Integer, default=0, nullable=False)


class Track(Base):

    __tablename__ = 'track'
    __table_args__ = {'schema':'musicbrainz'}

    id = Column(Integer, primary_key=True)
    gid = Column(UUID(as_uuid=True), unique=True, nullable=False)

    recording_id = Column(
        'recording', Integer, ForeignKey('musicbrainz.recording.id'),
        nullable=False
    )
    medium_id = Column('medium', Integer, ForeignKey('musicbrainz.medium.id'),
                       nullable=False)
    position = Column(Integer, nullable=False)
    number = Column(UnicodeText, nullable=False)
    name = Column(Unicode, nullable=False)
    artist_credit_id = Column(
        'artist_credit', Integer, ForeignKey('musicbrainz.artist_credit.id'),
        nullable=False
    )
    length = Column(Integer)

    edits_pending = Column(Integer, default=0, nullable=False)

    last_updated = Column(DateTime(timezone=True),
                          default=datetime.datetime.utcnow)

    artist_credit = relationship('ArtistCredit')
    recording = relationship('Recording')


class TrackRedirect(Base):

    __tablename__ = 'track_gid_redirect'
    __table_args__ = {'schema': 'musicbrainz'}

    gid = Column(UUID(as_uuid=True), primary_key=True)
    new_id = Column(Integer, ForeignKey('musicbrainz.track.id'))
    created = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
