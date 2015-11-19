package com.googlecode.meats;

import com.googlecode.meats.mappers.IntStr;

/**
 *
 * @author root
 */
public class Mapper {
    static String[] map(int[] data, IntStr mapper) {
        String[] res = new String[data.length];
        for(int i = 0; i<data.length; ++i)
            res[i] = mapper.map(data[i]);
        return res;
    }    
}
