#include <stdio.h>
#include <math.h>

int main()
{
    FILE *out = fopen("tone.raw", "w");
    float amp = 16000; // amplitude
    float a = 220; // Hz - the tone
    // sounds
    float cis = a * exp(log(2)*16/12);
    float e =  a * exp(log(2)*19/12);
    float rate = 44100; // Hz, sampling
    int i;
    float omega = 2 * M_PI * a;
    for (i = 0; i < 10*rate; ++i)
    {
        float t = i / rate;
        // base tone
        short sample = amp * sinf(t * omega);
        // add next after 3 secs
        if (i > 3*rate)
            sample = (sample + amp * sinf(t * 2 * M_PI * cis))*0.5f;
        // add next after 3 secs
        if (i > 6*rate)
            sample = (sample + amp * sinf(t * 2 * M_PI * e))*0.5f;
        // gentle fade-out between 0:08 and 0:10
        if (i > 8*rate)
            sample *= 1 - (i - 8*rate) / (2*rate);
        // printf("%hd %f\n", sample, amp * sinf(t * omega));
        fwrite(&sample, 1, sizeof(short), out);
    }
    fclose(out);
    return 0;
}
