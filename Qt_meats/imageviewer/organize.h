#ifndef ORGANIZE_H
#define ORGANIZE_H

#pragma once

class DirectoryFeeder;
class QString;

void createEvent(DirectoryFeeder& feeder, const QString& name);
void deleteCurrent(DirectoryFeeder& feeder);

#endif // ORGANIZE_H

