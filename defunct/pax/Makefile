SRC_FILES := $(wildcard *.cpp)
OBJ_FILES := $(patsubst %.cpp, %.o, $(SRC_FILES))
LD_FLAGS := 
CC_FLAGS := -std=c++0x -g

all: pax 
-include $(OBJ_FILES:.o=.d)

pax: $(OBJ_FILES)
	g++ $(LD_FLAGS) -o $@ $^

%.o: %.cpp
	g++ $(CC_FLAGS) -c -o $@ $<
	g++ -MM $(CC_FLAGS) -c $*.cpp > $*.d

depend:
	makedepend -- $(CC_FLAGS) -- $(SRC_FILES)

clean:
	rm pax *.o *.d
