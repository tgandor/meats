htm: htm.cpp
	$(CXX) -ohtm htm.cpp

htm.cpp: htm.l
	flex -ohtm.cpp htm.l

clean:
	rm htm.cpp htm
