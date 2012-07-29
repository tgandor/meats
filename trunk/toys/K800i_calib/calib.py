#!/usr/bin/env python

from cv import *
import numpy
import glob

def createChessboardMatrix(n, m):
    mat = CreateMat(n * m, 3, CV_32F)
    for i in xrange(n):
        for j in xrange(m):
            mat[i*m+j, 0] = j
            mat[i*m+j, 1] = i
            mat[i*m+j, 2] = 0
    return mat

def list2mat(l, type_ = CV_32F):
    mat = CreateMat(len(l), len(l[0]), type_)
    for i in xrange(len(l)):
        for j in xrange(len(l[i])):
            mat[i, j] = l[i][j]
    return mat

def out(mat):
    print numpy.asarray(mat)

def unrotMap(rvec, tvec):
    rotMat = CreateMat(3, 3, CV_32F)
    Rodrigues2(rvec, rotMat)
    unrotMat = CreateMat(3, 3, CV_32F)
    Invert(rotMat, unrotMat)
    return unrotMat

def unrotatedTvec(unrotMat, tvec):
    ttvec = CreateMat(3, 1, CV_32F)
    Transpose(tvec, ttvec)
    rotatedTvec = CloneMat(ttvec)
    MatMul(unrotMat, ttvec, rotatedTvec)
    return rotatedTvec

NamedWindow('wnd')

for i in glob.glob('*.JPG'):
    print i
    img = LoadImage(i, CV_LOAD_IMAGE_GRAYSCALE)
    print GetSize(img)
    size = (9, 6)
    ShowImage('wnd', img)
    WaitKey(0)

    found, corners = FindChessboardCorners(img, size)
    # DrawChessboardCorners(img, size, corners, found)
    print len(corners)

    cameraMatrix = CreateMat(3, 3, CV_32F)
    rvecs = CreateMat(1, 3, CV_32F)
    tvecs = CreateMat(1, 3, CV_32F)
    distCoefs = CreateMat(1, 5, CV_32F)
    objectPoints = createChessboardMatrix(size[1], size[0])

    error = CalibrateCamera2(
            objectPoints,
            list2mat(corners),
            list2mat([[9*6]], CV_32S),
            GetSize(img),
            cameraMatrix,
            distCoefs,
            rvecs,
            tvecs,
            0)

    print "Calibrated!"
    out(cameraMatrix)
    out(distCoefs)
    out(rvecs)
    out(tvecs)


    w, h = GetSize(img)
    mapx = CreateMat(h, w, CV_32FC1)
    mapy = CreateMat(h, w, CV_32FC1)
    outimg = CreateMat(h, w, CV_8U)

    # plain undistort
    InitUndistortMap(cameraMatrix, distCoefs, mapx, mapy)
    Remap(img, outimg, mapx, mapy)
    ShowImage('wnd', outimg)
    WaitKey(0)

    # undistort with unrotate
    InitUndistortRectifyMap(
            cameraMatrix,
            distCoefs,
            unrotMap(rvecs, tvecs),
            cameraMatrix,
            mapx, mapy)
    Remap(img, outimg, mapx, mapy)
    ShowImage('wnd', outimg)
    WaitKey(0)

    print mapx[0, 0]
    print mapy[0, 0]

    newvec = unrotatedTvec(unrotMap(rvecs, tvecs), tvecs)
    newvec2 = CloneMat(newvec)
    MatMul(cameraMatrix, newvec, newvec2)
    out(newvec2)

    newx = newvec2[0,0]/newvec2[2,0]
    newy = newvec2[1,0]/newvec2[2,0]
    print 'new x', newx
    print 'new y', newy

    newCam = CloneMat(cameraMatrix)
    newCam[0, 2] -= newx
    newCam[1, 2] -= newy
    InitUndistortRectifyMap(
            cameraMatrix,
            distCoefs,
            unrotMap(rvecs, tvecs),
            newCam,
            mapx, mapy)
    Remap(img, outimg, mapx, mapy)
    ShowImage('wnd', outimg)
    WaitKey(0)

    print mapx[0, 0]
    print mapy[0, 0]
