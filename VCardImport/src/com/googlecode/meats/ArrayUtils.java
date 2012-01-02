/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

/**
 * A lame replacement for some missing standards
 * @author olaija
 */
public class ArrayUtils {
    public static void sort(int[] arr)
    {
        for(int i=1; i<arr.length; ++i)
        {
            int val = arr[i];
            int j = i;
            while(j>0 && val < arr[j-1]) {
                arr[j] = arr[j-1];
                --j;
            }
            arr[j] = val;
        }

    }

    public static String pad(int n, int width)
    {
        String res = ""+n;
        if ( res.length() < width )
        {
            byte[] padding = new byte[width-res.length()];
            for(int i=0; i<padding.length; ++i)
                padding[i] = '0';
            String prefix = new String(padding);
            return prefix+res;
        }
        return res;
    }

}
