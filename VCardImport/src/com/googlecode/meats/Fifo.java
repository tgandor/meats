package com.googlecode.meats;

import java.util.Enumeration;
import java.util.Vector;

/**
 * A rudimentary queue, doesn't even shrink
 * @author tgandor
 */
public class Fifo  {
    
    private Vector data = new Vector();
    private int start = 0;
    
    public Fifo() {}
    
    public Fifo(Enumeration e) {
        while(e.hasMoreElements())
            data.addElement(e.nextElement());
    }
    
    public void enqueue(Object o) {
        data.addElement(o);
    }
    
    public Object dequeue() {
        if ( start < data.size() )
            return data.elementAt(start++);
        return null;
    }
    
    public boolean isEmpty() {
        return start == data.size();
    }
    
    public boolean hasMore() {
        return start < data.size();
    }
    
}
