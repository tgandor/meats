/*
 * Copyright (C) 2016 tgandor
 *
** You may use this file under the terms of the BSD license as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
*/

#include "directoryfeeder.h"

#include <QDir>
#include <QFileInfo>

DirectoryFeeder::DirectoryFeeder()
{
}

void DirectoryFeeder::reload(const QString &filename)
{
    QFileInfo info(filename);
    if (!info.exists())
    {
        files.clear();
        return;
    }
    QDir parent = info.isDir() ? QDir(filename) : info.dir();
    parent.setSorting(QDir::Name);
    files = parent.entryList(QStringList() << "*.jpg");
    currentDirectory = parent.absolutePath();
    if (files.contains(info.fileName()))
    {
        currentIndex = files.indexOf(info.fileName());
    }
    else
    {
        currentIndex = 0;
    }
}

QString DirectoryFeeder::next()
{
    if (files.empty())
        return QString();
    currentIndex = (currentIndex + 1) % files.size();
    return currentDirectory + QDir::separator() +  files[currentIndex];
}

QString DirectoryFeeder::prev()
{
    if (files.empty())
        return QString();
    currentIndex = (currentIndex + files.size() - 1) % files.size();
    return currentDirectory + QDir::separator() +  files[currentIndex];
}

QString DirectoryFeeder::current()
{
    if (files.empty() || currentIndex < 0 || currentIndex >= files.size())
        return QString();
    return currentDirectory + QDir::separator() +  files[currentIndex];
}

void DirectoryFeeder::rewind()
{
    currentIndex = -1;
}

void DirectoryFeeder::remove()
{
    if (files.empty() || currentIndex < 0 || currentIndex >= files.size())
        return;
    files.removeAt(currentIndex);
    if (files.empty())
        currentIndex = -1;
    else
        (void) prev();
}
