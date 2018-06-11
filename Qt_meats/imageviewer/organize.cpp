#include "organize.h"

#include "directoryfeeder.h"

#include <QDebug>
#include <QRegExp>
#include <QFile>
#include <QDir>

QString extractDate(const QString& path)
{
    // 1. try formatted datetime in image headers
    QRegExp datetime("\\d{4}([ :]\\d\\d){5}");
    QFile file(path);
    file.open(QIODevice::ReadOnly);
    const int SIZE = 1<<11;
    QByteArray header = file.read(SIZE);
    header.replace('\0', ' '); // must there not be a better way?
    QString dingbats(header);
    int pos;
    if ((pos = datetime.indexIn(dingbats, 0)) != -1)
    {
        QString raw(datetime.cap());
        qDebug() << "Found at" << pos << raw;
        // this would do it for datetime:
        // raw.replace(" ", "_");
        // raw.replace(":", "");
        raw.replace(QRegExp(" .*"), "");
        raw.replace(":", "-");
        return raw + "-";
    }

    // 2. try eight digits in file name
    QFileInfo info(path);
    QRegExp date("\\d{8}");
    QString basename = info.baseName();
    if (date.indexIn(basename, 0) != -1)
    {
        QString raw = date.cap();
        return raw.left(4) + "-" + raw.mid(4, 2) + "-" + raw.right(2) + "-";
    }

    // 3. give up
    return QString();
}

void createEvent(DirectoryFeeder &feeder, const QString &name)
{
    QString lastOne = feeder.current();
    feeder.rewind();

    QFileInfo last(lastOne);
    QDir parent = last.dir();
    QString subdir(extractDate(lastOne) + name);
    subdir.replace(" ", "-");
    parent.mkdir(subdir);
    subdir = parent.absolutePath() + QDir::separator() + subdir + QDir::separator();

    for (;;)
    {
        QString next = feeder.next();
        qDebug() << next << extractDate(next);
        if (next.isEmpty())
        {
            break;
        }

        QFile nextFile(next);
        QFileInfo nextFileInfo(next);
        nextFile.rename(subdir + nextFileInfo.fileName());

        if (next == lastOne)
        {
            break;
        }
    }
    qDebug() << name;
}

void deleteCurrent(DirectoryFeeder &feeder)
{
    QFile toDelete(feeder.current());
    if (!toDelete.exists())
        return;
    QFileInfo toDeleteInfo(toDelete);
    QDir parent = toDeleteInfo.absoluteDir();
    QDir trash(parent.absolutePath() + QDir::separator() + "_trash");
    if (!trash.exists())
    {
        trash.mkpath(".");
    }
    QString target = trash.absolutePath() + QDir::separator() + toDeleteInfo.fileName();
    qDebug() << "Moving" << toDeleteInfo.canonicalFilePath() << "to" << target;
    toDelete.rename(target);
    feeder.remove();
}
