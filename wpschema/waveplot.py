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


"""This module defines the database models for tables within the waveplot
schema, including WavePlot, WavePlotContext, Edit, Editor and Question.
"""

from sqlalchemy import (Boolean, Column, DateTime, Enum, ForeignKey, Integer,
                        Interval, SmallInteger, String, UnicodeText)
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text as sql_text

from wpschema.base import Base


WAVEPLOT_VERSIONS = [
    u"CITRUS",
    u"DAMSON",
]


class Edit(Base):
    """Respresents an Edit.

    An edit is any modification of WavePlot data by an Editor, whether that's
    uploading a new waveplot, adding tempo information to a track, or linking
    a WavePlot to various MusicBrainz entities.
    """

    __tablename__ = 'edit'
    __table_args__ = {'schema': 'waveplot'}

    id = Column(Integer, primary_key=True)

    type = Column(SmallInteger, nullable=False)

    time = Column(DateTime, nullable=False,
                  server_default=sql_text("(now() at time zone 'utc')"))

    editor_id = Column(Integer, ForeignKey('waveplot.editor.id'),
                       nullable=False)

    waveplot_gid = Column(
        UUID(as_uuid=True), ForeignKey('waveplot.waveplot.gid'), nullable=False
    )

    editor = relationship("Editor", backref='edits')
    waveplot = relationship("WavePlot", backref="edits")

    def __repr__(self):
        return '<Edit {!r} at {!r}>'.format(self.type, self.time)


class Editor(Base):
    """Represents an Editor.

    An editor is a user of the WavePlot website who is able to
    contribute new WavePlots, by scanning audio files on their system.
    Contributors must be editors so that their contributions can be
    undone if made maliciously.
    """

    __tablename__ = 'editor'
    __table_args__ = {'schema': 'waveplot'}

    id = Column(Integer, primary_key=True)

    name = Column(UnicodeText, nullable=False)

    email = Column(UnicodeText, nullable=False)

    key = Column(String(6), nullable=False, unique=True)

    query_rate = Column(Integer, nullable=False, server_default=sql_text("60"))

    active = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Editor {!r}>'.format(self.name)


class WavePlot(Base):
    """Class to represent a WavePlot, which is a representation of
    sound, and information related to that sound.
    """

    __tablename__ = 'waveplot'
    __table_args__ = {'schema': 'waveplot'}

    gid = Column(UUID(as_uuid=True), primary_key=True)

    duration = Column(Interval, nullable=False)

    source_type = Column(String(20), nullable=False)

    sample_rate = Column(Integer)

    bit_depth = Column(SmallInteger)

    bit_rate = Column(Integer)

    num_channels = Column(SmallInteger, nullable=False)

    dr_level = Column(SmallInteger, nullable=False)

    image_hash = Column(BYTEA(20), nullable=False)

    full = Column(BYTEA, nullable=False)
    preview = Column(BYTEA(400), nullable=False)
    thumbnail = Column(BYTEA(50), nullable=False)
    sonic_hash = Column(Integer, nullable=False)

    version = Column(
        Enum(*WAVEPLOT_VERSIONS, name='waveplot_version',
             inherit_schema=True),
        nullable=False
    )

    contexts = relationship('WavePlotContext', backref="waveplot")

    def __repr__(self):
        return '<WavePlot {!r}>'.format(self.gid)


class WavePlotContext(Base):
    """Represents a link between a WavePlot and a track, also storing the
    release, recording and artist credit to speed up searches and browsing.
    """

    __tablename__ = 'waveplot_context'
    __table_args__ = {'schema': 'waveplot'}

    id = Column(Integer, primary_key=True)

    waveplot_gid = Column(
        UUID(as_uuid=True), ForeignKey('waveplot.waveplot.gid'), nullable=False
    )

    # Ideally, these would be foreign keys, but MB IDs can be deleted through
    # replication.
    release_gid = Column(UUID(as_uuid=True), nullable=False)
    recording_gid = Column(UUID(as_uuid=True), nullable=False)
    track_gid = Column(UUID(as_uuid=True), nullable=False)
    artist_credit_id = Column(Integer, nullable=False)

    def __repr__(self):
        return '<WavePlotContext {!r}->{!r}>'.format(self.waveplot_gid,
                                                     self.track_gid)


class Question(Base):
    """Class to represent questions on the website help page."""

    __tablename__ = 'question'
    __table_args__ = {'schema': 'waveplot'}

    id = Column(Integer, primary_key=True)

    text = Column(UnicodeText, nullable=False)
    category = Column(SmallInteger, nullable=False)

    # Number of visits since "answered" date
    views = Column(Integer, nullable=False, server_default=sql_text("0"))

    # Optional properties
    answer = Column(UnicodeText)
    answer_time = Column(DateTime)

    def __repr__(self):
        return '<Question {!r}>'.format(self.text)
