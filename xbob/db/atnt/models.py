#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
# @date: Wed Oct 17 15:59:25 CEST 2012
#
# Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This file defines simple Client and File interfaces that should be comparable
with other xbob.db databases.
"""

import os
import bob

class Client:
  """The clients of this database contain ONLY client ids. Nothing special."""
  m_valid_client_ids = set(range(1, 41))

  def __init__(self, client_id):
    assert client_id in self.m_valid_client_ids
    self.id = client_id



class File:
  """Files of this database are composed from the client id and a file id."""
  m_valid_file_ids = set(range(1, 11))

  def __init__(self, client_id, client_file_id):
    assert client_file_id in self.m_valid_file_ids
    # compute the file id on the fly
    self.id = (client_id-1) * len(self.m_valid_file_ids) + client_file_id
    # copy client id
    self.client_id = client_id
    # generate path on the fly
    self.path = os.path.join("s" + str(client_id), str(client_file_id))


  @staticmethod
  def from_file_id(file_id):
    """Returns the File object for a given file_id"""
    client_id = (file_id-1) / len(File.m_valid_file_ids) + 1
    client_file_id = (file_id-1) % len(File.m_valid_file_ids) + 1
    return File(client_id, client_file_id)


  @staticmethod
  def from_path(path):
    """Returns the File object for a given path"""
    # get the last two paths
    paths = os.path.split(path)
    file_name = os.path.splitext(paths[1])[0]
    paths = os.path.split(paths[0])
    assert paths[1][0] == 's'
    return File(int(paths[1][1:]), int(file_name))


  def make_path(self, directory=None, extension=None):
    """Wraps the current path so that a complete path is formed

    Keyword parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    extension
      An optional extension that will be suffixed to the returned filename. The
      extension normally includes the leading ``.`` character as in ``.jpg`` or
      ``.hdf5``.

    Returns a string containing the newly generated file path.
    """

    if not directory: directory = ''
    if not extension: extension = ''

    return os.path.join(directory, self.path + extension)


  def save(self, data, directory=None, extension='.hdf5'):
    """Saves the input data at the specified location and using the given
    extension.

    Keyword parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      If not empty or None, this directory is prefixed to the final file
      destination

    extension
      The extension of the filename - this will control the type of output and
      the codec for saving the input blob.
    """

    path = self.make_path(directory, extension)
    bob.utils.makedirs_safe(os.path.dirname(path))
    bob.io.save(data, path)

