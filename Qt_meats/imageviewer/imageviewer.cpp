/****************************************************************************
**
** Copyright (C) 2013 Digia Plc and/or its subsidiary(-ies).
** Contact: http://www.qt-project.org/legal
**
** Modifications Copyright (C) 2016 tgandor - licensed likewise,
** under the terms of the BSD license.
**
** $QT_BEGIN_LICENSE:BSD$
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
**   * Neither the name of Digia Plc and its Subsidiary(-ies) nor the names
**     of its contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
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
**
** $QT_END_LICENSE$
**
****************************************************************************/

// finally, the right way: https://stackoverflow.com/a/24003230/1338797
#include <QtGlobal>
#if QT_VERSION >= QT_VERSION_CHECK(5, 0, 0)
#  include <QtWidgets>
#else
#  include <QtGui>
#endif

#include <QInputDialog>
#include <QShortcut>

#include "imageviewer.h"
#include "organize.h"

ImageViewer::ImageViewer()
{
    imageLabel = new QLabel;
    imageLabel->setBackgroundRole(QPalette::Base);
    imageLabel->setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    imageLabel->setScaledContents(true);

    scrollArea = new QScrollArea;
    scrollArea->setBackgroundRole(QPalette::Dark);
    scrollArea->setWidget(imageLabel);
    setCentralWidget(scrollArea);

    toolBar = new QToolBar;

    createActions();
    createMenus();

    toolBar->addAction(openAct);
    toolBar->addAction(prevAct);
    toolBar->addAction(nextAct);
    toolBar->addAction(zoomInAct);
    toolBar->addAction(zoomOutAct);
    toolBar->addAction(normalSizeAct);
    toolBar->addAction(fitToWindowAct);
    addToolBar(toolBar);

    setWindowTitle(tr("Image Sorter"));
    resize(1200, 800);

    scaleFactor = 1.0;
    statusBar()->show();
}

void ImageViewer::open()
{
    const QString LAST_DIRECTORY("last_directory");
    QSettings mySettings; // http://stackoverflow.com/a/3598245/1338797
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open File"),
                                                    mySettings.value(LAST_DIRECTORY).toString());
    if (!fileName.isEmpty())
    {
        QDir currentDirectory;
        mySettings.setValue(LAST_DIRECTORY, currentDirectory.absoluteFilePath(fileName));
        displayFile(fileName);
        feeder.reload(fileName);
    }
}

void ImageViewer::next()
{
    displayFile(feeder.next());
}

void ImageViewer::prev()
{
    displayFile(feeder.prev());
}

void ImageViewer::first()
{
    feeder.rewind();
    next();
}

void ImageViewer::last()
{
    feeder.rewind();
    feeder.next();
    prev();
}

void ImageViewer::zoomIn()
{
    scaleImage(1.25);
    updateActions();
}

void ImageViewer::zoomOut()
{
    scaleImage(0.8);
    updateActions();
}

void ImageViewer::normalSize()
{
    imageLabel->adjustSize();
    scaleFactor = 1.0;
    scaleImage(1.0);
}

void ImageViewer::fitToWindow()
{
    double widthRatio = 1.0 * scrollArea->width() / imageLabel->width();
    double heightRatio = 1.0 * scrollArea->height() / imageLabel->height();
    scaleImage(std::min(widthRatio, heightRatio));
    updateActions();
}

void ImageViewer::moveGroup()
{
    bool ok;
    // QMessageBox::information(this, "Test", "It works");

    QString eventName = QInputDialog::getText(this, "Move pictures to subfolder",
                                              "Event name:", QLineEdit::Normal, "", &ok);

    if (ok && !eventName.isEmpty())
    {
        createEvent(feeder, eventName);

        QString nextCandidate = feeder.next();
        QFile nextFile(nextCandidate);
        if (nextFile.exists())
        {
            displayFile(nextCandidate);
        }
        else
        {
            imageLabel->clear();
        }
        // works when not exists too
        feeder.reload(nextCandidate);
    }

}

void ImageViewer::deleteCurrent()
{
    ::deleteCurrent(feeder);
    displayFile(feeder.next());
}

void ImageViewer::about()
{
    QMessageBox::about(this, tr("About Image Sorter"),
            tr("<p>The <b>Image Sorter</b> is based on the <b>Image Viewer</b> Qt example.</p>"
               "<p>Removed features:</p>"
               "<ul>"
               "<li>Printing the image</li>"
               "<li>Force-fit image to window</li>"
               "<li>Zoom out limit scale>=0.33 (now >= 0.05)</li>"
               "</ul>"
               "<p>Added features:</p>"
               "<ul>"
               "<li>Toolbar</li>"
               "<li>Prev/next image in the directory</li>"
               "<li>Aspect-preserving fit to window (zooming action)</li>"
               "<li>Automatic fitting (zoom) to window when loading image</li>"
               //"<li></li>"
               "</ul>"
               ));
}

void ImageViewer::displayFile(const QString &fileName)
{
    if (fileName.isEmpty() || !QFile(fileName).exists())
    {
        imageLabel->clear();
        statusBar()->showMessage("No file loaded.");
        setWindowTitle("Image Sorter");
        resetActions();
        return;
    }

    QImage image(fileName);
    if (image.isNull())
    {
        QMessageBox::information(this, tr("Image Sorter"), tr("Cannot load %1.").arg(fileName));
        return;
    }

    imageLabel->setPixmap(QPixmap::fromImage(image));

    updateActions();

    imageLabel->adjustSize();

    scaleImage(1.0);
    if (autoFitAct->isChecked())
    {
        fitToWindow();
    }

    statusBar()->showMessage(QString("Loaded: ") + fileName);
    setWindowTitle(fileName + " - Image Sorter");
}



void ImageViewer::createActions()
{
    openAct = new QAction(tr("&Open..."), this);
    openAct->setShortcut(tr("Ctrl+O"));
    connect(openAct, SIGNAL(triggered()), this, SLOT(open()));

    nextAct = new QAction(tr("&Next"), this);
    nextAct->setShortcut(tr("Ctrl+N"));
    nextAct->setEnabled(false);
    connect(nextAct, SIGNAL(triggered()), this, SLOT(next()));

    QShortcut *nextArrow = new QShortcut(QKeySequence(Qt::Key_Right), this);
    connect(nextArrow, SIGNAL(activated()), this, SLOT(next()));
    QShortcut *nextSpace = new QShortcut(QKeySequence(Qt::Key_Space), this);
    connect(nextSpace, SIGNAL(activated()), this, SLOT(next()));

    prevAct = new QAction(tr("&Prev..."), this);
    prevAct->setShortcut(tr("Ctrl+P"));
    prevAct->setEnabled(false);
    connect(prevAct, SIGNAL(triggered()), this, SLOT(prev()));

    QShortcut *prevArrow = new QShortcut(QKeySequence(Qt::Key_Left), this);
    connect(prevArrow, SIGNAL(activated()), this, SLOT(prev()));
    QShortcut *prevBackspace = new QShortcut(QKeySequence(Qt::Key_Backspace), this);
    connect(prevBackspace, SIGNAL(activated()), this, SLOT(prev()));

    firstAct = new QAction(tr("&First"), this);
    firstAct->setShortcut(tr("Ctrl+A"));
    firstAct->setEnabled(false);
    connect(firstAct, SIGNAL(triggered()), this, SLOT(first()));

    lastAct = new QAction(tr("&Last"), this);
    lastAct->setShortcut(tr("Ctrl+E"));
    lastAct->setEnabled(false);
    connect(lastAct, SIGNAL(triggered()), this, SLOT(last()));

    QShortcut* firstShortcut = new QShortcut(QKeySequence(Qt::Key_Home), this);
    connect(firstShortcut, SIGNAL(activated()), this, SLOT(first()));

    QShortcut* lastShortcut = new QShortcut(QKeySequence(Qt::Key_End), this);
    connect(lastShortcut, SIGNAL(activated()), this, SLOT(last()));

    exitAct = new QAction(tr("E&xit"), this);
    exitAct->setShortcut(tr("Ctrl+Q"));
    connect(exitAct, SIGNAL(triggered()), this, SLOT(close()));

    zoomInAct = new QAction(tr("Zoom &In"), this);
    zoomInAct->setShortcut(tr("Ctrl++"));
    zoomInAct->setEnabled(false);
    connect(zoomInAct, SIGNAL(triggered()), this, SLOT(zoomIn()));

    zoomOutAct = new QAction(tr("Zoom &Out"), this);
    zoomOutAct->setShortcut(tr("Ctrl+-"));
    zoomOutAct->setEnabled(false);
    connect(zoomOutAct, SIGNAL(triggered()), this, SLOT(zoomOut()));

    normalSizeAct = new QAction(tr("&Normal Size"), this);
    normalSizeAct->setShortcut(tr("Ctrl+S"));
    normalSizeAct->setEnabled(false);
    connect(normalSizeAct, SIGNAL(triggered()), this, SLOT(normalSize()));

    fitToWindowAct = new QAction(tr("&Fit to Window"), this);
    fitToWindowAct->setEnabled(false);
    fitToWindowAct->setShortcut(tr("Ctrl+F"));
    connect(fitToWindowAct, SIGNAL(triggered()), this, SLOT(fitToWindow()));

    autoFitAct = new QAction(tr("A&uto Fit to window"), this);
    autoFitAct->setEnabled(true);
    autoFitAct->setCheckable(true);

    moveGroupAct = new QAction(tr("&Move group to subfolder"), this);
    moveGroupAct->setShortcut(tr("Ctrl+M"));
    moveGroupAct->setEnabled(false);
    connect(moveGroupAct, SIGNAL(triggered()), this, SLOT(moveGroup()));

    deleteAction = new QAction(tr("&Delete current image"), this);
    deleteAction->setShortcut(tr("Ctrl+D"));
    deleteAction->setEnabled(false);
    connect(deleteAction, SIGNAL(triggered()), this,SLOT(deleteCurrent()));

    aboutAct = new QAction(tr("&About"), this);
    connect(aboutAct, SIGNAL(triggered()), this, SLOT(about()));

    aboutQtAct = new QAction(tr("About &Qt"), this);
    connect(aboutQtAct, SIGNAL(triggered()), qApp, SLOT(aboutQt()));
}



void ImageViewer::createMenus()

{
    fileMenu = new QMenu(tr("&File"), this);
    fileMenu->addAction(openAct);
    fileMenu->addAction(prevAct);
    fileMenu->addSeparator();
    fileMenu->addAction(moveGroupAct);
    fileMenu->addAction(deleteAction);
    fileMenu->addSeparator();
    fileMenu->addAction(exitAct);

    viewMenu = new QMenu(tr("&View"), this);
    viewMenu->addAction(zoomInAct);
    viewMenu->addAction(zoomOutAct);
    viewMenu->addAction(normalSizeAct);
    viewMenu->addAction(fitToWindowAct);
    viewMenu->addSeparator();
    viewMenu->addAction(autoFitAct);

    helpMenu = new QMenu(tr("&Help"), this);
    helpMenu->addAction(aboutAct);
    helpMenu->addAction(aboutQtAct);

    menuBar()->addMenu(fileMenu);
    menuBar()->addMenu(viewMenu);
    menuBar()->addMenu(helpMenu);
}



void ImageViewer::updateActions()

{
    nextAct->setEnabled(true);
    prevAct->setEnabled(true);
    firstAct->setEnabled(true);
    lastAct->setEnabled(true);
    fitToWindowAct->setEnabled(true);
    normalSizeAct->setEnabled(true);
    zoomInAct->setEnabled(scaleFactor < 3.0);
    zoomOutAct->setEnabled(scaleFactor > 0.05);
    moveGroupAct->setEnabled(true);
    deleteAction->setEnabled(true);
}



void ImageViewer::resetActions()

{
    nextAct->setEnabled(false);
    prevAct->setEnabled(false);
    firstAct->setEnabled(false);
    lastAct->setEnabled(false);
    fitToWindowAct->setEnabled(false);
    normalSizeAct->setEnabled(false);
    zoomInAct->setEnabled(false);
    zoomOutAct->setEnabled(false);
    moveGroupAct->setEnabled(false);
    deleteAction->setEnabled(false);
}



void ImageViewer::scaleImage(double factor)

{
    Q_ASSERT(imageLabel->pixmap());
    scaleFactor *= factor;
    imageLabel->resize(scaleFactor * imageLabel->pixmap()->size());

    adjustScrollBar(scrollArea->horizontalScrollBar(), factor);
    adjustScrollBar(scrollArea->verticalScrollBar(), factor);

    statusBar()->showMessage(QString().sprintf("Scale set to: %.2lf x", scaleFactor));
}



void ImageViewer::adjustScrollBar(QScrollBar *scrollBar, double factor)

{
    scrollBar->setValue(int(factor * scrollBar->value()
                            + ((factor - 1) * scrollBar->pageStep()/2)));
}
