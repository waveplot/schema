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

from sqlalchemy import Column, DateTime, ForeignKey, Integer, SmallInteger
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import text

from wpschema.base import Base


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
                  server_default=text("(now() at time zone 'utc')"))

    editor_id = Column(Integer, ForeignKey('waveplot.editor.id'),
                       nullable=False)

    waveplot_gid = Column(UUID, ForeignKey('waveplot.waveplot.uuid'),
                          nullable=False)

    waveplot = relationship("WavePlot", backref="edits")

    def __repr__(self):
        return '<Edit {!r} at {!r}>'.format(self.type, self.time)
