from mechanize import Browser
from shutil import copyfile
br = Browser()
br.open("http://www.fileformat.info/format/tiff/sample/index.htm")

for link in br.links(url_regex="download"):
	file, hdrs = br.retrieve(link.absolute_url)
	fname = hdrs['content-disposition'].replace('download;filename=', '')
	copyfile(file, fname)
